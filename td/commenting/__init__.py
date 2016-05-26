def get_model():
    from .models import CommentWithTags
    # print "commenting/__init__.get_model()", CommentWithTags
    return CommentWithTags


def get_form():
    from .forms import CommentFormWithTags
    # print "commenting/__init__.get_forms()", CommentFormWithTags
    return CommentFormWithTags


def get_form_target():
    from django.core.urlresolvers import reverse
    from .views import post_comment
    # print "commenting/__init__.get_form_target", post_comment
    return reverse("comment:post_comment")
