
var camlib = function() {};

camlib.prototype.index = function() {
    var self = this;
    $(document).ready(function() {
        self.addEventHandlers();
    });
};

camlib.prototype.addEventHandlers = function() {
    var self = this;
    
    //setInterval(this.refreshModels, 1000);
    
    $('h1.home a').click(function(e) {
        e.preventDefault();
        $.get('/.json', function(data) {
            if(data.html) {
                self.replaceHtml(data.html);
            }
        });
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
};

camlib.prototype.showLoginError = function(msg) {
    if(loginerr = $('.login .loginerr')) {
        loginerr.text(msg);
        loginerr.effect('highlight', {color: '#ff0000'}, 1000);
    }
};

camlib.prototype.refreshModels = function() {
    $.get('/service/get_online_models', function(data) {
        $('.models').html('');
        $.each(data, function(i, item) {
            $('.models').append(''
                + '<div class="model">'
                + '    <div class="img">'
                + '        <a href="/' + item.name + '"><img src="' + item.thumb + '" width="100" height="100" alt="' + item.name + '" title="' + item.name + '" /></a>'
                + '    </div>'
                + '    <div class="name">'
                + '        <a href="/' + item.name + '">' + item.name + '</a>'
                + '    </div>'
                + '</div>');
        });
    });
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
