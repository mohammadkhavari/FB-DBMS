class Model():
    attributes_options = {
    }
    data_file = ''
    query_attr = ''

    def __init__(self, data, _id=None):
        for key, val in data.items():
            self.__dict__[key] = val
        self._id = _id

    def __save(self):
        validation_status = self.validate(to_update=False)
        if(validation_status != 'valid'):
            print('Validation Failed: ', validation_status)
            return
        # New Record (append)
        record_id = len(open(self.data_file).read().splitlines()) + 1
        self._id = record_id
        open(self.data_file, 'a').write(f'{self._id}-{self}\n')
        # __save index
        for attr, rules in self.__class__.attributes_options.items():
            if rules['indexed']:
                self.__save_index(attr)

    def __update(self, attr, val):
        prev_val = self.__dict__[attr]
        self.__dict__[attr] = val
        validation_status = self.validate(to_update=True)
        if(validation_status != 'valid'):
            print('Validation Failed: ', validation_status)
            return
        # Existing Record (overwrite)
        try:
            lines = open(self.data_file).read().splitlines()
            lines[self._id - 1] = f'{self._id}-{self}'
            open(self.data_file, 'w').write('\n'.join(lines)+'\n')
        except Exception as err:
            print('An error occured in saving:', err)

        if self.__class__.attributes_options[attr]["indexed"]:
            # __save current index
            self.__save_index(attr)
            # remove previous index
            self.__remove_index(attr, val = prev_val)

    def __remove(self):
        try:
            lines = open(self.data_file).read().splitlines()
            lines[self._id - 1] = f'{self._id}-removed'
            open(self.data_file, 'w').write('\n'.join(lines)+'\n')
            # removing indexes
            for attr, rules in self.__class__.attributes_options.items():
                if rules['indexed']:
                    self.__remove_index(attr)
        except Exception as err:
            print('An error occured in saving:', err)

    def validate(self, to_update):
        for attr, rules in self.__class__.attributes_options.items():
            if 'required' in rules.keys() and rules['required'] and attr not in self.__dict__.keys():
                return f'{self.__class__.__name__} should have {attr.lower()}'
            if 'numeric' in rules.keys() and rules['numeric'] and not self.__dict__[attr].isnumeric():
                return f'{attr.lower()} should be numeric'
            if 'exact' in rules.keys() and len(self.__dict__[attr]) != rules["exact"]:
                return f'{attr.lower()} should containt exactly {rules["exact"]} characters'
            if 'upperbound' in rules.keys() and len(self.__dict__[attr]) > rules['upperbound']:
                return f'{attr.lower()} should containt at most {rules["upperbound"]} characters'
            if 'lowerbound' in rules.keys() and len(self.__dict__[attr]) < rules["lowerbound"]:
                return f'{attr.lower()} should containt at least {rules["lowerbound"]} characters'
            if not to_update and 'unique' in rules.keys() and rules['unique'] and self.__class__.search_handler(attr, self.__dict__[attr]):
                return f'a {self.__class__.__name__} with this {attr.lower()} already exists'
        return 'valid'


    # returns a dict contains model attributes and values (used for quick parse in search and creating instance in updating and saving record)
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
        elif query_type == 'partial_find':
            cls.find(body, exact = False)
        elif query_type == 'update':
            cls.update(body)
        elif query_type == 'remove':
            cls.remove(body)
        else:  # throw exepction
            print("Invalid Query")

    # add new model
    @classmethod
    def add(cls, model_attrs):
        model_attrs = cls.parse_attributes(model_attrs)
        new_model = cls(data=model_attrs)
        new_model.__save()

    # remove model
    @classmethod
    def remove(cls, query_value):
        result = cls.search_handler(cls.query_attr, query_value)
        if not result:
            print('nothing found')
            return
        model = result[0]
        model.__remove()

    # updates a model
    @classmethod
    def update(cls, body):
        query_value, new_data = body.split(' set ')
        attr, val = new_data.split(' to ')
        result = cls.search_handler(cls.query_attr, query_value)
        if result == []:
            print("nothing found")
            return
        model = result[0]
        model.__update(attr, val)

    # returns a model object or null
    @classmethod
    def find(cls, body, exact = True):
        val, attr = body.split(' by ')
        if not exact:
            results = cls.non_indexed_search(attr, val, exact=False)
        else:
            results = cls.search_handler(attr, val)
        if len(results) == 0:
            print('Nothing Found!')
        else:
            for num, record in enumerate(results, start=1):
                print(f'{num}-{record}')

    @classmethod
    def search_handler(cls, attr, val):
        results = []
        if cls.attributes_options[attr]['indexed']:
            results = cls.indexed_search(attr, val)
        else:
            results = cls.non_indexed_search(attr, val)
        return results

    # find by any attributes WITHOUT INDEXING
    @classmethod
    def non_indexed_search(cls, attr, val, exact = True):
        results = []
        with open(cls.data_file, "r") as file:
            for num, line in enumerate(file, start=1):
                if line.split('-')[1] == 'removed\n':
                    continue
                attrs_str = '-'.join(line[:-1].split('-')[1:])
                attrs = cls.parse_attributes(attrs_str)
                if exact:
                    if val == attrs[attr]:
                        results.append(cls(data=attrs, _id=num))
                else:
                    if val in attrs[attr]:
                        results.append(cls(data=attrs, _id=num))
        return results

     # using indexes
    @classmethod
    def indexed_search(cls, attr, val):
        index_file = cls.attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()    
        result = cls.binary_search(lines, val)
        results = []
        if result['exist']:
            vals = lines[result['line']].split(':')[1].split('-')
            vals = [int(val) for val in vals]
            lines = open(cls.data_file).read().splitlines()
            for val in vals:
                attrs_str = '-'.join(lines[val - 1].split('-')[1:])
                attrs = cls.parse_attributes(attrs_str)
                results.append(cls(data=attrs, _id=val))
        return results

    def __save_index(self, attr):
        val = self.__dict__[attr]
        vals = val.split(',')
        index_file = self.__class__.attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()
        for val in vals:       
            result = self.__class__.binary_search(lines, val)
            if result['exist']:
                ids = lines[result['line']].split(':')[1].split('-')
                ids.append(str(self._id))
                lines[result['line']] = lines[result['line']].split(':')[0] + ':' + '-'.join(ids)
            else:
                new_line = f'{val}:{self._id}'
                lines = lines[0:result['line']] + [new_line] + lines[result['line']:]
        open(index_file, 'w').write('\n'.join(lines)+'\n')


    def __remove_index(self, attr, val=None):
        if not val:
            val = self.__dict__[attr]

        vals = val.split(',')

        index_file = self.__class__.attributes_options[attr]["index_file"]
        lines = open(index_file).read().splitlines()
        for val in vals:
            result = self.__class__.binary_search(lines, val)
            if result['exist']:
                ids = lines[result['line']].split(':')[1].split('-')
                ids.remove(str(self._id))
                if not ids:
                    lines.__delitem__(result['line'])           
                else:
                    lines[result['line']] = lines[result['line']].split(':')[0] + ':' + '-'.join(ids)
        if not lines:
            open(index_file, 'w').write('')
        else:               
            open(index_file, 'w').write('\n'.join(lines)+'\n')            
    
    @classmethod
    def reset(cls):
        files = [cls.data_file]
        for attr, rules in cls.attributes_options.items():
            if rules['indexed']:
                files.append(rules['index_file'])
        for file in files:
            open(file, 'w').write('')


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
        lo, hi = 0, len(lines)
        while lo < hi:
            mid = (lo + hi) // 2
            current = lines[mid].split(':')[0]
            if (current > target):
                hi = mid
            else:
                lo = mid + 1
        return {'line': lo, 'exist': False}
