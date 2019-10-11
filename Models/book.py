class Book():
    def __init__(self, data, _id = None):
        for key, val in data.items():
            self.__dict__[key] = val
        self._id = _id

    def save(self):
        #if id was None add a new line else edit existing line
        pass

        #validate a
    def validation(self):
        if len(self.ISBN) != 20:
            raise ValueError('A very specific bad thing happened.')
    
    def update_data(self, new_data):
        for key, val in new_data.items():
            self.__dict__[key] = val

    #return a represntable string form for instance
    def __str__(self):
        return "not implemnted"
    
    # returns a dict contains book attributes and values
    @staticmethod
    def deserialize(parameter_list):
        pass

    # reduce query and calll the target function
    @staticmethod
    def query(query_type, body):
        print(query_type, body)

    # add new book
    @staticmethod
    def add(book_str):
        a = Book()

    # remove book
    @staticmethod
    def remove(isbn):
        pass

    # updates a book 
    @staticmethod
    def update():
        pass

    # returns a book object or null
    @staticmethod
    def find():
        pass

