class Book():
    def __init__(self, data, _id=None):
        for key, val in data.items():
            self.__dict__[key] = val
        self._id = _id

    def save(self):
        validation_status = self.__validate()
        if(validation_status != 'valid'):
            print('Validation Failed:', validation_status)
            return

        if self._id == None:
            # New Record (append)
            with open("Data/books.txt", "a+") as file:
                file.seek(0)
                record_id = len(file.readlines()) + 1
                file.write(f'{record_id}-{self}\n')

        else:
            # Existing Record (overwrite)
            pass

    def remove(self):
        pass

    def __save_indexes(self):
        pass
        # validate a

    def __validate(self):
        if len(self.ISBN) != 2:
            return 'ISBN should containt 20 chars'
        # if le(self.)
        return 'valid'

    def update_data(self, new_data):
        for key, val in new_data.items():
            self.__dict__[key] = val

    # return a represntable string form for instance
    def __str__(self):
        return f'BookName:{self.BookName} , Authors:{self.Authors} , Publisher:{self.Publisher} , Subjects:{self.Subjects} , PublishedYear:{self.PublishedYear} , PageNo:{self.PageNo}'

    # returns a dict contains book attributes and values (used for quick parse in search and creating instance in updating and saving record)
    @staticmethod
    def parse_attributes(attrs_str):
        attrs = attrs_str.split(' , ')
        # attrs_dict = dict()
        # for attr in attrs:
        #     key, val = attr.split(':')[0], attr.split(':')[1]
        #     attrs_dict[key] = val
        return {attr.split(':')[0]: attr.split(':')[1] for attr in attrs}

    # reduce query and call the target function
    @classmethod
    def query(cls, query_type, body):
        if query_type == 'add':
            cls.add(body)
        elif query_type == 'find':
            cls.find(body)
        elif query_type == 'update':
            cls.update(body)
        elif query_type == 'remove':
            cls.remove(body)
        else:  # throw exepction
            pass

    # add new book
    @classmethod
    def add(cls, book_attrs):
        book_attrs = cls.parse_attributes(book_attrs)
        new_book = cls(data=book_attrs)
        new_book.save()

    # remove book
    @classmethod
    def remove(isbn):
        pass

    # updates a book
    @classmethod
    def update():
        pass

    # returns a book object or null
    @classmethod
    def find(cls, body):
        attr, val = body.split(' by ')[1], body.split(' by ')[0]
        results = []
        if attr == 'BookName':
            results = cls.find_by_name(val)
        elif attr == 'ISBN':
            results = cls.find_by_isbn(val)
        elif attr == 'Authors':
            results = cls.find_by_isbn(val)
        else:
            results = cls.implicit_find(attr, val)

        if len(results) == 0:
            print('Nothing Founded!')
        else:
            for num, record in enumerate(results, start=1):
                print(f'{num}-{record}')

    # find by any attributes WITHOUT INDEXING
    @classmethod
    def implicit_find(cls, attr, val):
        results = []
        with open("Data/books.txt", "r") as file:
            for num, line in enumerate(file, start=1):
                attrs_str = '-'.join(line[:-1].split('-')[1:])
                attrs = cls.parse_attributes(attrs_str)
                if val in attrs[attr]:
                    results.append(cls(data=attrs, _id=num))
        return results

     # using indexes
    @classmethod
    def find_by_name(cls, name):
        pass

    # using indexes
    @classmethod
    def find_by_isbn(cls, isbn):
        pass

    # using indexes
    @classmethod
    def find_by_authors(cls, author):
        pass
