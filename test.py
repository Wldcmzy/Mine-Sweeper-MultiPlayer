from ClearmindBase.dababaseOperator import sqlOperator

a = sqlOperator()

a.active()
# print(a.add_invite_code(5))
# print(a.test_select())
print(a.select_by_user('wowowo'))
print(a.select_by_user('ninini'))
# print(a.register('test', 'wowowo', 'qweqwe'))