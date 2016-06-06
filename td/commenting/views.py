from __future__ import absolute_import

from account.mixins import LoginRequiredMixin
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from django.utils.html import escape

import django_comments
from django.views.generic import View
from django_comments import signals
from django_comments.views.comments import CommentPostBadRequest
from django_comments.views.utils import next_redirect


class PostCommentView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        return super(PostCommentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, next=None, using=None):
        # Fill out some initial data fields from an authenticated user, if present
        data = request.POST.copy()
        data["name"] = request.user.get_full_name() or request.user.get_username()
        data["email"] = request.user.email

        # Look up the object we're trying to comment about
        result = self._lookup_object(data.get("content_type"), data.get("object_pk"), using)
        if isinstance(result, CommentPostBadRequest):
            return result
        else:
            model, target = result

        # Do we want to preview the comment?
        preview = "preview" in data

        # Construct the comment form
        form = django_comments.get_form()(target, data=data)

        # Check security information
        if form.security_errors():
            return CommentPostBadRequest("The comment form failed security verification: %s" %
                                         escape(str(form.security_errors())))

        # If there are errors or if we requested a preview show the comment
        if form.errors or preview:
            template_list = [
                # These first two exist for purely historical reasons. Django v1.0 and v1.1 allowed the underscore
                # format for preview templates, so we have to preserve that format.
                "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.model_name),
                "comments/%s_preview.html" % model._meta.app_label,
                # Now the usual directory based template hierarchy.
                "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.model_name),
                "comments/%s/preview.html" % model._meta.app_label,
                "comments/preview.html",
            ]
            return render(request, template_list, {
                "comment": form.data.get("comment", ""),
                "form": form,
                "next": data.get("next", next),
            })

        # Otherwise create the comment
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        comment.user = request.user
        html_comment, tags = form.process_tags()
        comment.comment = html_comment

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(sender=comment.__class__, comment=comment, request=request)

        for (receiver, response) in responses:
            if response is False:
                return CommentPostBadRequest(
                    "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(sender=comment.__class__, comment=comment, request=request)

        # Add the tags that are extracted from the comment
        comment.tags.add(*tags)

        return next_redirect(request, fallback=next or 'comments-comment-done', c=comment._get_pk_val())

    @staticmethod
    def _lookup_object(ctype=None, object_pk=None, using=None):
        if ctype is None or object_pk is None:
            return CommentPostBadRequest("Missing content_type or object_pk field.")
        try:
            model = apps.get_model(*ctype.split(".", 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except TypeError:
            return CommentPostBadRequest("Invalid content_type value: %r" % escape(ctype))
        except AttributeError:
            return CommentPostBadRequest("The given content-type %r does not resolve to a valid model." % escape(ctype))
        except ObjectDoesNotExist:
            return CommentPostBadRequest("No object matching content-type %r and object PK %r exists." %
                                         (escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest("Attempting go get content-type %r and object PK %r exists raised %s" %
                                         (escape(ctype), escape(object_pk), e.__class__.__name__))

        return model, target
