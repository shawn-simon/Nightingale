from datetime import datetime, timedelta
import urllib
from tornado.web import HTTPError, RequestHandler, StaticFileHandler
from nightingale.models import EmptyObject, User
from nightingale.uimodules import MicroLoginModule, UserInfoModule
from nightingale.utils import tojson

def get_routes():
    return [
        (r"/static/(.*)", StaticFileHandler, {'path': 'static'}),
        (r"/", IndexHandler),
        (r"/\.json", IndexHandler, dict(context='json')),
        (r"/login/?", LoginHandler),
        (r"/login/?\.json", LoginHandler, dict(context='json')),
        (r"/logout/?", LogoutHandler),
        (r"/logout/?\.json", LogoutHandler, dict(context='json')),
        (r"/users/?", UsersHandler),
        (r"/users/?\.json", UsersHandler, dict(context='json')),
        (r"/announce", VuzeHandler),
        (r"/scrape", VuzeHandler),
        (r"/(.[^/]+)/?\.json", ModelHandler, dict(context='json')),
        (r"/(.[^/]+).*", ModelHandler)
    ]

    
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return User.getByCookie(self.get_secure_cookie('user'))
    
    
class IndexHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
    
    def get(self):
        if self.context == 'json':
            result = EmptyObject()
            result.models = [model.publicInfo() for model in User.getOnlineModels()]
            self.set_header('Content-Type', 'application/json')
            self.write(tojson(result))
        else:
            self.render('index.html')
    
    
class LoginHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context

    def get(self):
        self.redirect('/')
        
    def post(self):
        if ('user' not in self.request.arguments or 
            'pass' not in self.request.arguments):
            return self.failedLogin(reason='Missing arguments')
        user = User.getByName(self.get_argument('user'))
        if not user:
            return self.failedLogin(reason='Invalid username')
        if not user.passwordMatches(self.get_argument('pass')):
            return self.failedLogin(reason='Invalid password')
        uid = user.createUID()
        user.addCookie(uid, expires=datetime.utcnow() + timedelta(1))
        self.set_secure_cookie('user', uid)
        self.successfulLogin(user) 
        
    def successfulLogin(self, user):
        if self.context == 'json':
            usercontrol = UserInfoModule(self)
            result = EmptyObject()
            result.id = user.id
            result.name = user.name
            result.html = []
            result.html.append(dict(target='.userinfo', html=usercontrol.render(user)))
            self.set_header('Content-Type', 'application/json')
            self.write(tojson(result))
        else:
            self.redirect('/')
        
    def failedLogin(self, reason='Login failed'):
        if self.context == 'json':
            result = EmptyObject()
            result.reason = reason
            self.set_header('Content-Type', 'application/json')
            self.write(tojson(result))
        else:
            self.redirect('/?' + urllib.urlencode(dict(loginerr=reason)))
    
    
class LogoutHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
        
    def get(self):
        self.clear_all_cookies()
        if self.context == 'json':
            logincontrol = MicroLoginModule(self)
            result = EmptyObject()
            result.html = []
            result.html.append(dict(target='.userinfo', html=logincontrol.render(force=True)))
            self.set_header('Content-Type', 'application/json')
            self.write(tojson(result))
        else:
            self.redirect('/')
    
    
class ModelHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
    
    def get(self, name):
        user = User.getByName(name)
        if self.context == 'json':
            result = EmptyObject()
            result.user = user.publicInfo()
            result.profile = EmptyObject()
            result.profile.title = user.name
            self.set_header('Content-Type', 'application/json')
            self.write(tojson(result))
        else:
            self.render('model.html')
    
    
class UsersHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
    
    def get(self):
        if self.context == 'json':
            pass
        else:
            self.render('users.html', users=User.getAllUsers())
    
    
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console."""
    def get(self):
        pass
