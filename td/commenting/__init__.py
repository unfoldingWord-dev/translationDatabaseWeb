def get_model():
    from .models import CommentWithTags
    return CommentWithTags


def get_form():
    from .forms import CommentFormWithTags
    return CommentFormWithTags
