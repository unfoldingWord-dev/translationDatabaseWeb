import re

from django_comments.forms import CommentForm

from td.commenting.models import CommentTag


class CommentFormWithTags(CommentForm):

    def __init__(self, *args, **kwargs):
        super(CommentFormWithTags, self).__init__(*args, **kwargs)
        comment_textarea = self.fields["comment"].widget
        comment_textarea.attrs["rows"] = "3"
        comment_textarea.attrs["placeholder"] = "Type a comment here..."

    def process_tags(self):
        comment = self.cleaned_data.get("comment")
        tags = [part.replace("#", "") for part in comment.split() if part.__contains__("#")]
        valid_tags = []

        for tag in tags:
            tag = re.sub(r"[\s.,\?\!\;\:\'\"\(\)]*", "", tag)
            try:
                tag_object = CommentTag.objects.get(slug=tag)
                tag_in_comment = r"#" + tag + "(?=[\s.,\?\!\;\:\'\"\(\)]|$)"
                comment = re.sub(r"%s" % tag_in_comment, tag_object.html, comment)
                tag not in valid_tags and valid_tags.append(tag)
            except CommentTag.DoesNotExist:
                # If tag is invalid, don't pick it up
                pass

        return comment, valid_tags
