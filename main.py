from flask import Flask, request
from datetime import datetime

import db
app = Flask(__name__)
last_date=datetime(2024,10,2,10,13,22)


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
