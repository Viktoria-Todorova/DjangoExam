from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Catalog(models.Model):
    # class Status(models.TextChoices):
    #     STARTED = 'Started', 'Started'
    #     COMPLETED = 'Completed', 'Completed'
    #     UNREAD = 'Unread', 'Unread'

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
    # status = models.TextField(choices=Status.choices, default=Status.UNREAD)
    genre = models.TextField(choices=Genre.choices, default=Genre.NONE)
    name_of_series = models.CharField(max_length=100, null=True, blank=True) #todo ?if to keep
    quantity = models.IntegerField(null=True, blank=True,default=1)

    def __str__(self):
        return f"{self.title} by {self.writer}"



class Reader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    # borrowed_book = models.ManyToManyField(Catalog, blank=True)
    # borrowing_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def currently_borrowed_books(self):
        """Get all books currently borrowed by this reader"""
        return self.borrowed_set.filter(return_date__isnull=True)

    def borrowing_history(self):
        """Get all borrowing records for this reader"""
        return self.borrowed_set.all().order_by('-borrow_date')




class Borrowed(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.reader} borrowed {self.book} on {self.borrow_date.date()}"

    #check if book is overdue


class Review(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reader} rated {self.book} - {self.rating}/5"
