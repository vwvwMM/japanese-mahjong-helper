from get_cards import lines,WHITE,ALL_CARDS
import json
has_word_degree=630
no_tile_degree=230
shift=[58,0]#58 for real
my_card_short=71
turn_position=[[1025+shift[0],515],[910+shift[0],425],[780+shift[0],515],[900+shift[0],617]]
mo_position=[[1415+shift[0],250],[730+shift[0],93],[390+shift[0],690],[1340+shift[0],905]]
river_position=[[1053+shift[0],618],[1006+shift[0],403],[747+shift[0],450],[796+shift[0],675]]
handcard_position=[380+shift[0]+my_card_short*x for x in range(14)]
handcard_position[13]+=4
HC_LEN=14
ACCURATE=16
river_cards=[0,0,0,0]
mo_distance=[54,63,-53,-106]
riichi_distance=[-11,-15,11,15]
card_short=[-35.5,-42.5,35.5,41]
card_long=[56,-47,-56,46]


def has_tile(color):
    if sum(color)>WHITE:
        return True
    elif sum(color)<no_tile_degree and color[2]>70:
        return False
def has_word(color):
    if sum(color)>has_word_degree:
        return True
    return False
def whose_turn(array):
    for idx,pos in enumerate(turn_position):
        if array[pos[1]][[pos[0]]][0][1]>100:
            return idx
    return None
def is_jkan(array,now_player,fulu):
    if fulu=='kan':
        if now_player==1 or now_player==3:
            if has_tile(array[mo_position[now_player][1]][mo_position[now_player][0]+mo_distance[now_player]]): return True
        else :
            if has_tile(array[mo_position[now_player][1]+mo_distance[now_player]][mo_position[now_player][0]]): return True
        return False
    return False
def recog_card(whole_pic):
    if has_tile(whole_pic[mo_position[3][1]][handcard_position[HC_LEN-1]+2]):
        with open('cards.json', 'r') as openfile:
            # Reading from json file
            cards_images = json.load(openfile)
            hc = [0 for x in range(HC_LEN)]
            for i in range(HC_LEN-1):
                start_idx= ALL_CARDS.index(hc[i-1]) if (i>0 and hc[i-1]!=0) else 0
                for prob in range(start_idx,len(ALL_CARDS)):
                    c=ALL_CARDS[prob]
                    unaccu=0
                    for line_name,line in lines.items():
                        for x in range(4,68):
                            if (x in cards_images[c[1]][int(c[0])-1][line_name] and sum(whole_pic[line][x+handcard_position[i]])<WHITE) or (x not in cards_images[c[1]][int(c[0])-1][line_name] and sum(whole_pic[line][x+handcard_position[i]])>WHITE): 
                                unaccu+=1
                            if c[0]!='5' and c[0]!='6': 
                                if unaccu>ACCURATE: break
                    if unaccu<ACCURATE:
                        hc[i]=c
                        break
            for c in ALL_CARDS:
                unaccu=0
                for line_name,line in lines.items():
                    for x in range(4,68):
                        if ((x in cards_images[c[1]][int(c[0])-1][line_name]) and (sum(whole_pic[line][x+handcard_position[HC_LEN-1]])<WHITE)) or ((x not in cards_images[c[1]][int(c[0])-1][line_name]) and (sum(whole_pic[line][x+handcard_position[HC_LEN-1]])>WHITE)):
                            unaccu+=1
                            if unaccu>ACCURATE: break
                    if unaccu>ACCURATE: break
                else:
                    hc[HC_LEN-1]=c
                    break
            str_hc=['m','p','s','z']
            for c in hc:
                if c==0: return ''
                for idx,t in enumerate(str_hc):
                    if c[1]==t[-1]: str_hc[idx]=str_hc[idx][0:-1]+c[0]+c[1]
            return ''.join(str_hc)
    else: return ''
def check_mo(array,now_player,fulu):
    global river_cards,river_position
    river_x=round(river_position[now_player][1])
    river_y=round(river_position[now_player][0])
    mo_x=round(mo_position[now_player][1])
    mo_y=round(mo_position[now_player][0])
    mo=array[mo_x][mo_y]
    riv=array[river_x][river_y]
    if (handcard_position[HC_LEN-1]-380-shift[0])%my_card_short==0:
        handcard_position[HC_LEN-1]+=4
    if not has_tile(riv) and not fulu:
        return None
    else:
        river_cards[now_player]+=1
        if river_cards[now_player]%6==0:
            if now_player==1 or now_player==3:
                river_position[now_player][1]+=card_long[now_player]
                if now_player==1:
                    river_position[now_player][0]=1006+shift[0]
                else:
                    river_position[now_player][0]=796+shift[0]
            else:
                river_position[now_player][0]+=card_long[now_player]
                if now_player==0:
                    river_position[now_player][1]=618
                elif now_player==2:
                    river_position[now_player][1]=450
        else:                
            if now_player==1 or now_player==3:
                river_position[now_player][0]+=card_short[now_player]
                if fulu=='riichi':
                    river_position[now_player][0]+=riichi_distance[now_player]
            else:
                river_position[now_player][1]+=card_short[now_player]
                if fulu=='riichi':
                    river_position[now_player][1]+=riichi_distance[now_player]
        if has_tile(mo):
            return False
        else:
            return True

def check_fulu(array,now_player,ex_player):
    global mo_position,river_position,river_cards
    fulu=None
    if now_player==0: #y axis is 495
        y=495
        # pon_position=[[1190,1239]]
        # kan_position=[[1191,1205],[1232,1250]]
        # chii_position=[[1203,1241],[1266,1279],[1330,1343],[1359,1372]]
        # riichi_position=[[1147,1200],[1223,1235],[1251,1264],[1338,1351],[1402,1415]]
        if has_word(array[y][1160+shift[0]]) and has_word(array[y][1410+shift[0]]):
            fulu='riichi'
        elif has_word(array[y][1220+shift[0]]) and has_word(array[y][1335+shift[0]]):
            fulu='chii'
        elif has_word(array[y][1245+shift[0]]) and has_word(array[y][1200+shift[0]]):
            fulu='kan'
        elif has_word(array[y][1235+shift[0]]) and has_word(array[y][1195+shift[0]]):
            fulu='pon'
    elif now_player==1: #y axis is 170
        y=170
        # pon_position=[[810,858]]
        # kan_position=[[811,825],[853,871]]
        # chii_position=[[822,863],[886,900],[950,963],[980,992]]
        # riichi_position=[[767,817],[842,856],[871,885],[958,971],[1022,1035]]
        if has_word(array[y][780+shift[0]]) and has_word(array[y][1025+shift[0]]):
            fulu='riichi'
        elif has_word(array[y][890+shift[0]]) and has_word(array[y][955+shift[0]]):
            fulu='chii'
        elif has_word(array[y][865+shift[0]]) and has_word(array[y][815+shift[0]]):
            fulu='kan'
        elif has_word(array[y][855+shift[0]]) and has_word(array[y][815+shift[0]]):
            fulu='pon'
    elif now_player==2: #y axis is 495
        y=495
        # pon_position=[[431,479]]
        # kan_position=[[432,446],[473,491]]
        # chii_position=[[443,481],[507,520],[571,585],[600,613]]
        # riichi_position=[[389,441],[464,477],[493,406],[580,593],[643,656]]
        if has_word(array[y][400+shift[0]]) and has_word(array[y][650+shift[0]]):
            fulu='riichi'
        elif has_word(array[y][515+shift[0]]) and has_word(array[y][575+shift[0]]):
            fulu='chii'
        elif has_word(array[y][485+shift[0]]) and has_word(array[y][440+shift[0]]):
            fulu='kan'
        elif has_word(array[y][435+shift[0]]) and has_word(array[y][475+shift[0]]):
            fulu='pon'
    elif now_player==3: #y axis is 781
        y=781
        # pon_position=[[810,858]]
        # kan_position=[[811,825],[853,871]]
        # chii_position=[[822,863],[886,900],[921,934],[950,963],[980,992]]
        # riichi_position=[[767,817],[842,856],[871,885],[958,971],[1022,1035]]
        if has_word(array[y][780+shift[0]]) and has_word(array[y][1030+shift[0]]):
            fulu='riichi'
        elif has_word(array[y][890+shift[0]]) and has_word(array[y][960+shift[0]]):
            fulu='chii'
        elif has_word(array[y][865+shift[0]]) and has_word(array[y][820+shift[0]]):
            fulu='kan'
        elif has_word(array[y][815+shift[0]]) and has_word(array[y][855+shift[0]]):
            fulu='pon'
    if fulu!=None and fulu!='riichi' and (not is_jkan(array,now_player,fulu)):
        river_cards[ex_player]-=1
        if river_cards[ex_player]%6==5:
            if ex_player==1 or ex_player==3:
                river_position[ex_player][1]-=card_long[ex_player]
                if ex_player==1:
                    river_position[ex_player][0]=794.5+shift[0]
                else:
                    river_position[ex_player][0]=1001+shift[0]
            else:
                river_position[ex_player][0]-=card_long[ex_player]
                if ex_player==0:
                    river_position[ex_player][1]=440.5
                elif ex_player==2:
                    river_position[ex_player][1]=627.5
        else:                
            if ex_player==1 or ex_player==3:
                river_position[ex_player][0]-=card_short[ex_player]
            else:
                river_position[ex_player][1]-=card_short[ex_player]
        river_cards[now_player]+=1
        if now_player==1 or now_player==3:
            if river_cards[now_player]%6==0:
                river_position[now_player][1]+=card_long[now_player]
                if now_player==1:
                    river_position[now_player][0]=1006+shift[0]
                else:
                    river_position[now_player][0]=796+shift[0]
            else:                
                river_position[now_player][0]+=card_short[now_player]
            if fulu=='kan':
                mo_position[now_player][0]+=3*mo_distance[now_player]
            else:
                mo_position[now_player][0]+=2*mo_distance[now_player]
        else:
            if river_cards[now_player]%6==0:
                river_position[now_player][0]+=card_long[now_player]
                if now_player==0:
                    river_position[now_player][1]=618
                elif now_player==2:
                    river_position[now_player][1]=450
            else:
                river_position[now_player][1]+=card_short[now_player]
            if fulu=='kan':
                mo_position[now_player][1]+=3*mo_distance[now_player]
            else:
                mo_position[now_player][1]+=2*mo_distance[now_player]
    elif is_jkan(array,now_player,fulu): fulu=None
    return fulu
def reset_detect():
    global mo_position,river_position,river_cards,HC_LEN,handcard_position
    mo_position=[[1415+shift[0],250],[730+shift[0],93],[390+shift[0],690],[1340+shift[0],905]]
    river_position=[[1053+shift[0],618],[1006+shift[0],403],[747+shift[0],450],[796+shift[0],675]]
    river_cards=[0,0,0,0]
    handcard_position=[380+shift[0]+my_card_short*x for x in range(14)]
    handcard_position[13]+=4
    HC_LEN=14