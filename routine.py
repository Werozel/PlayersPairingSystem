from Users import User
from Groups import Group
import globals

u1 = User.get(1)
u2 = User.get(2)
u3 = User.get(3)
g = Group(id=1, admin=u1, sport="Tennis", members=[u1, u2, u3])
g.upload()
g1 = Group.get(1)
g1.print()
Group.remove(g1.id)

globals.finish()
