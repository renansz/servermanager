# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_user, login_required, logout_user

from servermanager.extensions import login_manager
from servermanager.user.models import User
from servermanager.public.forms import LoginForm
from servermanager.user.forms import RegisterForm
from servermanager.utils import flash_errors
from servermanager.database import db

from servermanager.server_calls import estabilish_connection,get_all_info

blueprint = Blueprint('public', __name__, static_folder="../static")

import json

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)

# Server views
@blueprint.route("/servers/")
def list_server():
    # fake server data
    servers = json.load(open('servermanager/servers.json'))
    form = LoginForm(request.form)
    return render_template("servers.html", form=form, servers=servers)

@blueprint.route("/manage/<server_alias>")
def manage_server(server_alias):
    server_info = {'hostname':'localhost','username':'dsl','password':'bakrlz1234','port':5022}

    #connect
    ssh_client = estabilish_connection(server_info) 

    #get info
    info = get_all_info(ssh_client) 
    info['alias'] = server_alias
    info['ip'] = '127.0.0.1' #TODO make it dynamic
    
    form = LoginForm(request.form)
    return render_template("manage_server.html", form=form,info=info)
