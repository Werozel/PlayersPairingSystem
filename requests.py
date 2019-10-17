
update_user_req = "update users set name = %s, last_name = %s, age = %s, gender = %s," \
                  " admined_groups = %s, sport = %s, login = %s, psw = %s, groups = %s where id = %s"

upload_user_req = "insert into users(id, name, last_name, age, gender, admined_groups, sport, login, psw, groups) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

get_user_req = "select * from users where id = %s"

delete_user_req = "delete from users where id = %s"


update_group_req = "update groups set admin_id = %s, sport = %s, members = %s where id = %s"

upload_group_req = "insert into groups(id, admin_id, sport, members) " \
                   "values (%s, %s, %s, %s)"

get_group_req = "select * from groups where id = %s"

delete_group_req = "delete from groups where id = %s"


login_req = "select * from users where login = %s and psw = %s"


show_groups_req = "select * from groups where sport = %s"
