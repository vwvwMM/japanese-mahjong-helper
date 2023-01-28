import tkinter as tk
from typing import Text
from screenshot import *
from PIL import ImageGrab
import numpy as np
from mah import calc_shanten_14
from utils import calc_xiangting, convert_num_to_card

window_width=400
window_height=800
river_short=100
center_side=120
card_short=center_side/6
card_long=27
w_add_c=(window_width+center_side)/2
w_sub_c=(window_width-center_side)/2
text_height=50
text_position=[60,window_width+10]
KEY_RIGHT=39
KEY_UP=38
KEY_LEFT=37

window = tk.Tk()
window.title('helper')
window.geometry(str(window_width)+'x'+str(window_height))
window.wm_attributes("-topmost", 1)

running = False  # Global flag
def screenshot():
    im = ImageGrab.grab()
    im.save(r'./screenshots/screenshot.png')

def scanning():
    if running:  # Only do this if the Stop button has not been clicked
        get_info()

    # After 1 second, call scanning again (create a recursive loop)
    window.after(100, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True

def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False
pixelVirtual = tk.PhotoImage(width=card_long, height=card_long)
start_btn = tk.Button(window, image=pixelVirtual, text="Start Scan",compound="c", command=start)
stop_btn = tk.Button(window, image=pixelVirtual, text="Stop",compound="c", command=stop)
start_btn.place(x=0,y=0)
stop_btn.place(x=window_width-card_long,y=0)
center=tk.Frame(window,  width=center_side , height=center_side , bg='blue')
river1=tk.Frame(window,  width=river_short , height=center_side,bg='yellow')
river2=tk.Frame(window,  width=center_side , height=river_short,bg='yellow')
river3=tk.Frame(window,  width=river_short , height=center_side,bg='yellow')
river4=tk.Frame(window,  width=center_side , height=river_short,bg='yellow')
advice_region=tk.Frame(window,  width=window_width , height=window_width,bg='yellow')
restart_btn = tk.Button(window, text='RESTART',image=pixelVirtual, compound="c",bg='red', fg='white', font=('Arial', 12))
screenshot_btn = tk.Button(window, text='shot',image=pixelVirtual, compound="c",bg='red', fg='white', font=('Arial', 12))
restart_btn['activebackground'] = 'red'        
restart_btn['activeforeground'] = 'yellow'     
text_box = tk.Entry (window)
center.place(x=w_sub_c,y=w_sub_c)
river1.place(x=w_add_c,y=w_sub_c)
river2.place(x=w_sub_c,y=w_sub_c-river_short)
river3.place(x=w_sub_c-river_short,y=w_sub_c)
river4.place(x=w_sub_c,y=w_add_c)
advice_region.place(x=text_position[0],y=text_position[1])
rivers=[river1,river2,river3,river4]
text_box.place(width=w_sub_c,height=card_long,x=(window_width-w_sub_c)/2,y=window_width-2*card_long)
screenshot_btn.place(x=window_width-card_long,y=window_height-card_long)
restart_btn.place(x=0,y=window_height-card_long)

now_player=0
ex_player=5
now_position=[[0,center_side-card_short],[center_side-card_short,river_short-card_long],[river_short-card_long,0],[0,0]]

def create_card(input,player):
    global now_position
    card = tk.Frame(rivers[player],highlightbackground="black",highlightthickness=1)
    if input[0]=='q':
        card.config(bg='gray')
    elif input[0]=='w':
        card.config(bg='white')
    elif input[0]=='e':
        card.config(bg='red')
    if player==0:
        card.config(width=card_long,height=card_short)
        card.place(x=now_position[player][0],y=now_position[player][1])
        if now_position[0][1]==0:
            now_position[0]=[now_position[0][0]+card_long,center_side-card_short]
        else:
            now_position[0][1]-=card_short
    elif player==1:
        card.config(width=card_short,height=card_long)
        card.place(x=now_position[player][0],y=now_position[player][1])
        if now_position[1][0]==0:
            now_position[1]=[center_side-card_short,now_position[1][1]-card_long]
        else:
            now_position[1][0]-=card_short
    elif player==2:
        card.config(width=card_long,height=card_short)
        card.place(x=now_position[player][0],y=now_position[player][1])
        if now_position[2][1]==center_side-card_short:
            now_position[2]=[now_position[2][0]-card_long,0]
        else:
            now_position[2][1]+=card_short
    elif player==3:
        card.config(width=card_short,height=card_long)
        card.place(x=now_position[player][0],y=now_position[player][1])
        if now_position[3][0]==center_side-card_short:
            now_position[3]=[0,now_position[3][1]+card_long]
        else:
            now_position[3][0]+=card_short
def delete_card(player):
    global now_position
    rivers[player].winfo_children()[-1].destroy()
    if player==0:
        if now_position[0][1]==center_side-card_short:
            now_position[0]=[now_position[0][0]-card_long,0]
        else:
            now_position[0][1]+=card_short
    elif player==1:
        if now_position[1][0]==center_side-card_short:
            now_position[1]=[0,now_position[1][1]+card_long]
        else:
            now_position[1][0]+=card_short
    elif player==2:
        if now_position[2][1]==0:
            now_position[2]=[now_position[2][0]+card_long,center_side-card_short]
        else:
            now_position[2][1]-=card_short
    elif player==3:
        if now_position[3][0]==0:
            now_position[3]=[center_side-card_short,now_position[3][1]-card_long]
        else:
            now_position[3][0]-=card_short
def get_xian_ting():
    im = ImageGrab.grab()
    array=np.array(im)
    txt=recog_card(array)
    if txt != '':
        advice_list=calc_shanten_14(txt)
        for idx,x in enumerate(advice_list):
            advice="打"+str(convert_num_to_card(x[0]))+str(x[2])+"枚\n"+" 摸"+str([convert_num_to_card(x) for x in x[1]])
            t=tk.Label(advice_region ,text=advice,relief=tk.SUNKEN,justify=tk.LEFT,bg='red', fg='white', font=('Arial', 12))
            t.place(x=0,y=text_height*(idx+1),anchor='w')
def open_new_game():
    global now_position,river,now_player,ex_player
    stop()
    for river in rivers:
        for widgets in river.winfo_children():
            widgets.destroy()
    for widgets in advice_region.winfo_children():
        widgets.destroy()
    rivers[now_player].config(bg='yellow')
    now_player=0
    ex_player=5
    now_position=[[0,center_side-card_short],[center_side-card_short,river_short-card_long],[river_short-card_long,0],[0,0]]
    reset_detect()
def get_info():
    global now_player,ex_player,rivers
    im = ImageGrab.grab()
    array=np.array(im)
    turn=whose_turn(array)
    if turn!=None:
        rivers[now_player].config(bg='yellow')
        now_player=turn
        rivers[now_player].config(bg='green')
    if ex_player!=now_player:
        if ex_player==3:
            for widgets in advice_region.winfo_children():
                widgets.destroy()
        fulu=check_fulu(array,now_player,ex_player)
        if fulu==None or fulu=='riichi':
            if now_player==3 and len(advice_region.winfo_children())==0:
                get_xian_ting()
            is_mo=check_mo(array,now_player,fulu)
            if is_mo==True:
                create_card('q',now_player)
                ex_player=now_player
            elif is_mo==False:
                create_card('w',now_player)
                ex_player=now_player
        else:
            create_card('e',now_player)
            delete_card(ex_player)
            ex_player=now_player
            
window.after(120, scanning)  # After 1 second, call scanning
restart_btn.config(command=open_new_game)
screenshot_btn.config(command=screenshot)
window.mainloop()