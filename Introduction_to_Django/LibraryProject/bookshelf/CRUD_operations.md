# Create
from bookshelf.models import Book
 
 book= Book.objects.create(title='1984',author='George Orwell',publication_year=1949)

 # Retrieve
  Book.objects.all()
# <QuerySet [<Book: Book object (1)>, # <Book: Book object (2)>]>

# Update
>>> Book.objects.get(title='1984')
<Book: Book object (2)>
>>> book.title = 'Nineteen Eighty-Four'
>>> book.save()

# Delete
>>> Book.objects.get(publication_year=1949)
<Book: Book object (2)>
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.get(publication_year=1949)

# bookshelf.models.Book.DoesNotExist: Book matching query does not exist.