import os
import tornado.ioloop
import tornado.web
import lib.handlers
from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
metadata = MetaData(bind=engine)
settings = {
    'static_path':   os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'login_url':     r"/login",
    'debug':         True,
    'cookie_secret': "3dj1wnExSV6zvypr9y6KFbdDfxwkL0g7ky8VLUWJP3s="
}
application = tornado.web.Application(lib.handlers.get_routes(), **settings)

if __name__ == '__main__':
    application.listen(81)
    tornado.ioloop.IOLoop.instance().start()