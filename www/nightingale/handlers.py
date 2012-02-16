import json
import urllib
from tornado.web import HTTPError, RequestHandler, StaticFileHandler
from nightingale.models import LoginHandlerLogic, OnlineModels, User
from nightingale.uimodules import HomeModelsList, MicroLoginModule, UserInfoModule

def get_routes():
    return [
        (r"/static/(.*)", StaticFileHandler, {'path': 'static'}),
        (r"/", OnlineModelListingsHandler),
        (r"/login", LoginHandler),
        (r"/logout", LoginHandler),
        (r"/service", WebAPIHandler),
        (r"/service/(.+)", WebAPIHandler),
        (r"/announce", VuzeHandler),
        (r"/scrape", VuzeHandler)
    ]

    
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return User.getByCookie(self.get_secure_cookie('user'))
    
    
class LoginHandler(BaseHandler):
    def get(self):
        if 'logout' in self.request.uri:
            self.clear_all_cookies()
        if self.get_argument('partial', False):
            logincontrol = MicroLoginModule(self)
            html = dict(userinfo=logincontrol.render(force=True))
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(dict(html=html)))
        else:
            self.redirect('/')
        
    def post(self):
        login = LoginHandlerLogic()
        login.tryLogin(self)        
        
    def successfulLogin(self, user):
        self.redirect('/')
        
    def failedLogin(self, reason=None):
        if reason is None:
            self.redirect('/')
        else:
            self.redirect('/?' + urllib.urlencode(dict(loginerr=reason)))
    
    
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
            
    def post(self, action=None):
        if action == 'login':
            login = LoginHandlerLogic()
            login.tryLogin(self)    
        else:
            raise HTTPError(501)
            
    def successfulLogin(self, user):
        usercontrol = UserInfoModule(self)
        html = dict(userinfo=usercontrol.render(user))
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(dict(id=user.id, name=user.name, html=html)))
        
    def failedLogin(self, reason=None):
        self.set_header('Content-Type', 'application/json')
        if reason is None:
            self.write(json.dumps(dict(loginerr='Login failed')))
        else:
            self.write(json.dumps(dict(loginerr=reason)))
        
        
class OnlineModelListingsHandler(BaseHandler):
    def get(self):
        if self.get_argument('partial', False):
            modelscontrol = HomeModelsList(self)
            html = dict(models=modelscontrol.render())
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(dict(html=html)))
        else:
            self.render('index.html')
    
    
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console."""
    def get(self):
        pass
