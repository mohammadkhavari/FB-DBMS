# FileBasedLibrary

### Flexible File-Based-Data Manager with Python. (Configurable Model Scheme, Indexed Lookup)

---

## 1.DBMS Structure:

* Main:
Main Function handles the interactive input and pass queries to the right model handler

* Model Base Class:
To avoid reapiting code for each model and flexiblity. It Handles Queries and send them to the right handler, validate, saves, updates(data and its own indexes), removes(data and its own indexes), find(exact or partial, indexed) or non indexed) formats documents in string.
>**Indexes are always in sorted order (all mutations(update, save remove) respect the order and runs fast -> O(lon n)**)

>It contains classmethods to act as public library and also its private instance methos.

```python
attributes_options = {
}
data_file = ''   #file that saves whole records
query_attr = ''  #the attribute used in removing and updating
```

>and also configurable properties

* Attribute Options:
It's Possible to set rules for every attribute of Scheme in this configuration such as (upperbound, lowerbound, numeric, being uniqe, requiered). and set whether use indexes fo looking up by this attribute or not. (and also the index file location)

```python
class Publisher(Model):

    data_file = 'Data/Publisher/publishers.txt'

    query_attr = 'PubId'    

    attributes_options = {
        "PubId": {"exact": 6, "unique": True, "numeric": True, "indexed": True, "index_file": "Data/Publisher/PublisherPubIdIndex.txt", "required": True},
        "PubName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "Data/Publisher/PublisherNameIndex.txt", "required": True},
        "SubjectsInterest": {"upperbound": 200, "indexed": True, "index_file": "Data/Publisher/PublishesrSubjectsInterestIndex.txt", "required": True},
        "HeadName": {"upperbound": 100, "indexed": False, "required": True},
        "PubAddress": {"upperbound": 200, "indexed": False, "required": True},
        }
        .

```
>Code shows the publisher model configuration

* It's Possible to override Base Model functions, for example Book validation is overriden and Its Check the publisher registration.
```python
def validate(self, to_update):
        if not to_update:    
            result = Publisher.search_handler("PubName", self.Publisher)
            if not result:
                return f'publisher {self.Publisher} is not registered to Publishers'
        return super().validate(to_update)
```
>overrided validate on Book
---
## 2.User Guide:

## Input Exapmles are available in `input-test.txt`

- #### `--> reset` : 
>Clears saved data 
---
- #### `--> show all` : 
>Show all documents contain
---
- #### `--> add <model-name> [<attr:val1,val2>]` : 
>Creates new document and save it
---
- #### `--> update <model-name> <query_attr> set X to Y` :
> also removes previous indexes for changed attribute and add new vals
---
- #### `--> find <model-name> <val> by <attribute-name>` :
>Looks for the exact matching
---
- #### `--> partial_find <model-name> <val> by <attribute-name>` :
>Looks for the substring (doesn't use indexing)
---
- #### `--> remove <model-name> <<query_attr>>` 
> to remove a document
---

