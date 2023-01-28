#求向廳數函式：get_sht
#取雀頭函式：get_twice
#取刻順函式：get_three
#取刻順'函式：get_lack_three

#######################################
# K=(N-2)/3 其中N為手牌數
# P= 0(不存在雀頭): 1(有雀頭)
# G=刻子+順子的數量和
# G_pron=刻子'+順子'的數量和 其中'表示缺一張
# S=2(K-G)-G'-P 表示向聽數
#######################################
# def get_distance(x,y):
#     if abs(int(x[0])-int(y[0]))==1:
        
# def get_sht(tiles):
#   S = 8
#   C_max = 0
#   get_twice(tiles, len(tiles), S, C_max, (len(tiles)-2)/3)
#   return S

# def get_twice(tiles, C_rem, S, C_max, K):

#   for head in 取雀头迭代器(tiles):
#     get_three(tiles-head, 0, C_rem-2, S, C_max, K, 1, 0)
#   get_three(tiles, 0, C_rem, S, C_max, K, 0, 0)

# def get_three(tiles, i, C_rem, S, C_max, K, P, G):
#   if i==len(tiles):
#     get_lack_three(tiles, 0, C_rem, S, C_max, K, P, G, 0)
#     return
  
#   g = 取一个刻子或顺子(tiles)
#   if g!=0:
#     get_three(tiles-g, i, C_rem-3, S, C_max, K, P, G+1)
  
#   get_three(tiles, i+1, C_rem, S, C_max, K, P, G)


# def get_lack_three(tiles, i, C_rem, S, C_max, K, P, G, G_pron):
#   if S==-1:return
#   if G+G_pron>N:return
#   C = 3*G+2*G_pron+2*P
#   if C_rem<C_max-C:return
#   if C_rem==0:
#     S = min(S, 2*(K-G)-G_pron-P)
#     C_max = max(C_max, C)
#     return
  
#   g = 取一个刻子或顺子’(tiles)
#   if g!=0:
#     get_lack_three(tiles, i, C_rem-2, S, C_max, K, P, G, G_pron+1)
  
#   get_lack_three(tiles-tiles[i], i+1, C_rem-len(tiles[i]), S, C_max, K, P, G, G_pron)

# tiles={"1m":3,"2m":1,"3m":1,"5m":1,"6m":1,"4p":1,"5p":1,"6p":1,"7s":1,"8s":1,"1z":2}
import math
def distance(a,b):
  if a[-1]!=b[-1]: return math.inf
  dis=abs(int(a[0])-int(b[0]))
  if dis>2: return math.inf
  else: return dis
kinds=['m','p','s','z']
handcards=input("請輸入手牌\n") #手牌會長:123m-34555p-5567s-11z
piles=handcards.split('-')
handcards=''
handcards_pile={'cards':{},'distance':[]} #這裡會長:{'cards':{'1m': 1, '2m': 1, '3m': 3, '3p': 1, '4p': 2, '5p': 1, '7s': 1, '8s': 2, '3z': 1},
# distance:[1,1,inf,1,1,inf,1,inf]}
for pile in piles:
  for k in kinds:
    if pile[-1]==k:
      num=pile[0:-1]
      for n in num:
        name=n+k
        if name not in handcards_pile['cards']: handcards_pile['cards'][name]=1
        else:handcards_pile['cards'][name]+=1
card_list=list(handcards_pile['cards'])
for idx in range(len(card_list)-1):
  handcards_pile['distance'].append(distance(card_list[idx],card_list[idx+1]))
print(handcards_pile)
