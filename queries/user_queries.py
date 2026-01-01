from extensions import db
from models.result import ResultMessage
from models.user import User


class UserQueries:

    def get_user_by_name(self, name):

        try:

            print("=================> Getting user by name")

            requested_user = User.query.filter_by(name=name).all()

            if len(requested_user) == 0:
                result = ResultMessage(None, "error", f"No user found with name {name}", 404)
                print(result.message)
                print("======================> Finished getting user by name")
                return result

            else:
                result = ResultMessage(requested_user[0], "success", f"User with that name {name} found", 200)
                print(result.message)
                print("======================> Finished getting user by name")
                return result


        except Exception as e:
            result = ResultMessage("", "error", f"Error getting user by name {e}", 500)
            print(result.message)
            return result


    def add_user(self, new_user):

        try:

            print("=================> Adding new user")

            checking_user_result = self.get_user_by_name(new_user.name)

            if checking_user_result.data is None:
                print(f"=============> new_user{new_user} is not registered")
                db.session.add(new_user)
                db.session.commit()

                print("====================> Finished adding new user")

                result = ResultMessage(new_user, "success", f"New user added successfully", 200)
                print(result.message)
                return result

            else:
                result = ResultMessage("", "error", f"User with that name {new_user.name} already exists", 500)
                print(result.message)
                return result

        except Exception as e:
            result = ResultMessage("", "error", f"Error adding user {e}", 500)
            print(result.message)
            return result