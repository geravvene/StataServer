from flask import Flask, request

import db
app = Flask(__name__)


@app.route("/")
def main():
    return "Это просто сервер."

@app.route('/add/<name>', methods=['POST'])
def success(name):
    if request.method == 'POST':
      
        db.add(request.json.get('content', None), name)
        
        
        return "Nice"

if __name__ == '__main__':
  app.run(port=443)
