
var camlib = function() {};

camlib.prototype.init = function() {
    var self = this;
    $(document).ready(function() {
        self.addEventHandlers();
    });
};

camlib.prototype.addEventHandlers = function() {
    var self = this;
    
    //setInterval(function() { self.reloadIndex(); }, 1000);
    
    $('h1.home a').click(function(e) {
        e.preventDefault();
        self.reloadIndex();
    });
    
    $('.login .login-btn').live('click', function(e) {
        e.preventDefault();
        $('.login .loginerr').hide();
        $.post('/login.json', self.getPostVars('.login input'), function(data) {
            if(data.html) {
                self.replaceHtml(data.html);
            }
            if(data.loginerr) {
                self.showLoginError(data.loginerr);
                return;
            }
        }).error(function() {
            self.showLoginError('Try again later');
        });
    });
    
    $('.logout').live('click', function(e) {
        e.preventDefault();
        $.get('/logout.json', function(data) {
            if(data.html) {
                self.replaceHtml(data.html);
            }
        }).error(function() {
            self.showLoginError('Try again later');
        });
    });
    
    $('.models .model .viewprofile').live('click', function(e) {
        e.preventDefault();
        $.get(e.currentTarget.href + '.json', function(data) {
            if(data.profile) {
                self.showProfile(data);
            }
        });
    });
};

camlib.prototype.showLoginError = function(msg) {
    if(loginerr = $('.login .loginerr')) {
        loginerr.text(msg);
        loginerr.effect('highlight', {color: '#ff0000'}, 1000);
    }
};

camlib.prototype.reloadIndex = function() {
    var self = this;
    $.get('/.json', function(data) {
        if(data.models) {
            self.showModelList(data.models);
        }
    });
};

camlib.prototype.reloadProfile = function() {
    var self = this;
    $.get(window.location.href + '.json', function(data) {
        if(data.profile) {
            self.showProfile(data);
        }
    });
};

camlib.prototype.showModelList = function(models) {
    var html = '';
    $.each(models, function(i, item) {
        html += '<div class="model">'
             + '    <div class="img">'
             + '        <a href="/' + item.name + '" class="viewprofile">'
             +'             <img src="' + item.thumb + '" width="100" height="100" alt="' + item.name + '" title="' + item.name + '" />'
             +'         </a>'
             + '    </div>'
             + '    <div class="name">'
             + '        <a href="/' + item.name + '" class="' + item.namecss + ' viewprofile">' + item.name + '</a>'
             + '    </div>'
             + '</div>';
    });
    html = '<div class="models">' + html + '</div>';
    $('.content').html(html);
};

camlib.prototype.showProfile = function(data) {
    var user = data.user;
    var profile = data.profile;
    var html = '';
    html += '<h2 class="' + user.namecss + '">' + profile.title + '</h2>';
    html += '<p><img src="/static/camph.png" alt="" width="400" height="300" /></p>';
    $('.content').html(html);
};

camlib.prototype.getPostVars = function(target) {
    var result = {};
    $(target).each(function(i, o) { result[o.name] = $(o).val(); });
    return result;
};

camlib.prototype.replaceHtml = function(data) {
    $.each(data, function(i, row) {
        if(elem = $(row.target)) {
            elem.html(row.html);
        }
    });
}
