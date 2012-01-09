from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
import random

# these are class models not cam models

class User:
    def 

class Model:
    def __init__(self, name, thumb):
        self.thumb = thumb
        self.name = name
        
class OnlineModels:
    def get_online_models(self):
        lst = ['Chrysanthemum', 'Desert', 'Hydrangeas',  'Jellyfish', 'Koala', 'Lighthouse', 'Penguins', 'Tulips']
        random.shuffle(lst)
        result = []
        for n in range(0, random.randint(0, 4) + 3):
            model = Model(lst[n], 'static/thumbs/' + lst[n] + '.jpg')
            # custom objects not json serializable...so returning the dict for now
            result.append(model.__dict__)
        return result