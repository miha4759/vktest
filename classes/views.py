from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from app import app
from classes.config import Config
from classes.vkapi import VkApi


@app.route("/")
@app.route("/index")
def index():
    access_token = session.get('vk_access_token')
    data = {}

    if access_token:
        vk_api = VkApi()
        vk_api.access_token = access_token

        user_name = vk_api.get_user_info()
        user_friends = vk_api.get_user_friends()

        data['user'] = {
            'name': "%(first_name)s %(last_name)s" % {"first_name": user_name.get('first_name'), "last_name": user_name.get('last_name')},
            'friends': user_friends['items']
        }
    else:
        data['url'] = {
            'oauth_url': Config.VK_OAUTH_URL,
            'client_id': Config.VK_APP_CLIENT_ID,
            'redirect_uri': str(request.url_root) + 'oauth',
            'v': Config.VK_API_V
        }

    return render_template("index.html",
                           title='VK Auth',
                           data=data)


@app.route('/oauth')
def oauth():
    vk_api = VkApi()
    access_token = vk_api.get_access_token(request.args.get('code'))
    if access_token:
        session['vk_access_token'] = access_token
    return redirect(url_for('index'))
