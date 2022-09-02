from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session


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