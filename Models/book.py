class Book():
    __attributes_options = {
        "ISBN": {"exact": 20, "unique": True, "indexed": True, "index_file": "BookISBNIndex.txt"},
        "BookName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "BookTitleIndex.txt"},
        "Authors": {"upperbound": 200, "indexed": True, "index_file": "BookAuthorsIndex.txt"},
        "Publisher": {"upperbound": 200, "indexed": False},
        "Subjects": {"upperbound": 100, "indexed": False, },
        "PublishedYear": {"exact": 4, "indexed": False, },
        "PageNo": {"upperbound": 4, "indexed": False, },
    }

    def __init__(self, data, _id=None):
        for key, val in data.items():
            self.__dict__[key] = val
        self._id = _id

    def save(self):
        new_record = (self._id == None)
        validation_status = self.__validate(new_record)
        if(validation_status != 'valid'):
            print('Validation Failed: ', validation_status)
            return

        if new_record:
            # New Record (append)
            with open("Data/books.txt", "a+") as file:
                file.seek(0)
                record_id = len(file.readlines()) + 1
                file.write(f'{record_id}-{self}\n')

        else:
            # Existing Record (overwrite)
            lines = open('Data/books.txt').read().splitlines()
            lines[self._id - 1] = f'{self._id}-{self}'
            open('Data/books.txt', 'w').write('\n'.join(lines))

    def remove(self):
        pass

    def __save_indexes(self):
        pass

    def __validate(self, new_record):
        for attr, rules in Book.__attributes_options.items():
            if 'exact' in rules.keys() and len(self.__dict__[attr]) != rules["exact"]:
                return f'{attr.lower()} should containt exactly {rules["exact"]} characters'
            if 'upperbound' in rules.keys() and len(self.__dict__[attr]) > rules['upperbound']:
                return f'{attr.lower()} should containt at most {rules["upperbound"]} characters'
            if 'lowerbound' in rules.keys() and len(self.__dict__[attr]) < rules["lowerbound"]:
                return f'{attr.lower()} should containt at least {rules["lowerbound"]} characters'
            if new_record and 'unique' in rules.keys() and rules['unique'] and Book.search_handler(attr, self.__dict__[attr]):
                return f'a book with this {attr.lower()} already exists'
        return 'valid'

    def update_data(self, new_data):
        for key, val in new_data.items():
            self.__dict__[key] = val

    # return a represntable string form for instance
    def __str__(self):
        return f'ISBN:{self.ISBN} , BookName:{self.BookName} , Authors:{self.Authors} , Publisher:{self.Publisher} , Subjects:{self.Subjects} , PublishedYear:{self.PublishedYear} , PageNo:{self.PageNo}'

    # returns a dict contains book attributes and values (used for quick parse in search and creating instance in updating and saving record)
    @staticmethod
    def parse_attributes(attrs_str):
        attrs = attrs_str.split(' , ')
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
            print("Invalid Query")

    # add new book
    @classmethod
    def add(cls, book_attrs):
        book_attrs = cls.parse_attributes(book_attrs)
        new_book = cls(data=book_attrs)
        new_book.save()

    # remove book
    @classmethod
    def remove(cls, isbn):
        pass

    # updates a book
    @classmethod
    def update(cls, body):
        isbn, new_data = body.split(' set ')
        attr, val = new_data.split(' to ')
        result = cls.search_handler('ISBN', isbn)
        if result == []:
            print("nothing found")
            return
        book = result[0]
        book.update_data({attr: val})
        book.save()

    # returns a book object or null
    @classmethod
    def find(cls, body):
        val, attr = body.split(' by ')
        results = cls.search_handler(attr, val)
        if len(results) == 0:
            print('Nothing Founded!')
        else:
            for num, record in enumerate(results, start=1):
                print(f'{num}-{record}')

    @classmethod
    def search_handler(cls, attr, val):
        results = []
        if cls.__attributes_options[attr]['indexed']:
            results = cls.non_indexed_search(attr, val)
        else:
            results = cls.non_indexed_search(attr, val)
        return results

    # find by any attributes WITHOUT INDEXING
    @classmethod
    def non_indexed_search(cls, attr, val):
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
    def indexed_search(cls, attr, val):
        index_file = cls.__attributes_options[attr]["index_file"]
        return []
