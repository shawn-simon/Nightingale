import lib.handlers
import lib.test.testsample
import os
import tornado.ioloop
import tornado.web
import unittest

settings = {
    'static_path':   os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'login_url':     r"/login",
    'cookie_secret': '3dj1wnExSV6zvypr9y6KFbdDfxwkL0g7ky8VLUWJP3s=',
    'debug':         True
}
application = tornado.web.Application(lib.handlers.get_routes(), **settings)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromModule(lib.test.testsample)
    unittest.TextTestRunner().run(suite)
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()