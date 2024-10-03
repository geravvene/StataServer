from flask import Flask, request

import db
app = Flask(__name__)
last_date=0


@app.route("/")
def main():
    return "Это просто сервер."

@app.route('/add/<name>', methods=['POST'])
def success(name):
    if request.method == 'POST':
        global last_date
        last_date=db.add(request.json.get('content', None), name, last_date)
        return "Nice"

if __name__ == '__main__':
  app.run(port=443)
