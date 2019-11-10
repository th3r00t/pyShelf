from django.db import models

# Create your models here.


class books(models.Model):
    """
    pyShelfs Book Database class
    :param title: Book title
    :param author: Author
    :param categories: Categories <-- Not implemented
    :param cover: Cover image BinaryField
    :param pages: # of pages <-- Not implemented
    :param progress: Reader percentage <-- Not implented
    :param file_name: Path to book
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    categories = models.CharField(max_length=255, blank=True)
    cover = models.BinaryField(blank=True, editable=True)
    pages = models.IntegerField(blank=True)
    progress = models.IntegerField(blank=True)
    file_name = models.CharField(max_length=255, blank=False)
