import os
import unittest
import tornado.ioloop
import tornado.web
import nightingale.handlers
import nightingale.tests
import nightingale.uimodules

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'ui_modules': nightingale.uimodules,
    'login_url': r"/login",
    'cookie_secret': '3dj1wnExSV6zvypr9y6KFbdDfxwkL0g7ky8VLUWJP3s=',
    'debug': True
}
application = tornado.web.Application(nightingale.handlers.get_routes(), **settings)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromModule(nightingale.tests)
    unittest.TextTestRunner().run(suite)
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
