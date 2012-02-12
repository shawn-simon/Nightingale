
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
    
    $('.login .login-btn').live('click', function(e) {
        e.preventDefault();
        
        var postvars = {};
        $('.login input').each(function(i, o) { postvars[o.name] = $(o).val(); });
        
        var loginerr = $('.login .loginerr');
        loginerr.hide();
        
        $.post('/service/login', postvars, function(data) {
            if(data.html) {
                self.replaceHtml(data.html);
            }
            if(data.loginerr) {
                loginerr.text(data.loginerr);
                loginerr.effect('highlight', {color: '#ff0000'}, 1000);
                return;
            }
        });
    });
    
    $('.logout').live('click', function(e) {
        e.preventDefault();
        console.log('logging out...');
        $.get('/logout', {partial: true}, function(data) {
            if(data.html) {
                self.replaceHtml(data.html);
            }
            
        });
    });
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

camlib.prototype.replaceHtml = function(data) {
    for(k in data) {
        if(elem = $('.' + k)) {
            elem.html(data[k]);
        }
    }
}
