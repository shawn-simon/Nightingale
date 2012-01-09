import random

class Model:
    def __init__(self, name, thumb):
        self.name = name
        self.thumb = thumb

class OnlineModels:
    def get_online_models(self):
        lst = ['Chrysanthemum', 'Desert', 'Hydrangeas',  'Jellyfish', 'Koala', 'Lighthouse', 'Penguins', 'Tulips']
        random.shuffle(lst)
        return [Model(lst[n], 'static/thumbs/' + lst[n] + '.jpg') for n in range(0, random.randint(0, 4) + 3)]
