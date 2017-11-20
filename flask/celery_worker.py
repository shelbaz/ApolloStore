
from project.controllers.cart import CartController
from project import celery



celery.conf.beat_schedule = {
    'arbitrary-name': {
        'task': 'cart_timeout',
        'schedule': 5,
    },
}
