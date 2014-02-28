#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     13/12/2013
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web
from web import form
from base import render, logged, session
from loginmodel import LoginModel
import hashlib

model = LoginModel()

class Register:

    vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vemail = form.regexp(r".*@.*", "must be a valid email address")
    vuser_req = form.Validator("Username not provided.", bool)
    vuser_length = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vuser_exist = form.Validator("Username already exist.", lambda u: u is None or model.get_user(u.username) is None)
    vpass_match = form.Validator("Password didn't match", lambda i: i.password == i.password2)

    register_form = form.Form(
    form.Textbox("username", vuser_req, vuser_length, description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", vpass, description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [vpass_match, vuser_exist],
    )

    def GET(self):
        # do $:f.render() in the template
        if not logged():
            #f = self.register_form()
            return render.register(None, None)
        else:
            raise web.seeother('/')

    def POST(self):
        data = web.input()
        if self.userisexist(data.username) and not self.passwordmatch(data):
            return render.register({
                "user_err": "Username already exist!",
                "pass_err": "Password didn't match!",
                },
                data)
        elif self.userisexist(data.username):
            return render.register({
                "user_err": "Username already exist!",
                "pass_err": "",
                },
                data)
        elif not self.passwordmatch(data):
            return render.register({
                "user_err": "",
                "pass_err": "Password didn't match!",
                },
                data)
        else:
            model.new_user(data.username, self.encryptpass(data.password), data.email)
            session.user = data.username.strip()
            session.privilege = 0
            session.login = model.get_user(data.username.strip())['id']
            raise web.seeother('/')

    def passwordmatch(self, data):
        if data.password != data.password2:
            return False
        else:
            return True

    def userisexist(self,name):
        username = model.get_user(name)
        if username is None:
            return False
        else:
            return True

    def encryptpass(self, password):
        return hashlib.sha1("sAlT754-"+password).hexdigest()

