>>> Book.objects.get(title='1984')
<Book: Book object (2)>
>>> book.title = 'Nineteen Eighty-Four'
>>> book.save()