import gevent

from django_mushroom.utils import rpc_function, scheduled_function


@rpc_function
def new_user(self, request):
    if not hasattr(self, 'ACTIVE_CHATS'):
        self.ACTIVE_CHATS = {}
    if not hasattr(self, 'ACTIVE_USERS_BY_NAME'):
        self.ACTIVE_USERS_BY_NAME = {}
    if not hasattr(self, 'ACTIVE_USERS_BY_KEY'):
        self.ACTIVE_USERS_BY_KEY = {}
    if request.data[u'username'] != "":
        req_username = request.data[u'username']
        req_session_key = request.session.id
        req_chat_id = request.data[u'chat_id']
        if req_chat_id not in self.ACTIVE_CHATS:
            self.ACTIVE_CHATS[req_chat_id] = {}
        if req_session_key not in self.ACTIVE_CHATS[req_chat_id]:
            self.ACTIVE_CHATS[req_chat_id][req_session_key] = req_username

        for chat_id in self.ACTIVE_CHATS:
            if chat_id == req_chat_id:
                pass
            else:
                if req_session_key in self.ACTIVE_CHATS[chat_id]:
                    del self.ACTIVE_CHATS[chat_id][req_session_key]

        new_user_list = [
            {'username': self.ACTIVE_CHATS[chat_id][session_key]} for \
            session_key in self.ACTIVE_CHATS[chat_id]
        ]
        for session_key in self.ACTIVE_CHATS[req_chat_id]:
            self.sessions.sessions[session_key].notify(
                'users',
                new_user_list
            )
        self.ACTIVE_USERS_BY_NAME[req_username] = req_session_key
        self.ACTIVE_USERS_BY_KEY[req_session_key] = req_username


@rpc_function
def message(self, request):
    """
    """
    if request.data['message'].startswith('/msg '):
        msg = request.data['message']
        splitted_msg = msg.split()
        splitted_msg.pop(0)  # remove the /msg part
        if len(splitted_msg) > 1:  # check if username and a message is left
            to_user = splitted_msg.pop(0)
            session_key = self.ACTIVE_USERS_BY_NAME.get(to_user, None)
            if session_key:
                request.data['message'] = " ".join(splitted_msg)
                request.data['message_class'] = "whisper"
                self.sessions.sessions[session_key].notify(
                    'message',
                    request.data
                )
    else:
        for session_key in self.ACTIVE_CHATS[request.data['chat_id']]:
            request.data['message_class'] = 'message'
            self.sessions.sessions[session_key].notify('message', request.data)


@scheduled_function
def notify_active_users(self):
    while True:
        gevent.sleep(1)
        sessions = self.sessions.sessions
        if hasattr(self, 'ACTIVE_CHATS'):
            modified_chats = []
            for session_key in sessions:
                if not sessions[session_key].transport.connected:
                    username = self.ACTIVE_USERS_BY_KEY[session_key]
                    del self.ACTIVE_USERS_BY_NAME[username]
                    del self.ACTIVE_USERS_BY_KEY[session_key]
                    for chat_id in self.ACTIVE_CHATS:
                        if session_key in self.ACTIVE_CHATS[chat_id]:
                            del self.ACTIVE_CHATS[chat_id][session_key]
                            modified_chats.append(chat_id)

            for chat_id in modified_chats:
                new_user_list = [
                    {'username': self.ACTIVE_CHATS[chat_id][session_key]} for \
                        session_key in self.ACTIVE_CHATS[chat_id]
                ]
                for session_key in self.ACTIVE_CHATS[chat_id]:
                    self.sessions.sessions[session_key].notify(
                        'users',
                        new_user_list
                )
