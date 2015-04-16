from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!\n'

@app.route('/333')
def swag_world():
    return 'Just as planned\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3333)
