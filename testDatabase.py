from ClearmindBase.dababaseOperator import sqlOperator

a = sqlOperator()

a.active()

#print(a.select_invitation_userID('aaa'))
#print(a.select_invitation_userID('ninini'))
#print(a.select_invitation_ifUsed('aaa'))
#print(a.select_invitation_ifUsed('ggg'))
#print(a.update_invitation_ifUsed('aaa',0))
#print(a.update_invitation_ifUsed('aaa',0))

#user = { 'userID':'101','username':'xiaohua','passwd':'111'}
#print(a.insert_serInfo_uAp(user))
#user = { 'username':'xiaohua','passwd':'777'}
#print(a.update_userInfo_uAp('101',user))
#print(a.select_userInfo_uAp('101'))
#print(a.select_userInfo_ifOnline('xiaohua'))
#print(a.update_userInfo_ifOnline('xiaohua',0))
#print(a.select_userInfo_ifOnline('xiaohua'))
#print(a.select_userInfo_clearCount('xiaohua'))
#print(a.select_userInfo_clearCount('hua'))
#print(a.update_userInfo_clearCount('xiaohua',5))
#print(a.select_userInfo_clearCount('xiaohua'))
#print(a.update_userInfo_clearCount('hua',5))
print(a.update_userInfo_boomCount('xiaohua',15))
print(a.select_userInfo_boomCount('xiaohua'))
print(a.update_userInfo_boomCount('hua',5))