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
        self.default_status = 'offline'
        self.default_thumb = 'static/girl.png'
        self.default_namecss = 'f0 c0'
    
        self.id = id
        self.usertype = usertype
        self.name = name
        self.hash = hash
        self.created = created
        self.lastlogin = lastlogin
        self.status = status if status else self.default_status
        self.thumb = self.default_thumb
        self.namecss = namecss if namecss else self.default_namecss
        self.score = random.randint(0, 100)
    
    @classmethod
    def addUser(cls, name, password, namecss=None, usertype=None, status=None):
        result = db.execute("""
            insert into user (name, hash, namecss, usertype, status, created)
            values(:name, :hash, :namecss, :usertype, :status, datetime())
            """,
            name=name,
            hash=bcrypt.hashpw(password, bcrypt.gensalt()),
            namecss=namecss,
            usertype=usertype,
            status=status)
        return User.getByName(name)
    
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
    def getAllUsers(cls):
        result = db.execute("""
            select u.id, u.name, u.namecss, u.hash, u.created, u.lastlogin, u.status
            from user u order by u.id
            """)
        models = [User(**row) for row in result.fetchall()]
        return models
        
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
        
    def passwordMatches(self, password):
        return bcrypt.hashpw(password, self.hash) == self.hash
        
    def publicInfo(self):
        return dict(status=self.status,
            name=self.name,
            namecss=self.namecss,
            thumb=self.thumb,
            score=self.score)
        
    def save(self):
        result = db.execute("""
            update user set namecss=:namecss
            where id=:id
            """, **self.__dict__)
        
     