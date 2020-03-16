ROW_LIMIT = 5055
SUPERSET_WORKERS = 4
SUPERSET_WEBSERVER_PORT = 8088
import os
from flask import Flask
import time
import logging
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
from superset.security import SupersetSecurityManager
import logging
from flask_appbuilder import SQLA, AppBuilder
     
class CustomSsoSecurityManager(SupersetSecurityManager):
    #@appbuilder.sm.oauth_user_info_getter
    def oauth_user_info(self, provider, response=None):
      if provider == 'boilerplate':
        #print("INsilde Boiler")
       # time.sleep(5)
        print(self.appbuilder.sm.oauth_remotes[provider])
        res = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
        #print("Usersfddddddddddddddddddddddddddddddddddddddddddddddddd",res.data)
        if res.status != 200:
            logger.error('Failed to obtain user info: %s', res.data)
            return
        me = res.data
        #logger.debug(" user_data: %s", me)
        #print("BLEHHHHHHHHHHHHHHHHHHHHHH")
        prefix = 'Superset'
        return {
                'username' : me['username'],
                #'name' : me['name'],
                'email' : me['email'],
                'first_name': me['first_name'],
                'last_name': me['last_name'],
            }

# from superset.security import SupersetSecurityManager

# class CustomSsoSecurityManager(SupersetSecurityManager):
#     #@appbuilder.sm.oauth_user_info
#     def oauth_user_info(self, provider, response=None):
#         logging.debug("Oauth2 provider: {0}.".format(provider))
#         if provider == 'boilerplate':
#             # As example, this line request a GET to base_url + '/' + userDetails with Bearer  Authentication,
#             # and expects that authorization server checks the token, and response with user details
#             me = self.appbuilder.sm.oauth_remotes[provider].get('userinfo').data
#             logging.debug("user_data: {0}".format(me))
#             return { 'name' : me['name'], 'email' : me['email'], 'id' : me['user_name'], 'username' : me['user_name'], 'first_name':'', 'last_name':''}

CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
AUTH_TYPE = AUTH_OAUTH
AUTH_ROLE_PUBLIC = 'Public'
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Admin'
CSRF_ENABLED = True
ENABLE_PROXY_FIX = True
PREFERRED_URL_SCHEME = 'https'
  
OAUTH_PROVIDERS = [
 # {
 #   'name': 'google',
 #   'whitelist': ['@company.com'],
 #   'icon': 'fa-google',
 #   'token_key': 'access_token', 
 #   'remote_app': {
 #     'base_url': 'https://www.googleapis.com/oauth2/v2/',
 #     'request_token_params': {
 #     'scope': 'email profile'
 #     },
 #     'request_token_url': None,
 #     'access_token_url':'https://accounts.google.com/o/oauth2/token',
 #     'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
 #     'consumer_key': '540645713264-u915tbjkpbs0t3ognt37158q88m3ea5v.apps.googleusercontent.com',
 #     'consumer_secret': 'wm3iXRYd27--sQmkFOLukAud'
 #    }
 #  }

 {
   'name': 'boilerplate',
   #'whitelist': ['@company.com'],
   'icon': 'fa-google',
   'token_key': 'access_token', 
   'remote_app': {
      'base_url': 'https://' + os.getenv("BASE_URL") + '/backend/o/',
     'request_token_params': {
     #'scope': 'email profile'
     },
     'request_token_url': None,
     'access_token_url':'https://' + os.getenv("BASE_URL") + '/backend/o/token/',
     'authorize_url': 'https://' + os.getenv("BASE_URL") + '/backend/o/authorize/',
     'consumer_key':  os.getenv("CONSUMER_KEY") ,
     'consumer_secret': os.getenv("CONSUMER_SECRET")
    }
  }
]
