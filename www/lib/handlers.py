import json
import tornado.web
from models import OnlineModels

def get_routes():
    return [
        (r"/", OnlineModelListingsHandler),
        (r"/service", WebAPIHandler),
        (r"/service/(get_online_models)", WebAPIHandler),
        (r"/announce", VuzeDiscoveryHandler),
        (r"/scrape", VuzeDiscoveryHandler)
    ]
    
class WebAPIHandler(tornado.web.RequestHandler):
    def get(self, action=None):
        if action == 'get_online_models':
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps([model.__dict__ for model in OnlineModels().get_online_models()]))
        else:
            self.write("<p><a href=\"/service/get_online_models\">get_online_models</a></p>")
        
class OnlineModelListingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', models=OnlineModels().get_online_models())
    
class VuzeDiscoveryHandler(tornado.web.RequestHandler):
    def get(self):
        pass