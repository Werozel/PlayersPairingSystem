from Users import User
import globals

print(User.get_valid_id())
User(id=5, name="Jej", last_name="Guk", age=20, sex="M").upload()

globals.finish()
