#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     10/01/2014
# Copyright:   (c) mc185104 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web
from loginmodel import LoginModel
from base import render, logged, session, withprivilege, superuser
import hashlib

model = LoginModel()

class Login:

    def GET(self):
        """Login page"""
        if not logged():
            return render.login("")
        else:
            raise web.seeother('/')

    def POST(self):
        f = web.input()
        error_msg = "Incorrect username and password!"
        if not self.authenticate():
            return render.login(error_msg)
        else:
            user = model.get_user(f.username.strip())
            session.login = user.id
            session.privilege = user.privilege;
            if f.username.strip() == "admin":
                session.privilege = 1
                session.user = f.username.strip()

            session.user = f.username.strip()
            raise web.seeother('/')

    def authenticate(self):
        f = web.input()
        usr = model.get_user(f.username.strip())
        if usr is None:
            return False
        elif usr['pwd'] != hashlib.sha1("sAlT754-"+f.password).hexdigest():
            return False
        else:
            return True

class Users:
    def GET(self):
        if withprivilege():
            users = model.get_users()
            return render.users(users)
        else:
            raise web.seeother('/')


class EditUser:
    def GET(self, id):
        if withprivilege() and superuser():
            user = model.get_userbyid(int(id))
            return render.usersedit(user)
        else:
            raise web.seeother('/')

    def POST(self, id):
        data = web.input()
        model.update_user(int(id), data.username, data.email, int(data.privilege))
        raise web.seeother('/users')