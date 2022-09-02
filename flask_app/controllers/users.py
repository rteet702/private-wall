from flask_app import app
from flask_app.models.user import User
from flask import render_template, request, redirect


@app.route('/')
def r_landing():
    return render_template('landing.html')

@app.route('/register', methods=['POST'])
def f_register():
    if User.validate_registration(request.form):
        print('Valid registration')
    else:
        print('Invalid registration')
    return redirect('/')