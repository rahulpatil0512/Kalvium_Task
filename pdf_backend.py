# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
pdf_page = 1
lock = Lock()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('page_update', {'page': pdf_page}, room=room)

@socketio.on('change_page')
def on_change_page(data):
    global pdf_page
    new_page = data['page']
    with lock:
        pdf_page = new_page
    emit('page_update', {'page': pdf_page}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
