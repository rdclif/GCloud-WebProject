#from google.cloud import datastore
import requests
import json
import datetime
import appScripts
import config
import os
import numpy as np
import math



from flask import Flask, render_template, request, session, redirect, Response, current_app
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)


# Environment variables are defined in app.yaml.

if (config.DEBUG):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    user_ip = db.Column(db.String(46))
    user_city = db.Column(db.String(46))
    user_country = db.Column(db.String(46))

    def __init__(self, timestamp, user_ip, user_city, user_country):
        self.timestamp = timestamp
        self.user_ip = user_ip
        self.user_city = user_city
        self.user_country = user_country

class Zip(db.Model):
    __tablename__ = 'zips'

    zip_id = db.Column(db.INT, autoincrement=True, primary_key=True)
    zip = db.Column(db.String(20))
    city = db.Column(db.String(50))
    st = db.Column(db.String(10))
    lat = db.Column(db.Float(10))
    lon = db.Column(db.Float(10))

    def __init__(self, zip_code, city, st, lat, lon):
        self.zip = zip_code
        self.city = city
        self.st = st
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return 'Zip: {}, City: {}, State: {}, Lat: {}, Lon: {}'.format(self.zip, self.city, self.st, self.lat, self.lon)


# Home page
@app.route('/')
def home():
    user_ip = request.environ['REMOTE_ADDR']
    request_url = "https://ipinfo.io/" + user_ip + "/json"
    city = "None"
    county = "None"
    r = requests.get(request_url)

    if r is not None:
        data = r.json()
        print(data)
        try:
            city = data['city']
            county = data['country']
        except:
            city = "None"
            county = "None"



    visit = Visit(
        user_ip=user_ip,
        timestamp=datetime.datetime.utcnow(),
        user_city=city,
        user_country=county
    )

    db.session.add(visit)
    db.session.commit()
    return render_template('home.html')


# Resume Page
@app.route('/resume')
def about():
    return render_template('resume.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# zip code page
@app.route('/zip')
def zip():
    return render_template('zip.html')

# Zipcode POST request -
@app.route('/zipRequest/<zip>', defaults={'dist': None}, methods=['POST'])
@app.route('/zipRequest/<zip>/<dist>', methods=['POST'])
def zipRequest(zip, dist):
    if request.method == 'POST':
        if(zip):
            if(dist):
                #in case of error
                if (dist == 'null'):
                    dist = '5'
                d = int(dist)
            else:
                d = 5

            center = Zip.query.filter(Zip.zip == zip).first()
            if center is not None:
                lat = center.lat
                lon = center.lon
                #of the earth in miles!
                r = 3959

                latN = np.rad2deg(np.arcsin(np.sin(np.deg2rad(lat)) * np.cos(d / r) + np.cos(np.deg2rad(lat)) * np.sin(d / r) * np.cos(np.deg2rad(0))))
                latS = np.rad2deg(np.arcsin(np.sin(np.deg2rad(lat)) * np.cos(d / r) + np.cos(np.deg2rad(lat)) * np.sin(d / r) * np.cos(np.deg2rad(180))))
                lonE = np.rad2deg(np.deg2rad(lon) + np.arctan2(np.sin(np.deg2rad(90)) * np.sin(d / r) * np.cos(np.deg2rad(lat)), np.cos(d / r) - np.sin(np.deg2rad(lat)) * np.sin(np.deg2rad(latN))))
                lonW = np.rad2deg(np.deg2rad(lon) + np.arctan2(np.sin(np.deg2rad(270)) * np.sin(d / r) * np.cos(np.deg2rad(lat)), np.cos(d / r) - np.sin(np.deg2rad(lat)) * np.sin(np.deg2rad(latN))))


                latN = np.asscalar(latN)
                latS = np.asscalar(latS)
                lonE = np.asscalar(lonE)
                lonW = np.asscalar(lonW)
                #print("{} {} {} {}".format(latN, latS, lonE, lonW))

                list = Zip.query.filter(db.and_(Zip.lat <= latN, Zip.lat >= latS, Zip.lon <= lonE, Zip.lon >= lonW)).filter(db.and_(Zip.zip != zip)).order_by(Zip.st, Zip.city, Zip.lat, Zip.lon)

                output = []

                for x in list:
                    list_item = {'zip': x.zip, "city": x.city, "st": x.st, "lat": x.lat, "lon": x.lon}
                    output.append(list_item)

                map_center = {'lat': lat, 'lon': lon}
                out_array = [map_center, output]

                txt_output = json.dumps(out_array)

                return Response(txt_output, mimetype='text/xml')
            else:
                output = "bad request"
            return Response(output, mimetype='text/xml')
        else:
            return appScripts.fBadRequest()
    else:

        return appScripts.fBadRequest()

#based on the gcloud demo
@app.route('/ipList', methods=['GET'])
def ipLits():
    visits = Visit.query.order_by(sqlalchemy.desc(Visit.timestamp)).limit(20)

    results = [
        'Time: {}, Addr: {}, City: {}, Country: {}'.format(x.timestamp, x.user_ip, x.user_city, x.user_country)
        for x in visits]

    output = 'Last 20 visits:\n{}'.format('\n'.join(results))

    return Response(output, mimetype='text/xml')


# Blog - Not currently used
# @app.route('/blog')
# def blog():
#     out = {}
#     if 'email' in session:
#         if session['email'] == "rclif4433@gmail.com":
#             admin = True
#         elif session['email'] == "Kim.cooper122@gmail.com":
#             admin = True
#         else:
#             admin = False
#     else:
#         admin = False
#     admin = True
#     out['admin'] = admin
#     return render_template('blog.html', data = out)
#
# # oAuth page - either asks user to login with google or display user email -
# @app.route('/oAuthReq')
# def reqAuth():
#     if 'email' in session:
#         data = session['email']
#     else:
#         data = None
#     return render_template('oAuthReq.html', data=data)
#
# #Called from G+ login link - Sends first Get Request to google - Redirect User to Login
# @app.route('/oauth', methods=['GET', 'POST'])
# def oauth():
#     if request.method == 'POST':
#         print(request.form)
#     else:
#         try:
#             state = appScripts.idGen()
#             session['state'] = state
#             redir = request.url_root + "oauthcallback"
#             payload = '?response_type=' + config.RESPONSE_TYPE + '&client_id=' + config.CLIENT_ID + '&redirect_uri=' + redir + '&scope=' + config.SCOPE + '&state=' + state
#             res = config.AUTH_URL + payload
#             return redirect(res)
#         except:
#             return "Bad Request", 400
#
#
# #Handles Callback from google -  handles authorization code request to get access token - also get request for user data and renders
# @app.route('/oauthcallback')
# def oauthcallback():
#     data = request.args
#     state = data['state']
#     code = data['code']
#     redir = request.url_root + "oauthcallback"
#     if session['state'] == state:
#         try:
#             payload = {'code': code, 'client_id': config.CLIENT_ID, 'client_secret': config.CLIENT_SECRET, 'redirect_uri': redir, 'scope': config.SCOPE, 'grant_type': 'authorization_code'}
#             req = requests.post(config.TOKEN_URL, data=payload)
#             resp = req.json()
#             session['access_token'] = resp['access_token']
#             session['token_type'] = resp['token_type']
#             auth = session['token_type'] + ' ' + session['access_token']
#             headers = {'Authorization': auth}
#             addr = 'https://www.googleapis.com/plus/v1/people/me'
#             r = requests.get(addr, headers=headers)
#             getresp = r.json()
#             session['email'] = getresp['emails'][0]['value']
#             out = {}
#             out['resp'] = json.dumps(getresp)
#             out['fName'] = getresp['name']['givenName']
#             out['lName'] = getresp['name']['familyName']
#             out['gplus'] = getresp['isPlusUser']
#             out['state'] = session['state']
#             if getresp['isPlusUser'] == True:
#                 out['gplus'] = 'True'
#                 out['link'] = getresp['url']
#             else:
#                 out['gplus'] = 'False'
#                 out['link'] = ''
#             return render_template('oAuthRes.html', data=out)
#         except:
#             return "Bad Request", 400
#     else:
#         return "Bad Request", 400
#
# #removes
# @app.route('/logout')
# def logout():
#    # remove the username from the session if it is there
#    session.pop('email', None)
#    session.pop('access_token', None)
#    session.pop('token_type', None)
#    session.pop('state', None)
#    return redirect('/')
#
# @app.route('/post_update', methods=['POST'])
# def postHandler():
#     if request.method == 'POST':
#         ds = get_client()
#         key = ds.key('Post')
#         entity = datastore.Entity(key=key, exclude_from_indexes=['post'])
#         data = request.form.to_dict(flat=True)
#         entity.update(data)
#         ds.put(entity)
#         return redirect('/blog')
#     else:
#         return appScripts.fForbid()


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500
# [END app]

def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=config.DEBUG)
