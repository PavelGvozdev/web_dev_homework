from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Author(models.Model):
  full_name = models.TextField()
  birth_year = models.SmallIntegerField()
  country = models.CharField(max_length=2)

  def __str__(self):
    return self.full_name

class Book(models.Model):
  ISBN = models.CharField(max_length=13)
  title = models.TextField()
  description = models.TextField()
  year_release = models.SmallIntegerField()
  author = models.ForeignKey("p_library.Author", on_delete=models.CASCADE, verbose_name=_("Автор"), related_name="book_author")
  publisher = models.ForeignKey("p_library.Publisher", on_delete=models.CASCADE, verbose_name=_("Издатель"), related_name="book_publisher", null=True)
  copy_count = models.SmallIntegerField(default=1)
  price = models.DecimalField(max_digits=7, decimal_places=2)

  def __str__(self):
    return self.title

class Publisher(models.Model):
  title = models.TextField()
  year_of_foundation = models.SmallIntegerField()
  address = models.TextField()
  books = models.ForeignKey("p_library.Book", on_delete=models.CASCADE, verbose_name=_("Книги"), related_name="publisher_book", null=True)

  def __str__(self):
    return self.title
