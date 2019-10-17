from Users import User
import globals

print(User.get_valid_id())
User(name="Jej", last_name="Guk", age=20, sex="M").upload_user()

globals.finish()
