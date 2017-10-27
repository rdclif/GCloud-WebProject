from google.cloud import datastore
import requests
import json
import appScripts
import config

from flask import Flask, render_template, request, session, redirect, Response, current_app
app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    out = {}
    if 'email' in session:
        if session['email'] == "rclif4433@gmail.com":
            admin = True
        elif session['email'] == "Kim.cooper122@gmail.com":
            admin = True
        else:
            admin = False
    else:
        admin = False
    admin = True
    out['admin'] = admin
    return render_template('blog.html', data = out)

@app.route('/resume')
def about():
    return render_template('resume.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# oAuth page - either asks user to login with google or display user email
@app.route('/oAuthReq')
def reqAuth():
    if 'email' in session:
        data = session['email']
    else:
        data = None
    return render_template('oAuthReq.html', data=data)

#Called from G+ login link - Sends first Get Request to google - Redirect User to Login
@app.route('/oauth', methods=['GET', 'POST'])
def oauth():
    if request.method == 'POST':
        print(request.form)
    else:
        try:
            state = appScripts.idGen()
            session['state'] = state
            redir = request.url_root + "oauthcallback"
            payload = '?response_type=' + config.RESPONSE_TYPE + '&client_id=' + config.CLIENT_ID + '&redirect_uri=' + redir + '&scope=' + config.SCOPE + '&state=' + state
            res = config.AUTH_URL + payload
            return redirect(res)
        except:
            return "Bad Request", 400


#Handles Callback from google -  handles authorization code request to get access token - also get request for user data and renders
@app.route('/oauthcallback')
def oauthcallback():
    data = request.args
    state = data['state']
    code = data['code']
    redir = request.url_root + "oauthcallback"
    if session['state'] == state:
        try:
            payload = {'code': code, 'client_id': config.CLIENT_ID, 'client_secret': config.CLIENT_SECRET, 'redirect_uri': redir, 'scope': config.SCOPE, 'grant_type': 'authorization_code'}
            req = requests.post(config.TOKEN_URL, data=payload)
            resp = req.json()
            session['access_token'] = resp['access_token']
            session['token_type'] = resp['token_type']
            auth = session['token_type'] + ' ' + session['access_token']
            headers = {'Authorization': auth}
            addr = 'https://www.googleapis.com/plus/v1/people/me'
            r = requests.get(addr, headers=headers)
            getresp = r.json()
            session['email'] = getresp['emails'][0]['value']
            out = {}
            out['resp'] = json.dumps(getresp)
            out['fName'] = getresp['name']['givenName']
            out['lName'] = getresp['name']['familyName']
            out['gplus'] = getresp['isPlusUser']
            out['state'] = session['state']
            if getresp['isPlusUser'] == True:
                out['gplus'] = 'True'
                out['link'] = getresp['url']
            else:
                out['gplus'] = 'False'
                out['link'] = ''
            return render_template('oAuthRes.html', data=out)
        except:
            return "Bad Request", 400
    else:
        return "Bad Request", 400

#removes
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('email', None)
   session.pop('access_token', None)
   session.pop('token_type', None)
   session.pop('state', None)
   return redirect('/')

@app.route('/post_update', methods=['POST'])
def postHandler():
    if request.method == 'POST':
        ds = get_client()
        key = ds.key('Post')
        entity = datastore.Entity(key=key, exclude_from_indexes=['post'])
        data = request.form.to_dict(flat=True)
        entity.update(data)
        ds.put(entity)
        return redirect('/blog')
    else:
        return appScripts.fForbid()


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500
# [END app]

def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
