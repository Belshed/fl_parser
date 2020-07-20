

class User:
    def __init__(self):
        self.user_id = ''
        self.chat_id = ''
        self.user_name = ''
        self.next_step = 'category_choice'

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_name(self):
        return self.user_name

    def set_user_name(self, user_name):
        self.user_name = user_name

    def get_chat_id(self):
        return self.chat_id

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def get_next_step(self):
        return self.next_step

    def set_next_step(self, next_step):
        self.next_step = next_step
