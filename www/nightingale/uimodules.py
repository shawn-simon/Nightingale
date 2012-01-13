from tornado.web import UIModule

class CurrentUserModule(UIModule):
    """Show current user info or login form if not logged in."""
    def render(self):
        if not self.current_user:
            return self.render_string('loginform.html')
        else:
            return self.render_string('currentuser.html')