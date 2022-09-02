from flask_app import app
from flask_app.models.user import User
from flask import render_template, redirect, session

@app.route('/wall')
def r_wall():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {'id': session['user_id']}

    other_users = User.get_all_other_users(user_data)
    user = User.find_by_id(user_data)
    return render_template('wall.html', user=user, other_users=other_users)

@app.route('/logout')
def f_logout():
    session.clear()
    return redirect('/')