from .model import Model
from .publisher import Publisher

class Book(Model):
    attributes_options = {
        "ISBN": {"exact": 20, "numeric":True, "unique": True, "indexed": True, "index_file": "Data/Book/BookISBNIndex.txt", "required": True},
        "BookName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "Data/Book/BookTitleIndex.txt", "required": True},
        "Authors": {"upperbound": 200, "indexed": True, "index_file": "Data/Book/BookAuthorsIndex.txt", "required": True},
        "Publisher": {"upperbound": 200, "indexed": False, "required": True,},
        "Subjects": {"upperbound": 100, "indexed": False, "required": True, "indexed": True, "index_file": "Data/Book/BookSubjectsIndex.txt"},
        "PublishedYear": {"exact": 4, "indexed": False, "required": True, "indexed": True, "index_file": "Data/Book/BookYearIndex.txt"},
        "PageNo": {"upperbound": 4, "numeric":True, "indexed": False, "required": True},
    }
    data_file = 'Data/Book/books.txt'
    query_attr = 'ISBN'

    def validate(self, to_update):
        if not to_update:    
            result = Publisher.search_handler("PubName", self.Publisher)
            if not result:
                return f'publisher {self.Publisher} is not registered to Publishers'
        return super().validate(to_update)
    
    @classmethod
    def print_all(cls):
        books = cls.non_indexed_search('ISBN', '', exact=False)
        for book in books:
            publisher = Publisher.search_handler('PubName', book.Publisher)
            if not publisher:
                pub_subjects = pub_address = 'no information!'
            else:
                pub_subjects, pub_address = publisher[0].SubjectsInterest, publisher[0].PubAddress
            print(f' ISBN : {book.ISBN} \n BookName : {book.BookName} \n Authors : {book.Authors} \n Publisher : {book.Publisher} \n Subjects : {book.Subjects} \n PublishedYear : {book.PublishedYear} \n PageNo : {book.PageNo} \n SubjectsInterest : {pub_subjects}\n PubAddress : {pub_address}\n---------------')

    def __str__(self):
        return f'ISBN:{self.ISBN} , BookName:{self.BookName} , Authors:{self.Authors} , Publisher:{self.Publisher} , Subjects:{self.Subjects} , PublishedYear:{self.PublishedYear} , PageNo:{self.PageNo}'
