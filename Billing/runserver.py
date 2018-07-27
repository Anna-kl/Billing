"""
This script runs the Billing application using a development server.
"""

from os import environ
from Billing import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    PORT=5500
    app.run(HOST, PORT)
