import bcrypt
from operator import attrgetter
import random
import uuid
from nightingale.database import db

class EmptyObject:
    """Necessary for anonymous objects that need a __dict__ attribute (ex. JSON responses)"""
    pass

class User:
    def __init__(self, id=0, usertype='', name='', namecss='', hash='', created=None, lastlogin=None, status=None):
        self.id = id
        self.usertype = usertype
        self.name = name
        self.hash = hash
        self.created = created
        self.lastlogin = lastlogin
        self.status = status if status else 'offline'
        #self.thumb = 'static/thumbs/' + name + '.jpg'
        self.thumb = 'static/girl.png'
        #self.namecss = namecss if namecss else 'f' + str(random.randint(0, 14)) + ' c' + str(random.randint(0, 16))
        self.namecss = namecss if namecss else 'f0 c0'
        self.score = random.randint(0, 100)
        
    @classmethod
    def getByCookie(cls, cookie):
        result = db.execute("""
            select u.id, u.name, u.namecss, u.hash, u.created, u.lastlogin, u.status
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
            select u.id, u.name, u.namecss, u.hash, u.created, u.lastlogin, u.status
            from user u where u.name = :name
            """, name=name)
        row = result.first()
        if not row:
            return None
        return User(**row)
        
    @classmethod
    def getOnlineModels(cls):
        result = db.execute("""
            select u.id, u.name, u.namecss, u.hash, u.created, u.lastlogin, u.status
            from user u where u.usertype = 'model' and u.status = 'online'
            """)
        models = [User(**row) for row in result.fetchall()]
        models = sorted(models, key=attrgetter('score', 'name'))
        return models
        
    def createUID(self):
        return uuid.uuid4().hex
        
    def addCookie(self, cookie, expires):
        db.execute("""
            insert into usercookie (userid, cookie, expires)
            values (:userid, :cookie, :expires)
            """, userid=self.id, cookie=cookie, expires=expires)
        
    def passwordMatches(self, pwd):
        return bcrypt.hashpw(pwd, self.hash) == self.hash
        
     