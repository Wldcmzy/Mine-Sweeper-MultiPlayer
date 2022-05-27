map = [ ['']*1000 for i in range(1000) ]
cell = [ [0]*1000 for i in range(1000) ]
who = [ [0]*1000 for i in range(1000) ]

user_scan = [0]*100
user_boom = [1]*100

dx = [-1,-1,-1,0,1,1,1,0]
dy = [-1,0,1,1,1,0,-1,-1]

MOD = 998244353

def one(x,y,I,J,now,PART_SIZE_N,PART_SIZE_M):
    xx = (now % PART_SIZE_N) + 1
    now = now // PART_SIZE_N
    yy = (now % PART_SIZE_M) + 1
    cell[x+I][y+J], cell[xx+I][yy+J] = cell[xx+I][yy+J],cell[x+I][y+J]

def distirbute(N,PART_SIZE,MINE_NUM,SEED):
    for I in range(0,N,PART_SIZE):
        for J in range(0,N,PART_SIZE):
            tag = 0
            PART_SIZE_N = PART_SIZE
            PART_SIZE_M = PART_SIZE
            MINE_NUM_NM = MINE_NUM
            if I+PART_SIZE_N > N :
                PART_SIZE_N = N-I
                tag = 1
            if J+PART_SIZE_M > N :
                PART_SIZE_M = N-J
                tag = 1
            if tag == 1:
                MINE_NUM_NM=PART_SIZE_N*PART_SIZE_M*MINE_NUM//(PART_SIZE*PART_SIZE)
                  
            iter = 0
            for i in range(1,PART_SIZE_N+1):
                for j in range(1,PART_SIZE_M+1):
                    cell[I+i][J+j]=iter
                    iter+=1
            fib1=1
            fib2=2
            now = SEED
            SEED=(SEED*SEED)%MOD
            for i in range(1,PART_SIZE_N+1):
                for j in range(1,PART_SIZE_M+1):
                    tmp = (fib1 + fib2) % MOD
                    fib1 = fib2
                    fib2 = tmp
                    now = now * fib1 % MOD
                    one(i, j,I,J,now,PART_SIZE_N,PART_SIZE_M) 
            for i in range(1,PART_SIZE_N+1):
                for j in range(1,PART_SIZE_M+1):
                    if cell[I+i][J+j] < MINE_NUM_NM :
                        map[I+i][J+j]='M'
                    else:
                        map[I+i][J+j]=' '
    for i in range(1,N+1):
        for j in range(1,N+1):
            if map[i][j] == ' ':
                cnt = 0
                for k in range(8):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if nx >= 1 and nx <= N and ny >=1 and ny<=N:
                        cnt += map[nx][ny] == 'M'
                if cnt >0:
                    map[i][j]=cnt

def dfs(x,y,user,N):
    user_scan[user] += 1
    who[x][y] = user
    if map[x][y] == ' ':
        for k in range(8):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx >= 1 and nx <= N and ny >=1 and ny<=N:
                if map[nx][ny] != 'M' and who[nx][ny] == 0:
                    dfs(nx,ny,user,N)
    else:
        for k in range(8):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx >= 1 and nx <= N and ny >=1 and ny<=N:
                if map[nx][ny] == ' ' and who[nx][ny] == 0:
                    dfs(nx,ny,user,N)

def sweeper(x,y,user,N):
    if map[x][y] == 'M':
        user_boom[user] += 1
        who[x][y] = user
    dfs(x,y,user,N)

distirbute(10,5,6,777)
for i in range(1,10+1):
    for j in range(1,10+1):
        print(map[i][j],end=" ")
    print()
sweeper(4,2,1,10)
for i in range(1,10+1):
    for j in range(1,10+1):
        print(who[i][j],end=" ")
    print()
print(user_scan[1])
print(user_boom[1])