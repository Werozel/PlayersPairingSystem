
update_user_req = "update users set name = %s, last_name = %s, age = %s, sex = %s," \
                  " admined_groups = %s, sport = %s where id = %s"

upload_user_req = "insert into users(id, name, last_name, age, sex, admined_groups, sport) " \
                  "values (%s, %s, %s, %s, %s, %s, %s)"

get_user_req = "select * from users where id = %s"

delete_user_req = "delete from users where id = %s"


update_group_req = "update groups set admin_id = %s, sport = %s, users = %s where id = %s"

upload_group_req = "insert into groups(id, admin_id, sport, users) " \
                   "values (%s, %s, %s, %s)"

get_group_req = "select * from groups where id = %s"

delete_group_req = "delete from groups where id = %s"
