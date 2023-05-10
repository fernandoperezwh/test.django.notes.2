# python packages
import uuid
# django packages
from django.db import models


# Create your models here.
class Blogs(models.Model):
    folio = models.UUIDField(
        verbose_name='Folio',
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    title = models.CharField(
        verbose_name='title',
        max_length=255,
    )

    content = models.TextField(
        verbose_name='content',
        blank=True,
        null=True,
    )

    published = models.BooleanField(
        verbose_name='is it published?',
        default=False,
    )
