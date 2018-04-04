#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, IPAddress, Referrer
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)