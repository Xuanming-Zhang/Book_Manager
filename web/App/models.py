from django.db import models

# Create your models here.
class Books(models.Model):

    bookID = models.IntegerField(primary_key=True)
    title = models.TextField()
    authors = models.TextField()
    average_rating = models.FloatField()
    publication_date = models.TextField()
    publisher = models.TextField()

    class Meta:
        db_table = 'books'

class Focus(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    book_id = models.IntegerField()

    class Meta:
        db_table = 'focus'