import flask
import os
import err
import main

import google
from google_auth_oauthlib import flow as google_flow
import google_auth_httplib2
import googleapiclient
URI = os.getenv("URI")
app = main.app

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

REDIR_PATH = "/oauth2/redir"

CLIENT_CONF_FILE = os.getenv("CLIENT_CONF_FILE")

@app.route("/oauth2")
def redirect_to_oauth():
    flow = google_flow.Flow.from_client_config(CLIENT_CONF_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for(REDIR_PATH, _external=True)
    
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    flask.session['state'] = state
    
    return flask.redirect(auth_url)
    
@app.route(REDIR_PATH)
def oauth_recieve():
    state = flask.session['state']
    flow = google_flow.Flow.from_client_config(CLIENT_CONF_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for(REDIR_PATH, _external=True)
    auth_res = flask.request.url
    flow.fetch_token(authorization_response=auth_res)
    
    credentials = flow.credentials
    credentials = credentials_to_dict(credentials)
    flask.session['credentials'] = credentials
    
    features = check_granted_scopes(credentials)
    #App needs email to run
    if features['email'] == False:
        return app.redirect("/oauth2/error/email")
    flask.session['features'] = features
    return flask.redirect('/dashboard')
    
    
    
    
@app.route("/oauth2/error/email")
def needs_email():
    return "Error: we need your email! Go back to sign in and allow us to see your email."    
    
def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'granted_scopes': credentials.granted_scopes}
  
def check_granted_scopes(credentials):
  features = {}
  if "https://www.googleapis.com/auth/userinfo.email" in credentials['granted_scopes']:
    features['email'] = True
  else:
    features['email'] = False

  if "https://www.googleapis.com/auth/userinfo.profile" in credentials['granted_scopes']:
    features['profile'] = True
  else:
    features['profile'] = False

  if "openid" in credentials['granted_scopes']:
      features['openid'] = True
  else:
      features['openid'] = False
  return features