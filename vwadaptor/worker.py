import os
from celery import Celery

from vwadaptor.settings import DevConfig, ProdConfig

if os.environ.get("VWADAPTOR_ENV") == 'prod':
    config = ProdConfig
else:
    config = DevConfig

celery= Celery('vwadaptor',
                broker=config.CELERY_BROKER_URL,
                backend=config.CELERY_RESULT_BACKEND)
