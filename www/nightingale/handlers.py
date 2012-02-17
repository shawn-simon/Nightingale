from datetime import datetime, timedelta
import json
import urllib
from tornado.web import HTTPError, RequestHandler, StaticFileHandler
from nightingale.models import OnlineModels, User
from nightingale.uimodules import ListModelsModule, MicroLoginModule, UserInfoModule

def get_routes():
    return [
        (r"/static/(.*)", StaticFileHandler, {'path': 'static'}),
        (r"/", IndexHandler),
        (r"/\.json", IndexHandler, dict(context='json')),
        (r"/login/?", LoginHandler),
        (r"/login/?\.json", LoginHandler, dict(context='json')),
        (r"/logout/?", LogoutHandler),
        (r"/logout/?\.json", LogoutHandler, dict(context='json')),
        (r"/service/?", WebAPIHandler),
        (r"/service/(.+)", WebAPIHandler),
        (r"/announce", VuzeHandler),
        (r"/scrape", VuzeHandler)
    ]

    
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return User.getByCookie(self.get_secure_cookie('user'))
    
    
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
            result = dict(
                id=user.id,
                name=user.name,
                html=[
                    dict(target='.userinfo', html=usercontrol.render(user))
                ]
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result))
        else:
            self.redirect('/')
        
    def failedLogin(self, reason='Login failed'):
        if self.context == 'json':
            result = dict(
                reason=reason
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result))
        else:
            self.redirect('/?' + urllib.urlencode(dict(loginerr=reason)))
    
    
class LogoutHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
        
    def get(self):
        self.clear_all_cookies()
        if self.context == 'json':
            logincontrol = MicroLoginModule(self)
            result = dict(
                html=[
                    dict(target='.userinfo', html=logincontrol.render(force=True))
                ]
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result))
        else:
            self.redirect('/')
    
    
class WebAPIHandler(BaseHandler):
    def get(self, action=None):
        if action is None:
            self.write('<ul>')
            self.write('<li><a href="/service/get_online_models">get_online_models</a></li>')
            self.write('</ul>')
            return
        if action == 'get_online_models':
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps([model.__dict__ for model in OnlineModels().getOnlineModels()]))
        else:
            raise HTTPError(501)
            
        
class IndexHandler(BaseHandler):
    def initialize(self, context=None):
        self.context = context
    
    def get(self):
        if self.context == 'json':
            models = ListModelsModule(self)
            result = dict(
                html=[
                    dict(target='.models', html=models.render())
                ]
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result))
        else:
            self.render('index.html')
    
    
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console."""
    def get(self):
        pass
