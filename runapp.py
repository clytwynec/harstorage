import os

from paste.deploy import loadapp
from paste import httpserver

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = loadapp('config:production.ini', relative_to='.')

    httpserver.serve(app, host='0.0.0.0', port=port)
