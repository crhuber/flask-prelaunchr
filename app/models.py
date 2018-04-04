from flask import current_app, request, url_for, abort
from datetime import datetime
from time import time
from hashlib import md5
from . import db
import os
from binascii import hexlify


class Referrer(db.Model):
    __tablename__ = 'referrer'

    id = db.Column(db.Integer, primary_key=True)
    referral_code = db.Column(db.String(18))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    referral_code = db.Column(db.String(10), unique=True)
    referrer =  db.Column(db.Integer, db.ForeignKey('referrer.id'), nullable=True)
    repeat_ip = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(10))
    referrals = db.Column(db.Integer, default=0)
    
    def generate_ref(self):
        if not self.referral_code:
            new_code = hexlify(os.urandom(4))
            collision = User.query.filter_by(referral_code=new_code).first()
            while collision:
                new_code = hexlify(os.urandom(4))
                collision = User.query.filter_by(referral_code=new_code).first()
            self.referral_code = new_code


class IPAddress(db.Model):
    __tablename__ = 'ip_adddress'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120),unique=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

