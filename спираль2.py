"""
Выведите таблицу размером n×n, заполненную числами от 1 до n^2 по спирали, выходящей из левого верхнего угла и закрученной по часовой стрелке
"""

n=int(input())
mat=[[(n*i)+j+1 for j in range(n)] for i in range(n)]
f=0
d=n-1
l=0
r=n-1
k=0
while f<=d and l<=r:
    if l<=r: #вправо
        for j in range(l,r+1):
            if k==n*n:
                mat[f][j] = k
            else:
                k+=1
                mat[f][j]=k
        f+=1
    if f<=d: #вниз
        for i in range(f,d+1):
            if k==n*n:
                mat[i][r] = k
            else:
                k+=1
                mat[i][r]=k
        r-=1
    if r>=l: #влево
        for j in range(r,l-1,-1):
            if k==n*n:
                mat[d][j] = k
            else:
                k+=1
                mat[d][j]=k
        d-=1
    if d>=f: #вверх
        for i in range(d,f-1,-1):
            if k==n*n:
                mat[i][l] = k
            else:
                k+=1
                mat[i][l]=k
        l+=1
for x in mat:
    print(" ".join(map(str,x)))
