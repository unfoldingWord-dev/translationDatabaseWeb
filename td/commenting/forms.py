from django import forms
from django.core.exceptions import ObjectDoesNotExist

from django_comments.forms import CommentForm

from td.models import WARegion, Country, Language
from td.tracking.models import Charter, Event


class CommentFormWithTags(CommentForm):
    # tags = forms.CharField(max_length=300, required=False)

    def get_comment_create_data(self):
        data = super(CommentFormWithTags, self).get_comment_create_data()
        # data["tags"] = self.extract_tags(data.get("comment"))
        # data["comment"], data["tags"] = self.convert_hashtags_to_links(data.get("comment"))
        print "*** CommentFormWithTags.get_comment_create_data():", data
        return data
    
    def get_comment_object_and_tags(self):
        data = self.get_comment_create_data()
        # tags = data.pop("tags")

        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        CommentModel = self.get_comment_model()
        new = CommentModel(**data)
        new = self.check_for_duplicate_comment(new)
        # return new, tags
        return new

    # @staticmethod
    # def extract_tags(s):
    #     return [part[1:] for part in s.split() if part.startswith('#')]

    # def convert_hashtags_to_links(self, comment):
    #     tags = [part[1:] for part in comment.split() if part.startswith('#')]
    #     # tags = ["r:southasia", "c:uk", "l:en", "ch:en", "ev:en:1"]
    #     for tag in tags:
    #         # tag = "r:southasia"
    #         print "\n*** processing tag", tag
    #
    #         split_tag = tag.lower().split(":")
    #         # split_tag = ["r", "southasia"]
    #
    #         if len(split_tag) > 2:
    #             model = self.get_model_from_tag(split_tag[0], split_tag[1], split_tag[2])
    #         elif len(split_tag) > 1:
    #             model = self.get_model_from_tag(split_tag[0], split_tag[1])
    #         else:
    #             print "!!! Invalid split_tag", split_tag
    #             model = None
    #         print "*** Model returned is ", model
    #
    #         if model:
    #             pass
    #         else:
    #             tags.remove(tag)
    #
    #     return comment, tags

    # @staticmethod
    # def get_model_from_tag(obj, term_1, term_2=None):
    #     print "*** get_model_from_tag()", obj, term_1, term_2
    #     try:
    #         mapping = {
    #             "r": WARegion.objects.get(slug__iexact=term_1),
    #             "c": Country.objects.get(code__iexact=term_1),
    #             "l": Language.objects.get(code__iexact=term_1),
    #             "ch": Charter.objects.get(language__code__iexact=term_1),
    #             "ev": Event.objects.get(charter__language__code__iexact=term_1, number=term_2),
    #         }
    #         model = mapping.get(obj, None)
    #         if model:
    #             instance = model.objects.get(slug__iexact=term_1) if obj == "r" else\
    #                 model.objects.get(code__iexact=term_1) if (obj == "c" or obj == "l") else\
    #                 model.objects.get(language__code__iexact=term_1) if obj == "ch" else \
    #                 model.objects.get(c)
    #     except ObjectDoesNotExist:
    #         print "!!! OBJECT DOES NOT EXIST", obj, term_1, term_2
    #         model = None
    #
    #     return model
