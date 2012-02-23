from datetime import datetime, timedelta
from unittest import TestCase
import uuid
import bcrypt
from nightingale.models import User
from nightingale.simulation import randusername
        
class TestCrypt(TestCase):
    def test_basic(self):
        password = 'qwerasdf'
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        self.assertEqual(bcrypt.hashpw(password, hashed), hashed)
        
class  TestUser(TestCase):
    def test_getByCookie(self):
        self.assertEqual(None, User.getByCookie(None))
        self.assertEqual(None, User.getByCookie('test'))
        
    def test_getByName(self):
        self.assertEqual(None, User.getByName(None))
        self.assertEqual(None, User.getByName('test'))
        self.assertNotEqual(None, User.getByName('kdeloach'))
        
    def test_addCookie(self):
        u = User.getByName('kdeloach')
        uid = u.createUID()
        expires = datetime.utcnow() + timedelta(1)
        u.addCookie(uid, expires)
        self.assertNotEqual(None, User.getByCookie(uid))
        
    def test_addCookie_expired(self):
        u = User.getByName('kdeloach')
        uid = u.createUID()
        expires = datetime.utcnow() - timedelta(1)
        u.addCookie(uid, expires)
        self.assertEqual(None, User.getByCookie(uid))
      
    def test_simulation1(self):
        self.assertNotEqual('', randusername());
        self.assertNotEqual(None, randusername());
        #for n in range(100):
            #print randusername()
            
