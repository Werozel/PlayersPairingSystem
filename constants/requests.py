
update_user = "update users set name = %s, last_name = %s, age = %s, gender = %s," \
                  " admined_groups = %s, sport = %s, username = %s, password = %s, groups = %s, last_login = %s where id = %s"

upload_user = "insert into users(id, name, last_name, age, gender, " \
              "admined_groups, sport, username, password, groups, last_login) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

get_user = "select * from users where id = %s"

delete_user = "delete from users where id = %s"

check_user_login = "select id from users where username = %s"

update_user_time = "update users set last_login = %s where id = %s"


update_group = "update groups set admin_id = %s, sport = %s, members = %s, name = %s where id = %s"

upload_group = "insert into groups(id, admin_id, sport, members, name) " \
                   "values (%s, %s, %s, %s, %s)"

get_group = "select * from groups where id = %s"

get_all_groups = "select id from groups"

delete_group = "delete from groups where id = %s"


login = "select * from users where username = %s and password = %s"


show_groups = "select * from groups where sport = %s"
