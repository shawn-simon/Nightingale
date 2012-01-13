from datetime import datetime, timedelta
import json
from tornado.web import RequestHandler, StaticFileHandler
from nightingale.models import User, OnlineModels

def get_routes():
    return [
        (r"/static/(.*)", StaticFileHandler, {'path': 'static'}),
        (r"/", OnlineModelListingsHandler),
        (r"/login", LoginHandler),
        (r"/logout", LoginHandler),
        (r"/service", WebAPIHandler),
        (r"/service/(get_online_models)", WebAPIHandler),
        (r"/announce", VuzeHandler),
        (r"/scrape", VuzeHandler)
    ]

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return User.getByCookie(self.get_secure_cookie('user'))
    
class LoginHandler(BaseHandler):
    def get(self):
        if self.request.uri.endswith('logout'):
            self.clear_all_cookies()
        self.redirect('/')
        
    def post(self):
        if ('user' not in self.request.arguments or 
            'pass' not in self.request.arguments):
            return self.failedLogin()
        user = User.getByName(self.get_argument('user'))
        if not user:
            return self.failedLogin()
        if not user.passwordMatches(self.get_argument('pass')):
            return self.failedLogin()
        uid = user.createUID()
        user.addCookie(uid, expires=datetime.utcnow() + timedelta(1))
        self.set_secure_cookie('user', uid)
        self.redirect('/')
        
    def failedLogin(self):
        self.redirect('/')
    
class WebAPIHandler(BaseHandler):
    def get(self, action=None):
        if action == 'get_online_models':
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps([model.__dict__ for model in OnlineModels().getOnlineModels()]))
        else:
            self.write("<p><a href=\"/service/get_online_models\">get_online_models</a></p>")
        
class OnlineModelListingsHandler(BaseHandler):
    def get(self):
        self.render('index.html', models=OnlineModels().getOnlineModels())
    
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console."""
    def get(self):
        pass
