from random import choice, random, randint, randrange
from nightingale.models import User

def randusername():
    """Generate random username"""
    words = ['young', 'nova', 'swift', 'soft', 'lotus', 'sleep', 'french', 'pink',
             'smurf', 'hitch', 'flame', 'foryou', 'you', 'free', 'crafty', 'fan', 'sky',
             'plump', 'fresh', 'panda', 'bear', 'boob', 'danger', 'within', 'dick', 'kids',
             'zombie', 'horse', 'clue', 'glitter', 'pleasure', 'sheep', 'fuck', 'blaze',
             'girls', 'hard', 'hairless', 'hooker', 's', 'inator', 'inky', 'er', 'sugar',
             'good', 'night', 'smoke', 'tail', 'shadow', 'ass', 'black', 'virgin', 'smart',
             'guest', 'user', 'man', 'porn', 'daddy', 'big', 'fun', 'fire', 'nice', 'viewer',
             'pocket', 'not', 'frisky', 'fox', 'fish', 'dragon', 'pony', 'punk', 'lick',
             'trip', 'plauge', 'bugs', 'bunny', 'angel', 'pervert', 'bomb', 'trip',
             'some', 'guy', 'hunny', 'happy', 'me', 'spread', 'stretch', 'slug', 'amazon',
             'idiot', 'click', 'death', 'bit', 'camel', 'fun', 'intense', 'cool', 'head',
             'wag', 'devil', 'latex', 'dildo', 'purple', 'red', 'pussy', 'beast', 'candy',
             'boom', 'disturbed', 'horny', 'scream', 'massive', 'lucky', 'player', 'love',
             'lover', 'freak', 'cutie', 'army', 'master', 'nation', 'silly', 'dead', 'sin',
             'cheek', 'smooth', 'pain', 'panther', 'lovely', 'cock', 'suck', 'cam']
    result = []
    if random() > 0.75:
        result.append(choice(['xx', 'xxx', 'xXx']))
    for n in range(randrange(2, 3)):
        result.append(choice(words).title())
    if random() > 0.66:
        result.append(choice(['xx', 'xxx', 'xXx', '69', '99', '420', '89', '11', '13', '00', '90']))
    return ''.join(result)
 
def randnamecss():
    return 'f' + str(randint(0, 14)) + ' c' + str(randint(0, 16))
 
def registerusers(amount=10):
    """Register n users with random data"""
    for n in range(amount):
        User.addUser(name=randusername(), password='qwerasdf', namecss=randnamecss(), usertype='model', status='online')
        