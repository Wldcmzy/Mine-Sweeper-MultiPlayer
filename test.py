from ClearmindBase.dababaseOperator import sqlOperator

a = sqlOperator()

a.active()
print(a.add_invite_code(5))
print(a.test_select())