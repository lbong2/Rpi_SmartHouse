from bs4 import BeautifulSoup
import requests
import re
from tkinter import *


from PIL import Image, ImageTk
import datetime
#import RPi.GPIO as GPIO
import pickle
import time
import os



"""
    SW_Project Team3
    author: LEE KYUNGBONG
"""
"""
def ctrl_win():
    global p
    if win_val.get() == 1:
        p.ChangeDutyCycle(7.5)
    else:
        p.ChangeDutyCycle(2.5)

def exit():
    global on_flag
    on_flag -= 1
    
    GPIO.cleanup()
    win.quit()

"""
spl_dic = {'매우높음': '01', '높음': '02', '보통': '03', '낮음': '04'}
pois_dic = {'관심': '01', '주의': '02', '경고': '03', '위험': '04'}
uv_dic = {'낮음':'01', '보통': '02', '높음': '03', '매우높음': '04', '위험': '05'}
we_dic = {'맑음': '01', '구름조금': '02', '구름많음': '03', '흐림': '04', '비': '05', '눈': '06'}
car_dic = {'97허8065': '아빠'}

mot_sig = 17  

on_flag=1
win_prev = 0
pin = 18



"""
GPIO.setmode(GPIO.BCM)
 
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(mot_sig, GPIO.OUT)





p=GPIO.PWM(pin, 50)
p.start(2.5)
"""
while(on_flag != 0):
    
    html = requests.get('https://weather.naver.com/today')
    soup = BeautifulSoup(html.text, 'html.parser')

    # 위치 데이터
    data1 = soup.find('div', {'class':'location_area'})
    find_address = data1.find('strong', {'class':'location_name'}).text
    print('현재 위치: '+ find_address)

    # 날씨, 온, 습도 데이터
    data2 = soup.find('div', {'class':'weather_area'})
    temp = data2.find('strong', {'class':'current'}).text
    find_temp = re.sub(r'[^0-9]', '', temp)
    find_humid= data2.find('dd', {'class':'desc'}).text
    find_weather = data2.find('span', {'class':'weather before_slash'}).text
    
    # 미세먼지, 초미세먼지, 자외선 데이터
    data3 = soup.find('ul', {'class':'chart_list'})
    data4 = data3.findAll('li', {'class':'item'})
    find_uv = data4[1].find('strong', {'class':'level_dsc'}).text
    find_spl = data4[2].find('strong', {'class':'level_dsc'}).text
    find_poison = data4[3].find('strong', {'class':'level_dsc'}).text
   
    # 날짜 데이터
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d')


    # Tkinter GUI 구현부
    win = Tk()
    win.title("window")
    win.geometry('1600x600+0+200')
    win.resizable(False, False)

    # place label
    place_image = Image.open("./image/position.jpg")
    place_image = ImageTk.PhotoImage(image=place_image)
    place_label = Label(win, image=place_image, text=find_address, background='white', compound='left', width=500, height=100)
    
    # time_label
    time_img = Image.open("./image/calender.png")
    time_img = ImageTk.PhotoImage(image=time_img)
    time_label = Label(win, text=now, image=time_img, compound='left', background='white', width=300, height=100)

    # weather_label
    weather_img = Image.open("image/we" + we_dic[find_weather] + ".png")
    weather_img = ImageTk.PhotoImage(image=weather_img)
    weather_label = Label(win, image=weather_img, text=find_weather + "\n온도: " + find_temp + "℃\n습도: " + find_humid,
    compound='left', background='white',width=500, height=300 )
    # Thema weather label
    air_img = Image.open("./image/air_" + spl_dic[find_spl] + ".jpg")
    air_img = ImageTk.PhotoImage(image=air_img)
    pois_img = Image.open("./image/pois_" + pois_dic[find_poison] + ".jpg")
    pois_img = ImageTk.PhotoImage(image=pois_img)
    uv_img = Image.open("./image/uv_" + uv_dic[find_uv] + ".jpg")
    uv_img = ImageTk.PhotoImage(image=uv_img)

    air_label = Label(win, image=air_img, text="대기확산\n" + find_spl, compound='left', background='white', width=300, height=80)
    pois_label = Label(win, image=pois_img, text="식중독\n" + find_poison, compound='left', background='white', width=300, height=80)
    uv_label = Label(win, image=uv_img, text="자외선\n" + find_uv, compound='left', background='white', width=300, height=80)

    # window_button
    win_val = IntVar()
    win_val.set(win_prev)
    window_but = Checkbutton(win, text="창문 열기", variable=win_val, command=ctrl_win, background='white', width=27, height=3)

    # 방문 차량 알림 구현부 
    try:
        with open('number.p', 'rb') as file:
            car_num = pickle.load(file)
            if car_num in car_dic.keys():
                car_num2 = "\n방문한 차량은 " + car_dic[car_num] + "의 차량입니다."
                car_img = Image.open("carImage.jpg")
                car_img = car_img.resize((600, 300))
                car_img2 = ImageTk.PhotoImage(image=car_img)
                img_label = Label(win, text="방문 차량 알림", image=car_img2, background='white',compound='bottom', width=800, height=400)
                car_img.close()
            else:
                car_num2 = "\n방문한 차량은 "+ car_num +" 차량입니다.\n방문자를 확인 후 문을 열어주십시오."
                car_img = Image.open("carImage.jpg")
                car_img = car_img.resize((600, 300))
                car_img2 = ImageTk.PhotoImage(image=car_img)
                img_label = Label(win, text="방문 차량 알림", image=car_img2, background='white',compound='bottom', width=800, height=400)
                car_img.close()
        os.system("rm carImage.jpg")
        os.system("rm number.p")
    except FileNotFoundError:
        car_num2 = "방문한 차량이 없습니다."
        car_img = Image.open("ex_img.jpg")
        car_img = car_img.resize((600, 300))
        car_img2 = ImageTk.PhotoImage(image=car_img)
        img_label = Label(win, text="방문 차량 알림", image=car_img2, background='white',compound='bottom', width=800, height=400)
        car_img.close()

    num_label = Label(win, text=car_num2, width=50, height=3, background='white')

    # 새로고침, 끝내기 버튼
    # Exit, F5 button
    refresh = Button(text = "새로 고침", command = win.destroy, width=25, height=3)
    exit_but = Button(text = "끝내기", command = exit, width=25, height=3)

    # recommand activity
    if int(we_dic[find_weather][1]) > 2:
        rec = "● 야외 활동시 우산 챙겨주세요."
    else:
        rec = "● 비교적 맑은 날씨입니다."
        if int(spl_dic[find_spl][1]) < 2:
            rec += "\n● 야외 활동, 야외건조 추천드립니다!"
        else: 
            rec += "\n● 외출 시 마스크 꼭 챙겨주세요!"
    

    if int(spl_dic[find_spl][1]) > 2:
        rec += "\n● 대기 확산 지수가 좋지않아요. 창문을 닫아주세요."
    else: 
        if int(we_dic[find_weather][1]) > 2:
            rec += "\n● 비가 오지만 환기하기 좋은 날씨에요."
        else:
            rec += "\n● 환기시키기 정말 좋은 날입니다! 창문을 열어주세요."
    
    if int(pois_dic[find_poison][1]) > 2:
        rec += "\n● 음식물 보관에 주의하세요. 상하기 쉬운 음식 주의하세요."
    
    if int(uv_dic[find_uv][1]) > 2:
        rec += "\n● 외출시 자외선에 대비하세요."
    else:
        rec += "\n● 자외선 수치가 좋아요."


    
    rec_label = Label(win, text=rec, width=50, height=5, background='white', justify='left')
    place_label.configure(font=("Courier", 20, "italic"))
    img_label.configure(font=("Courier", 20, "italic"))
    weather_label.configure(font=("Courier", 20, "italic"))
    time_label.configure(font=("Courier", 20, "italic"))
    air_label.configure(font=("Courier", 20, "italic"))
    pois_label.configure(font=("Courier", 20, "italic"))
    uv_label.configure(font=("Courier", 20, "italic"))
    window_but.configure(font=("Courier", 12, "italic"))
    
    num_label.configure(font=("Courier", 20, "italic"))
    exit_but.configure(font=("Courier", 20, "italic"))
    refresh.configure(font=("Courier", 20, "italic"))
    rec_label.configure(font=("Courier", 20, "italic"))

    place_label.grid(row=0, column=0)
    time_label.grid(row=0,column=1)
    img_label.place(x=800, y=0)
    weather_label.grid(row=1, column=0)
    air_label.place(x=500, y=100)
    pois_label.place(x=500, y=180)
    uv_label.place(x=500, y=260)
    window_but.place(x=500, y=340)
   
    num_label.place(x=800, y=400)
    exit_but.place(x=1200, y=500)
    refresh.place(x=800, y=500)
    rec_label.place(x=0, y=400)
    
    win.mainloop()
    
    win_prev = win_val.get()
   
    
    
    
    


