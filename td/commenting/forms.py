from django import forms

from django_comments.forms import CommentForm


class CommentFormWithTags(CommentForm):
    tags = forms.CharField(max_length=300, required=False)

    def get_comment_create_data(self):
        data = super(CommentFormWithTags, self).get_comment_create_data()
        data["tags"] = self.cleaned_data["tags"]
        return data
