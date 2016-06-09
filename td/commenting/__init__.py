def get_model():
    from .models import CommentWithTags
    return CommentWithTags


def get_form():
    from .forms import CommentFormWithTags
    return CommentFormWithTags


def get_form_target():
    from django.core.urlresolvers import reverse
    return reverse("comment:post_comment")
