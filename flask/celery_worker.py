
from project.controllers import printer
from project import celery


# Schedules task using Celery's beat scheduler
celery.conf.beat_schedule = {
    'arbitrary-name': {
        'task': 'printer',
        'schedule': 30,
        'args': (6,)
    },
}
