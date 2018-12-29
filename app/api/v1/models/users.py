from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
USERS_LIST = []

class Users():
    def put(self, name, username, email, password):
        self.single_user = {}

        email_data = [user for user in USERS_LIST if user["email"] == email]
        username_data = [user for user in USERS_LIST if user["username"] == username]

        if "message" not in email_data:
             return {"message": "Email already exists"}
        if "message" not in username_data:
            return {"message": "Username already exists"}

        self.single_user["name"] = name
        self.single_user["username"] = username
        self.single_user["email"] = email
        self.single_user["password"] = password

        USERS_LIST.append(self.single_user)

        return {"message": "User with username {} added succesfully".format(username)}

    def password_validation(self, username, password):
        user = [user for user in USERS_LIST if user["username"] == username]
        if "message" not in user:
            valid = check_password_hash(
                user['password'], password)
            if valid:
                return "True"
            return {"message": "The password you entered is incorrect"}
        return user

    def get_user_by_username(self, username):
        user = [user for user in USERS_LIST if user["username"] == username]
        if "message" not in user:
            return user
        return {"message": "User is not our  in record"}

    def get_all_users(self):
        return USERS_LIST
