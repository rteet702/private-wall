from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask import render_template, redirect, session, request, flash

@app.route('/wall')
def r_wall():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {'id': session['user_id']}

    other_users = User.get_all_other_users(user_data)
    user = User.find_by_id(user_data)
    messages_for_user = Message.get_message_to_user(user_data)

    return render_template('wall.html', user=user, other_users=other_users, messages=messages_for_user, count=len(messages_for_user))


@app.route('/logout')
def f_logout():
    session.clear()
    return redirect('/')


@app.route('/deletemessage/<int:id>')
def f_delete_message(id):
    message_data = {
        'id' : id
    }
    message = Message.find_message_by_id(message_data)
    if int(message.recipient_id) != session['user_id']:
        flash(f'AHHHHH STOP TRYING TO HACK MY SHIT YOU LOSER\nTHIS IS NOT A WARNING\nMessage {message.id} is not yours to delete.', 'hacker')
        return redirect('/danger')

    Message.delete_message(message_data)
    return redirect('/wall')


@app.route('/sendmessage', methods=['POST'])
def f_send_message():
    message_data = {
        'author_id' : session['user_id'],
        'recipient_id' : request.form.get('target_user'),
        'content' : request.form.get('message_content')
    }
    Message.create_message(message_data)
    return redirect('/wall')