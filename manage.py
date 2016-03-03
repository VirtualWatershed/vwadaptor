#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from flask_migrate import MigrateCommand

from celery.bin.celery import main as celery_main

from vwadaptor.app import create_app
from vwadaptor.user.models import User
from vwadaptor.modelrun.models import ModelRun
from vwadaptor.settings import DevConfig, ProdConfig
from vwadaptor.database import db

if os.environ.get("VWADAPTOR_ENV") == 'prod':
    config = ProdConfig
else:
    config = DevConfig
app = create_app(config)
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User,'ModelRun':ModelRun}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def celeryworker():

    celery_args = ['celery', 'worker', '-n', config.CELERY_WORKER_NAME, '-C',
                    '--autoscale={max},{min}'.format(max=config.CELERY_SCALE_MAX,min=config.CELERY_SCALE_MIN),
                    '--without-gossip']
    with app.app_context():
        return celery_main(celery_args)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
