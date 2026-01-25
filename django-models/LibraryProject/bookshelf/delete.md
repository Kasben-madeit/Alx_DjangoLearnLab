from bookshelf.models import Book
>>> Book.objects.get(publication_year=1949)
<Book: Book object (2)>
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.get(publication_year=1949)


# bookshelf.models.Book.DoesNotExist: Book matching query does not exist.