from ClearmindBase.databaseOperator import sqlOperator

a = sqlOperator()

a.active()

def menu():
    print('0. 退出')
    print('1. 增加邀请码')
    print('2. 查看可用邀请码')

while True:
    menu()
    op = int(input('请输入选项:'))
    if op == 0: break
    elif op == 1:
        num = int(input('请输入增加数量(最大10)'))
        num = min(10, num)
        a.add_invite_code(num)
        print('ok')
    elif op == 2:
        for each in a.get_invite_code():
            print(each['code'])