from Users import User
import globals

u = User(id=3, name="Vladimir", last_name="Abramov", age=70, sex="M")
u.upload_user()

globals.finish()
