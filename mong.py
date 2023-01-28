# import time,os
# from urllib.request import urlopen
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 定義 headless
# chrome_path = "C:/Users/User/chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
# driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)



# url="https://running.biji.co/index.php?q=album&act=photo_list&album_id=35892&cid=7214&start=1545528000&end=1545528600&type=place&subtitle=%E8%81%96%E8%AA%95%E6%AD%A1%E6%A8%82%E4%B8%BB%E9%A1%8C%E5%9C%98%E8%B7%91-%E8%8F%AF%E7%82%BA%E6%89%8B%E7%92%B0%E9%AB%94%E9%A9%97"
# driver.get(url)
# driver.implicitly_wait(1)

# for i in range(1,101):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(0.3)

# soup=BeautifulSoup(driver.page_source,'html.parser')
# title = soup.find('h1','album-title').text.strip()
# all_imgs = soup.find_all('img', {"class": "photo_img photo-img"})

# images_dir ='d:\\'+ title + "\\"
# if not os.path.exists(images_dir):
#     os.mkdir(images_dir)

# # 處理所有 <img> 標籤
# n = 0

# for img in all_imgs:
#     # 讀取 src 屬性內容
#     src = img['src']
#     # 讀取 .jpg 檔
#     if src != None and ('.jpg' in src):
#         # 設定圖檔完整路徑
#         full_path = src
#         filename = full_path.split('/')[-1]  # 取得圖檔名
#         print(full_path)
#         # 儲存圖片
#         try:
#             image = urlopen(full_path)
#             with open(os.path.join(images_dir, filename), 'wb') as f:
#                 f.write(image.read())
#             n += 1
#             if n >= 1000:  # 最多下載 1000 張
#                 break
#         except:
#             print("{} 無法讀取!".format(filename))

# print("共下載", n, "張圖片")
# driver.quit()  # 關閉瀏覽器並退出驅動程式
import socket
HOST='192.168.10.120'
PORT=5000
server_addr=(HOST,PORT)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    outdata=input('請輸入')
    print('sendto '+str(server_addr)+":"+outdata)
    s.sendto(outdata.encode(),server_addr)