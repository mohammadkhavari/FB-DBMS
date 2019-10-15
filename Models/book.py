from .model import Model

class Book(Model):
    attributes_options = {
        "ISBN": {"exact": 20, "unique": True, "indexed": True, "index_file": "Data/Book/BookISBNIndex.txt", "required": True},
        "BookName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "Data/Book/BookTitleIndex.txt", "required": True},
        "Authors": {"upperbound": 200, "indexed": True, "index_file": "Data/Book/BookAuthorsIndex.txt", "required": True},
        "Publisher": {"upperbound": 200, "indexed": False, "required": True,},
        "Subjects": {"upperbound": 100, "indexed": False, "required": True, "indexed": True, "index_file": "Data/Book/BookSubjectsIndex.txt"},
        "PublishedYear": {"exact": 4, "indexed": False, "required": True, "indexed": True, "index_file": "Data/Book/BookYearIndex.txt"},
        "PageNo": {"upperbound": 4, "indexed": False, "required": True},
    }
    data_file = 'Data/Book/books.txt'
    query_attr = 'ISBN'

    def __str__(self):
        return f'ISBN:{self.ISBN} , BookName:{self.BookName} , Authors:{self.Authors} , Publisher:{self.Publisher} , Subjects:{self.Subjects} , PublishedYear:{self.PublishedYear} , PageNo:{self.PageNo}'
