from models import User, db, check_password_hash, user_schema, loggedin_user_schema
from flask import Blueprint, request, flash, jsonify

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# New user sign up
@auth.route('/signup', methods = ['POST'])
def signup():
    try:
        first_name = request.json['first_name']
        email = request.json['email']
        password = request.json['password']

        user = User(first_name, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully createed a user account {email}', 'User-created')
        response = user_schema.dump(user)
        return jsonify(response)
            
    except:
        raise Exception('Invalid form data: Please check your form')

@auth.route('/signin', methods=['POST'])
def signin():
    try:
        email = request.json['email']
        password = request.json['password']

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            flash('You have successfully logged in!', 'auth-success')
            response = loggedin_user_schema.dump(logged_user)
            return jsonify(response)
        else:
            flash('Login failed.', 'auth-failed')
            return jsonify({'message': 'Login failed'})
    except:
        raise Exception('Error: please check that your form data is correct')