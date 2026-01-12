from django.db import models

# Create your models here.

class Catalog(models.Model):
    class Status(models.TextChoices):
        STARTED = 'Started', 'Started'
        COMPLETED = 'Completed', 'Completed'
        UNREAD = 'Unread', 'Unread'

    class Genre(models.TextChoices):
        FANTASY = "FANTASY", "Fantasy"
        NOVEL = "NOVEL", "Novel"
        SCIENCE_FICTION = "SCIENCE_FICTION", "Science Fiction"
        THRILLER = "THRILLER", "Thriller"
        CRIME = "CRIME", "Crime"
        ROMANCE = "ROMANCE", "Romance"
        HORROR = "HORROR", "Horror"
        MYSTERY = "MYSTERY", "Mystery"
        DRAMA = "DRAMA", "Drama"
        BIOGRAPHY_MEMOIR = "BIOGRAPHY_MEMOIR", "Biography Memoir"
        SELF_IMPROVEMENT = "SELF_IMPROVEMENT", "Self Improvement"
        BULGARIAN_CLASSICS = "BULGARIAN_CLASSICS", "Bulgarian Classics"
        POETRY = "POETRY", "Poetry"
        LGBT_LITERATURE = "LGBT_LITERATURE", "LGBT Literature"
        TEXTBOOK = "TEXTBOOK", "Textbook"
        ESOTERIC = "ESOTERIC", "Esoteric"
        COOKBOOKS = "COOKBOOKS", "Cookbooks"
        ADVENTURE = "ADVENTURE", "Adventure"
        SHORT_STORIES = "SHORT_STORIES", "Short Stories"
        ANTHOLOGY = "ANTHOLOGY", "Anthology"
        POPULAR_SCIENCE = "POPULAR_SCIENCE", "Popular Science"
        NONE = "NONE", "None"
        
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    status = models.TextField(choices=Status.choices, default=Status.UNREAD)
    genre = models.TextField(choices=Genre.choices, default=Genre.NONE)
    grade =...