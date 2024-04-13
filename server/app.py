#!/usr/bin/env python3

from flask import request, session,jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe


class Signup(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url')
        bio = data.get('bio')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 422

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 422

        # Create a new user
        new_user = User(username=username, password_hash=password,
                        image_url=image_url, bio=bio)
        db.session.add(new_user)
        db.session.commit()

        # Save user ID in session
        session['user_id'] = new_user.id

        # Prepare response
        user_data = {
            "id": new_user.id,
            "username": new_user.username,
            "image_url": new_user.image_url,
            "bio": new_user.bio
        }

        return jsonify(user_data), 201


api.add_resource(Signup, '/signup')

class CheckSession(Resource):
    pass

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)