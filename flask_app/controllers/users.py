from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session, flash


BCRYPT = Bcrypt(app)


@app.route('/')
def r_landing():
    if 'user_id' in session:
        redirect('/wall')
    return render_template('landing.html')


@app.route('/register', methods=['POST'])
def f_register():
    if not User.validate_registration(request.form):
        print('Invalid registration')
        return redirect('/')

    print('Valid registration')
    registration_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': BCRYPT.generate_password_hash(request.form['password'])
    }

    session['user_id'] = User.register_user(registration_data)

    return redirect('/')


@app.route('/login', methods=['POST'])
def f_login():
    login_data = {
        'email': request.form['email_login'],
        'password': request.form['password_login']
    }
    user = User.check_for_email(login_data)
    if not user or not BCRYPT.check_password_hash(user.password, request.form['password_login']):
        flash('* Invalid Email or Password.')
        return redirect('/')

    session['user_id'] = user.id
    print(session['user_id'])
    return redirect('/')