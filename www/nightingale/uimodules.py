from tornado.web import UIModule

class UserInfoModule(UIModule):
    """Show current user info if logged in."""
    def render(self, user=None):
        if user:
            return self.render_string('module_userinfo.html', user=user)
        elif self.current_user:
            return self.render_string('module_userinfo.html', user=self.current_user)
        return ''
            
class MicroLoginModule(UIModule):
    """Login form on the homepage."""
    def render(self, force=False):
        loginerr = self.handler.get_argument('loginerr', '')
        if not self.current_user or force:
            return self.render_string('module_micrologin.html', loginerr=loginerr)
        return ''
