from main import create_app

from threading import Lock
from flask import session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

if __name__=='__main__':
    
    app = create_app()

    class MyNamespace(Namespace):
        ### Explore page
        # If a user is interested
        def on_interested_user(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            username = message['username']
            profilepic = message['profilepic']
            print(f'\n\n\n{username} : {profilepic}\n\n\n')
            emit('interest_update',
                {'username': message['username'], 'profilepic' : message['profilepic'], 'event_id' : message['eventID'], 'count': session['receive_count']} , broadcast=True )

        def on_uninterested_user(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            username = message['username']
            profilepic = message['profilepic']
            print(f'\n\n\n{username} : {profilepic}\n\n\n')
            emit('uninterest_update',
                {'username': message['username'], 'profilepic' : message['profilepic'], 'event_id' : message['eventID'], 'count': session['receive_count']} , broadcast=True )

        def on_this_bitch(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            print('\n\n\ntHIS BITCH CRAZY\n\n\n')
            emit('my_response',
                {'data': message['data'], 'count': session['receive_count']} , broadcast=True )

        def on_my_event(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': message['data'], 'count': session['receive_count']})

        def on_my_broadcast_event(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': message['data'], 'count': session['receive_count']},
                broadcast=True)

        def on_join(self, message):
            join_room(message['room'])
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': 'In rooms: ' + ', '.join(rooms()),
                'count': session['receive_count']})

        def on_leave(self, message):
            leave_room(message['room'])
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': 'In rooms: ' + ', '.join(rooms()),
                'count': session['receive_count']})

        def on_close_room(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                                'count': session['receive_count']},
                room=message['room'])
            close_room(message['room'])

        def on_my_room_event(self, message):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': message['data'], 'count': session['receive_count']},
                room=message['room'])

        def on_disconnect_request(self):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response',
                {'data': 'Disconnected!', 'count': session['receive_count']})
            disconnect()

        def on_my_ping(self):
            emit('my_pong')

        def on_connect(self):
            global thread
            with thread_lock:
                if thread is None:
                    thread = socketio.start_background_task(background_thread)
            emit('my_response', {'data': 'Connected', 'count': 0})

        def on_disconnect(self):
            print('Client disconnected', request.sid)

    socketio = SocketIO(app, async_mode=None)
    thread = None
    thread_lock = Lock()

    socketio.on_namespace(MyNamespace('/'))

    socketio.run(app, debug =True)