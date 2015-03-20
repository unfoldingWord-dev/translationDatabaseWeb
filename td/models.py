from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AdditionalLanguage(models.Model):
    DIRECTION_CHOICES = (
        ("l", "ltr"),
        ("r", "rtl")
    )
    ietf_tag = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    two_letter = models.CharField(max_length=2, blank=True)
    three_letter = models.CharField(max_length=3, blank=True)
    native_name = models.CharField(max_length=100, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default="l")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def merge_code(self):
        return self.two_letter or self.three_letter or self.ietf_tag

    def merge_name(self):
        return self.native_name or self.common_name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(AdditionalLanguage, self).save(*args, **kwargs)

    def __str__(self):
        return self.ietf_tag

    class Meta:
        verbose_name = "Additional Language"
