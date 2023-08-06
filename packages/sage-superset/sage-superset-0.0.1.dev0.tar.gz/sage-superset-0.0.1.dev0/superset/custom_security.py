from flask import redirect, g, flash, request
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user
import requests
import superset_config
class CustomAuthDBView(AuthDBView):
    @expose('/sso/login/', methods=['GET'])
    def sso_login(self):
        print("------------ login", request.args)
        if request.args.get('ticket') is not None:
            r = requests.get(**login_url**, verify=False)
            print("------------ validate", r.json()['username'])
            username = r.json()['username']
            user = self.appbuilder.sm.find_user(username=username)
            if user is not None:
                print("------------ find user", user)
                login_user(user, remember=False)
                return redirect(self.appbuilder.get_url_for_index)
            else:
                user = self.appbuilder.sm.add_user(
                    username=username,
                    first_name=username.split('.')[0],
                    last_name=username.split('.')[1],
                    password = username,
                    email=username,
                    role=self.appbuilder.sm.find_role(self.appbuilder.sm.auth_user_registration_role))
                print("------------ new user", user)
                login_user(user, remember=False)
                return redirect(self.appbuilder.get_url_for_index)
        else:
            return redirect(***login_url***)
    @expose('/sso/logout/', methods=['GET'])
    def sso_logout(self):
        print("------------ logout", logout_url)
        return redirect(**logout_url**)
class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)
