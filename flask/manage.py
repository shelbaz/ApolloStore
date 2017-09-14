
from project import create_app, logger


logger.info('Server has started.')


app = create_app()


if __name__ == '__main__':
    app.run()
