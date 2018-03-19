from flask_socketio import SocketIO,emit,join_room
from flask import Flask, render_template, request, session,redirect,url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = 'windroc-nwpc-project'

app.debug = True
socketio = SocketIO(app)


@app.route('/',methods=['POST','GET'])
def get_index_page():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('user')
        session['user'] = name
        return redirect(url_for('get_chat_page'))
    return render_template('name.html')


@app.route('/chat')
def get_chat_page():
    return render_template('test.html')


@socketio.on('text', namespace='/test')
def chat_text(data):
    room = data['room']
    user = session['user']
    # 发送给在room下的所有人
    emit('message', {'content': data['msg'], 'user': user}, room=room)



@socketio.on('enter_room', namespace='/test')
def joined(data):
    room = data['room']
    print('前端room',data['room'])
    join_room(room)
    emit('status', {'room': data['room'], 'user': session['user']})


if __name__ == "__main__":
    socketio.run(app, port=5101)