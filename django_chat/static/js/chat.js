$(document).ready(function() {

    var model = {
        username: django_username,
        users: ko.observableArray(),
        message: ko.observable(''),
        messages: ko.observableArray(),
        online: ko.observable(false),
        server_time: ko.observable(''),

        showInUsers: function() {
            client.notify('django_chat_new_user', {
                username: this.username,
                chat_id: django_chat_id
            });
        },
        sendMessage: function() {
            client.notify('django_chat_message', {
                username: this.username,
                message: this.message(),
                chat_id: django_chat_id
            });
            this.message('');
            return false;
        }
    };

    ko.applyBindings(model);
    var client = new mushroom.Client({
        url: 'http://127.0.0.1:8100'
    });

    client.signals.connected.connect(function() {
        model.online(true);
    });

    client.method('message', function(request) {
        model.messages.push(request.data);
    });

    client.method('time', function(request) {
        var new_time_val = new Date(request.data * 1000);
        var h=new_time_val.getHours();
        var m=new_time_val.getMinutes();
        model.server_time(h+":"+m);
    });

    client.method('users', function(request) {
        model.users(request.data);
    });

    client.connect();
    model.showInUsers();
});