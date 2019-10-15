from .model import Model

class Publisher(Model):
    attributes_options = {
        "PubId": {"exact": 6, "unique": True, "numeric": True, "indexed": True, "index_file": "Data/Publisher/PublisherPubIdIndex.txt", "required": True},
        "PubName": {"lowerbound": 1, "upperbound": 200, "indexed": True, "index_file": "Data/Publisher/PublisherNameIndex.txt", "required": True},
        "SubjectsInterest": {"upperbound": 200, "indexed": True, "index_file": "Data/Publisher/PublishesrSubjectsInterestIndex.txt", "required": True},
        "HeadName": {"upperbound": 100, "indexed": False, "required": True},
        "PubAddress": {"upperbound": 200, "indexed": False, "required": True},
        }
    data_file = 'Data/Publisher/publishers.txt'
    query_attr = 'PubId'    

    def __str__(self):
        return f'PubId:{self.PubId} , PubName:{self.PubName} , SubjectsInterest:{self.SubjectsInterest} , HeadName:{self.HeadName} , PubAddress:{self.PubAddress}'
