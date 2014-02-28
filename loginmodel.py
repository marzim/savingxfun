
from model import Model

class LoginModel:

    db = Model().getDB()
    def get_users(self):
        return self.db.select('users', order='id DESC')

    def get_user(self,user):
        try:
            return self.db.select('users', where='user=$user', vars=locals())[0]
        except IndexError:
            return None

    def get_userbyid(self,userid):
        try:
            return self.db.select('users', where='id=$userid', vars=locals())[0]
        except IndexError:
            return None

    def new_user(self,user, pwd, email):
        self.db.insert('users', user=user, pwd=pwd, email=email)

    def del_user(self,user):
        self.db.delete('users', where="user=$user", vars=locals())

    def update_user(self,id, user, email, privilege):
        self.db.update('users', where="id=$id", vars=locals(), email=email, privilege=privilege)
