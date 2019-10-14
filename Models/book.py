class Book():
    __attributes_options = {
        "ISBN": {"exact": 20, "unique": True, "indexed": True, "index_file": "Data/BookISBNIndex.txt", "required": True},
        "BookName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "Data/BookTitleIndex.txt", "required": True},
        "Authors": {"upperbound": 200, "indexed": True, "index_file": "Data/BookAuthorsIndex.txt", "required": True},
        "Publisher": {"upperbound": 200, "indexed": False, "required": True},
        "Subjects": {"upperbound": 100, "indexed": False, "required": True},
        "PublishedYear": {"exact": 4, "indexed": False, "required": True},
        "PageNo": {"upperbound": 4, "indexed": False, "required": True},
    }

    def __init__(self, data, _id=None):
        for key, val in data.items():
            self.__dict__[key] = val
        self._id = _id

    def __save(self):
        validation_status = self.__validate(new_record=True)
        if(validation_status != 'valid'):
            print('Validation Failed: ', validation_status)
            return
        # New Record (append)
        record_id = len(open("Data/books.txt").read().splitlines()) + 1
        self._id = record_id
        open("Data/books.txt", 'a').write(f'{self._id}-{self}\n')
        # __save index
        for attr, rules in Book.__attributes_options.items():
            if rules['indexed']:
                self.save_index(attr)

    def __update(self, attr, val):
        prev_val = self.__dict__[attr]
        self.__dict__[attr] = val
        validation_status = self.__validate(new_record=False)
        if(validation_status != 'valid'):
            print('Validation Failed: ', validation_status)
            return
        # Existing Record (overwrite)
        try:
            lines = open('Data/books.txt').read().splitlines()
            lines[self._id - 1] = f'{self._id}-{self}'
            open('Data/books.txt', 'w').write('\n'.join(lines)+'\n')
        except Exception as err:
            print('An error occured in saving:', err)

        if Book.__attributes_options[attr]["indexed"]:
            index_file = Book.__attributes_options[attr]["index_file"]
            # __save current index
            for index in val.split(','):
                print('saving current index')
            # remove previous index
            for index in prev_val.split(','):
                print('removing previous index')

    def __remove(self):
        try:
            lines = open('Data/books.txt').read().splitlines()
            lines[self._id - 1] = f'{self._id}-removed'
            open('Data/books.txt', 'w').write('\n'.join(lines)+'\n')
            # removing indexes
            for attr, rules in Book.__attributes_options.items():
                if rules['indexed']:
                    self.__remove_index(attr)
        except Exception as err:
            print('An error occured in saving:', err)

    def __validate(self, new_record):
        for attr, rules in Book.__attributes_options.items():
            if 'required' in rules.keys() and attr not in self.__dict__.keys():
                return f'book should have {attr.lower()}'
            if 'exact' in rules.keys() and len(self.__dict__[attr]) != rules["exact"]:
                return f'{attr.lower()} should containt exactly {rules["exact"]} characters'
            if 'upperbound' in rules.keys() and len(self.__dict__[attr]) > rules['upperbound']:
                return f'{attr.lower()} should containt at most {rules["upperbound"]} characters'
            if 'lowerbound' in rules.keys() and len(self.__dict__[attr]) < rules["lowerbound"]:
                return f'{attr.lower()} should containt at least {rules["lowerbound"]} characters'
            if new_record and 'unique' in rules.keys() and rules['unique'] and Book.search_handler(attr, self.__dict__[attr]):
                return f'a book with this {attr.lower()} already exists'
        return 'valid'

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
        new_book.__save()

    # remove book
    @classmethod
    def remove(cls, isbn):
        result = cls.search_handler('ISBN', isbn)
        if not result:
            print('nothing found')
            return
        book = result[0]
        book.__remove()

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
        book.__update(attr, val)

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
                if line.split('-')[1] == 'removed\n':
                    continue
                attrs_str = '-'.join(line[:-1].split('-')[1:])
                attrs = cls.parse_attributes(attrs_str)
                if val in attrs[attr]:
                    results.append(cls(data=attrs, _id=num))
        return results

     # using indexes
    @classmethod
    def indexed_search(cls, attr, val):
        index_file = cls.__attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()    
        result = cls.binary_search(lines, val)
        results = []
        if result['exist']:
            vals = lines[result['line']].split(':')[1].split('-')
            vals = [int(val) for val in vals]
            lines = open('Data/books.txt').read().splitlines()
            for val in vals:
                attrs_str = '-'.join(lines[val - 1].split('-')[1:])
                attrs = cls.parse_attributes(attrs_str)
                results.append(cls(data=attrs, _id=val))
        return results

    def save_index(self, attr):
        val = self.__dict__[attr]
        vals = val.split(',')
        index_file = Book.__attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()
        for val in vals:       
            result = Book.binary_search(lines, val)
            if result['exist']:
                ids = lines[result['line']].split(':')[1].split('-')
                ids.append(self._id)
                lines[result['line']] = lines[result['line']].split(':')[0] + ':' + '-'.join(vals)
            else:
                new_line = f'{val}:{self._id}'
                lines = lines[0:result['line']] + [new_line] + lines[result['line']:]
        open(index_file, 'w').write('\n'.join(lines)+'\n')


    def __remove_index(self, attr):
        val = self.__dict__[attr]
        vals = val.split(',')
        index_file = Book.__attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()
        for val in vals:
            result = Book.binary_search(lines, val)
            if result['exist']:
                ids = lines[result['line']].split(':')[1].split('-')
                ids.remove(self._id)
                if not ids:
                    lines.__delitem__[result['line']]           
                else:
                    lines[result['line']] = lines[result['line']].split(':')[0] + ':' + '-'.join(ids)
        if not lines:
            open(index_file, 'w').write('')
        else:               
            open(index_file, 'w').write('\n'.join(lines)+'\n')            
                            
    @staticmethod
    def binary_search(lines, target):
        lo, hi = 0, len(lines) - 1
        while lo <= hi:
            mid = lo + (hi - lo)//2
            current = lines[mid].split(':')[0]
            if current == target:
                return {'line': mid, 'exist': True}
            elif current < target:
                lo = mid + 1
            else:
                hi = mid - 1

        # if were not returned yet we should return the neerest position
        lo, hi = 0, len(lines) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            current = lines[mid].split(':')[0]
            if (current > target):
                hi = mid
            else:
                lo = mid + 1
        return {'line': lo, 'exist': False}
