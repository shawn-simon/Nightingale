import random
import uuid
import bcrypt
from nightingale.database import db

class Model:
    def __init__(self, name):
        self.name = name
        self.thumb = 'static/thumbs/' + name + '.jpg'

class User:
    def __init__(self, id=0, name='', hash='', created=None, lastlogin=None):
        self.id = id
        self.name = name
        self.hash = hash
        self.created = created
        self.lastlogin = lastlogin
        self.status = 'offline'
        
    @classmethod
    def getByCookie(cls, cookie):
        result = db.execute("""
            select u.id, u.name, u.hash, u.created, u.lastlogin 
            from user u inner join usercookie uc on uc.userid = u.id
            where uc.cookie = :cookie and uc.expires > datetime()
            """, cookie=cookie)
        row = result.first()
        if not row:
            return None
        return User(**row)
   
    @classmethod
    def getByName(cls, name):
        result = db.execute("""
            select u.id, u.name, u.hash, u.created, u.lastlogin 
            from user u where u.name = :name
            """, name=name)
        row = result.first()
        if not row:
            return None
        return User(**row)
        
    def createUID(self):
        return uuid.uuid4().hex
        
    def addCookie(self, cookie, expires):
        db.execute("""
            insert into usercookie (userid, cookie, expires)
            values (:userid, :cookie, :expires)
            """, userid=self.id, cookie=cookie, expires=expires)
        
    def passwordMatches(self, pwd):
        return bcrypt.hashpw(pwd, self.hash) == self.hash
        
    
class OnlineModels:
    def getOnlineModels(self):
        lst = ['Chrysanthemum', 'Desert', 'Hydrangeas',  'Jellyfish', 'Koala', 'Lighthouse', 'Penguins', 'Tulips']
        random.shuffle(lst)
        return [Model(lst[random.randint(0, len(lst) -1)]) for n in range(0, 42)]

        