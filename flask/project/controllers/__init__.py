# --------------------------------------------------------------------
# Whenever you want to create a package in Python, you must create a
# directory with an __init__.py inside, even if it's empty.
# --------------------------------------------------------------------

from project import celery


# Defines a Celery task that can be called by a Celery worker
@celery.task(name='printer')
def printer(number_argument):
    print('Celery: I\'m just printing some stuff every 30 seconds. The argument passed is: ' + str(number_argument))
