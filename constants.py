
update_user_req = "update users set id=%s, name=%s, last_name=%s, age=%s, sex=%s," \
                  " admined_groups=%s, sport=%s"

upload_user_req = "insert into users(id, name, last_name, age, sex, admined_groups, sport) " \
                  "values (%s, %s, %s, %s, %s, %s, %s)"

get_user_req = "select * from users where id = %s"

delete_user_req = "delete from users where id=%s"
