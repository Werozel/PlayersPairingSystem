from Users import User
import globals

u = User(id=4, sex="F")
u.print()
u.update_user()
u.print()

globals.finish()
