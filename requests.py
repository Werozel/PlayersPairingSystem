
update_user = "update users set name = %s, last_name = %s, age = %s, gender = %s," \
                  " admined_groups = %s, sport = %s, login = %s, psw = %s, groups = %s, last_login = %s where id = %s"

upload_user = "insert into users(id, name, last_name, age, gender, " \
              "admined_groups, sport, login, psw, groups, last_login) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

get_user = "select * from users where id = %s"

delete_user = "delete from users where id = %s"

check_user_login = "select id from users where login = %s"

update_user_time = "update users set last_login = %s where id = %s"


update_group = "update groups set admin_id = %s, sport = %s, members = %s where id = %s"

upload_group = "insert into groups(id, admin_id, sport, members) " \
                   "values (%s, %s, %s, %s)"

get_group = "select * from groups where id = %s"

delete_group = "delete from groups where id = %s"


login = "select * from users where login = %s and psw = %s"


show_groups = "select * from groups where sport = %s"
