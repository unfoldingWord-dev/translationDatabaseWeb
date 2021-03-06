from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from td.models import Language


NAME_TO_PROPERTY = {
    "name": "ln",
    "code": "lc",
    "direction": "ld",
    "country": "cc",
    "region": "lr"
}


def transform_country_data(data):
    tree = {"name": "World", "parent": None, "children": []}
    for code in data:
        datum = {
            "name": data[code]["obj"].name,
            "parent": "World",
            "children": [],
            "hasGatewayLanguages": len(data[code]["gateways"]) > 1,
            "detailUrl": reverse("country_detail", args=[data[code]["obj"].pk])
        }
        for gateway in data[code]["gateways"]:
            if gateway == "n/a":
                name = "No Gateway"
            else:
                name = data[code]["gateways"][gateway][0].gateway_language.name
            gdatum = {
                "name": name,
                "parent": data[code]["obj"].name,
                "children": [
                    {
                        "name": l.name,
                        "detailUrl": reverse("language_detail", args=[l.pk]),
                        "parent": name,
                        "children": []
                    }
                    for l in data[code]["gateways"][gateway]
                ],
                "notGatewayLanguage": gateway == "n/a"
            }
            datum["children"].append(gdatum)
        tree["children"].append(datum)
    return tree

"""
tree = {
    "name": "Root",
    "parent": None,
    "children": [
        {"name": "", "parent": "Root", "children": []},
        {"name": "", "parent": "Root", "children": []},
        {"name": "", "parent": "Root", "children": []},
    ]
}
"""


@python_2_unicode_compatible
class Media(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uw_media'
        verbose_name_plural = "Media"


@python_2_unicode_compatible
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    extra_data = JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uw_publisher'


@python_2_unicode_compatible
class Title(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    extra_data = JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uw_title'


@python_2_unicode_compatible
class Resource(models.Model):
    title = models.ForeignKey(Title, related_name="versions")
    language = models.ForeignKey(Language, related_name="resources")
    medias = models.ManyToManyField(Media, blank=True, verbose_name="Media", db_table='uw_resource_medias')
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    published_flag = models.BooleanField(default=True, db_index=True, blank=True)
    published_date = models.DateField(default=None, null=True, blank=True, db_index=True)
    copyright_year = models.IntegerField(default=None, null=True, blank=True, db_index=True, verbose_name="copyright")
    extra_data = JSONField(default=dict)

    def the_publisher(self):
        return self.publisher or self.title.publisher

    def __str__(self):
        return "{0} in {1}".format(str(self.title), str(self.language))

    class Meta:
        db_table = 'uw_resource'
        unique_together = ("title", "language")


@python_2_unicode_compatible
class Questionnaire(models.Model):
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    questions = JSONField()
    field_mapping = JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @property
    def language_data(self):
        return {NAME_TO_PROPERTY.get(field_name): int(qid) for qid, field_name in self.field_mapping.items()}

    @property
    def grouped_questions(self):
        group = []
        ret = []
        for q in self.questions:
            if q["depends_on"] is None and len(group) != 0:
                ret.append(group)
                group = [q]
            else:
                group.append(q)
        ret.append(group)
        return ret
