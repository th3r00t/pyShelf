from django.contrib.postgres.search import SearchVector
from django.db import models

# Create your models here.


class Books(models.Model):
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

    class Meta:
        db_table = "books"

    def __str__(self):
        return self.title

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True)
    categories = models.CharField(max_length=255, null=True)
    cover = models.BinaryField(null=True, editable=True)
    pages = models.IntegerField(null=True)
    progress = models.IntegerField(null=True)
    file_name = models.CharField(max_length=255, null=False)

    def generic_search(self, query):
        try:
            results = Books.objects.annotate(
                search=SearchVector("title", "file_name", "author"),
            ).filter(search=query)
        except Exception as e:
            raise
        return results


class Collections(models.Model):
    class Meta:
        db_table = "collections"

    def __str__(self):
        return self.collection

    collection = models.CharField(max_length=255)
    book_id = models.ForeignKey(Books, on_delete=models.PROTECT)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse("model-detail-view", args=[str(self.id)])

    def generic_search(self, query):
        try:
            results = Books.objects.annotate(search=SearchVector("collection"),).filter(
                search=query
            )
        except Exception as e:
            raise
        return results


class Navigation(models.Model):
    """
    pyShelfs Navigation Database class
    :param title: Link Text
    :param link: Link link :)
    :param category: Where in the nav tree do I belong
    :param parent_id: This link is a sub link of link with id of me
    :param alt: Alternate text of link
    :param type: Web link, or Socket link which will be expected to act on \
    the link, and the action defined in socket
    :param socket: if a Socket link define socket here
    """

    class Meta:
        db_table = "navigation"

    def __str__(self):
        return self.title

    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    parent_id = models.IntegerField(null=True, editable=True)
    alt = models.CharField(max_length=255, null=True)
    type = models.IntegerField(null=True)
    socket = models.CharField(max_length=255, null=False)

    def generic_search(self, query):
        try:
            results = Navigation.objects.annotate(
                search=SearchVector("title", "parent_id", "category"),
            ).filter(search=query)
        except Exception as e:
            raise
        return results
