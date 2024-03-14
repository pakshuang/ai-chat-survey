import os

from flask import Flask

BACKEND_CONTAINER_PORT = os.getenv("BACKEND_CONTAINER_PORT", "5000")

app = Flask(__name__)

@app.route('/dummy')
def dummy_route():
    return 'Hello, this is the dummy route!'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=BACKEND_CONTAINER_PORT)