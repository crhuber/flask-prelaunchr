from __future__ import absolute_import, unicode_literals
import os
import datetime
from datetime import datetime
from sqlalchemy import desc

from flask import render_template, session, redirect, url_for, current_app, flash, abort, request
#from .. import db
#from ..models import User
from .email import send_email
from . import main
from .forms import ContestForm
from .. import db
from ..models import User, Referrer, IPAddress

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"%s - %s" % (
                getattr(form, field).label.text,
                error
            ))

@main.route('/')
def landing_page():
    # redirect to referral page is user has already signed up
    if 'h_email' in session:
        email = session['h_email']
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return redirect(url_for('main.refer'))
        except:
            session.pop('h_email', None)
   

    return redirect(url_for('main.sign_up'))

@main.route('/refer/<string:referral_code>')
def new_referral(referral_code):
    # if its a new user, get the user that referred them. Save referrer in a cookie. Redirect to signup
    if referral_code:
        try:
            user = User.query.filter_by(referral_code=referral_code).first()
            if user:
                session['h_ref'] = user.referral_code
        except:
            pass
    return redirect(url_for('main.sign_up'))

def handle_ip(ip_address, user):
    # Prevent someone from gaming the site by referring themselves.
    # Presumably, users are doing this from the same device so block
    # their ip after their ip appears three times in the database.
    curr_ip = IPAddress.query.filter_by(address=ip_address).first()
    if not curr_ip:
        newIP = IPAddress(address=ip_address)
        db.session.add(newIP)
        db.session.commit()
    elif curr_ip.count > 2:
        user.repeat_ip = True
        flash('IP address has already appeared too many times times in our records.')
        db.session.commit()
        #return abort(403)
        return redirect(url_for('main.landing_page'))
    else:
        curr_ip.count = curr_ip.count + 1
        db.session.commit()


@main.route('/signup', methods=['GET','POST'])
def sign_up():
    form = ContestForm()
    if form.validate_on_submit():
        session['h_email'] = form.email.data
        # get user ip. If there is a proxy in front of Flask, then something like this will get the real ip
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr
        user = User(email=form.email.data, ip_address=ip_address)
        user.generate_ref()
        db.session.add(user)
        db.session.commit()
        #send email in production only
        if current_app.config['DEBUG'] == False:
            send_email(user.email, user.referral_code)
        handle_ip(ip_address, user)   
        if 'h_ref' in session:
            referral_code = session['h_ref']
            try:
                referring_user = User.query.filter_by(referral_code=referral_code).first()
                if referring_user:
                    # increment referring users count
                    referring_user.referrals += 1
                    db.session.commit()

                    # get or create referral codes in db
                    refer = Referrer.query.filter_by(referral_code=referral_code).first()
                    if refer:
                        user.referrer = refer.id
                        db.session.commit()
                        if referring_user.repeat_ip:
                            user.repeat_ip = True
                            db.session.commit()
                    else:
                        referrer = Referrer(referral_code=referral_code)
                        db.session.add(referrer)
                        db.session.commit()

            except Exception as e:
                print e
                session.pop('h_ref', None)
        return redirect(url_for('main.refer'))
    else:
        flash_errors(form)
    return render_template('signup.html', form=form)


@main.route('/refer', methods=['GET'])
def refer():
    if 'h_email' in session:
        try:
            email = session['h_email']
            user = User.query.filter_by(email=email).first_or_404()
            if user:
                referral_code = user.referral_code
                referrals = user.referrals

        except:
            session.pop('h_email', None)
            redirect(url_for('main.landing_page'))
    else:
        return redirect(url_for('main.landing_page'))
    
    return render_template('refer.html', referral_code=referral_code, referrals=referrals)