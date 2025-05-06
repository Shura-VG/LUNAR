import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
import playsound
import pyttsx3
import pygame
import datetime
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

language = 'vi'
path = ChromeDriverManager().install()
wikipedia.set_lang('vi')

# Thay đổi ngôn ngữ thành 'vi' cho tiếng Việt
def speak(text):
    print("Lunar: {}".format(text))
    tts = gTTS(text=text, lang='vi', slow=False)
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    tts.save(filename)

    # Dùng pygame để phát âm thanh
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Chờ đến khi phát xong
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Dừng nhạc, xóa file âm thanh
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
    os.remove(filename)

def speak_and_display(text):
    chat_display.insert(tk.END, f"Lunar: {text}\n")
    chat_display.see(tk.END)
    chat_display.update()  # Giúp hiển thị đầy đủ ngay
    speak(text)

def get_audio():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        chat_display.insert(tk.END, "Tôi: Đang lắng nghe...\n")  
        chat_display.see(tk.END)
        chat_display.update()
        audio = r.record(source, duration=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            chat_display.insert(tk.END, f"Bạn: {text}\n")
            chat_display.see(tk.END)
            chat_display.update()
            return text
        except:
            print("...")
            return 0

def stop():
    speak_and_display("Hẹn gặp lại bạn nhé!")

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak_and_display("Lunar không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(8)
    stop()
    return 0

def open_website(text):
    regex = re.search ('mở (.+)', text)
    if regex:
        domain = regex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak_and_display("Trang web của bạn đã được mở lên!")
        return True
    else:
        return False

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import re
import time

def google_search(text):
    try:
        search_query = text.split("tìm kiếm", 1)[1].strip()
        speak_and_display("Ok, Lunar đang tìm kiếm...")
        # Khởi tạo Chrome (kèm User Agent giả lập trình duyệt thật)
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Mở Google
        driver.get("https://www.google.com")
        
        # Nhập từ khóa và bấm tìm kiếm
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        # Chờ CAPTCHA xuất hiện (nếu có) và thông báo cho người dùng nhập
        speak_and_display("Vui lòng nhập CAPTCHA trong 20 giây nếu có yêu cầu...")
        time.sleep(10)  # Chờ đủ thời gian nhập CAPTCHA
        
    except Exception as e:
        speak_and_display("Lỗi khi tìm kiếm. Vui lòng thử lại sau.")
        print(f"[Lỗi] {e}")
    finally:
        time.sleep(10)  # Giữ trình duyệt mở thêm 10s trước khi đóng
        driver.quit()

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak_and_display("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak_and_display("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak_and_display("Lunar không hiểu")

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak_and_display("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak_and_display("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak_and_display("Lunar không hiểu")

def play_youtube():
    speak_and_display("Xin mời bạn chọn bài hát")
    time.sleep(2)
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results = 10).to_dict()
        if result:
            break;
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak_and_display("Bài hát của bạn đã được mở, hãy thưởng thức nhó!")
    time.sleep(2)

def weather():
    speak_and_display("Bạn muốn xem thời tiết ở đâu ạ!")
    time.sleep(2)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time  = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day, month = now.month, year= now.year, hourrise = sun_rise.hour, minrise = sun_rise.minute,
                                                                           hourset = sun_set.hour, minset = sun_set.minute,
                                                                           temp = current_temp, pressure = current_pressure, humidity = current_humidity)
        speak_and_display(content)
        time.sleep(3)
    else:
        speak_and_display("Không tìm thấy thành phố!")

def open_application(text):
    if "google" in text:
        speak_and_display("Mở google")
        os.startfile(r'C:\Program Files\CocCoc\Browser\Application\browser.exe')
    elif "word" in text:
        speak_and_display("Mở Microsoft Word")
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
    elif "excel" in text:
        speak_and_display("Mở Microsoft Excel")
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
    elif "powerpoint" in text:
        speak_and_display("Mở Microsoft PowerPoint")
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE')
    else:
        speak_and_display("Lunar không tìm thấy phần mềm bạn muốn")

def chang_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']

    urllib2.urlretrieve(photo, r"C:\Users\thanh\Downloads\image.png")
    image = os.path.join(r"C:\Users\thanh\Downloads\image.png")
    ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
    speak_and_display("Hình nền máy tính vừa được thay đổi")
    time.sleep(2)

def tell_me():
    try:
        speak_and_display("Bạn muốn nghe về gì ạ!")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak_and_display(contents[0])
        time.sleep(10)
        for content in contents[1:]:
            speak_and_display("Bạn muốn nghe tiếp hay không ?")
            ans = get_text()
            if "không" in ans:
                break
            speak_and_display(content)
            time.sleep(2)

        speak_and_display("Cảm ơn bạn đã lắng nghe!")
    except:
        speak_and_display("Lunar không định nghĩa được ngôn ngữ của bạn!")
    
import json
import datetime
import time
import threading
from pathlib import Path

# Tệp lưu nhắc nhở
REMINDER_FILE = "reminders.json"

def load_reminders():
    if Path(REMINDER_FILE).exists():
        with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    with open(REMINDER_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders, f, indent=2, ensure_ascii=False)

def add_reminder(task, remind_time):
    reminders = load_reminders()
    reminders.append({"task": task, "time": remind_time})
    save_reminders(reminders)
    print(f"Đã lưu nhắc nhở: {task} lúc {remind_time}")

def reminder_loop():
    while True:
        now = datetime.datetime.now()
        reminders = load_reminders()
        for reminder in reminders:
            try:
                reminder_time = datetime.datetime.strptime(reminder['time'], "%H:%M")
                # Gộp ngày hiện tại với giờ phút nhắc nhở
                reminder_datetime = now.replace(hour=reminder_time.hour, minute=reminder_time.minute, second=0, microsecond=0)
                
                # Tính khoảng cách thời gian (tính bằng phút)
                time_diff = (reminder_datetime - now).total_seconds() / 60

                # Nếu nhắc nhở nằm trong khoảng từ 0 đến 60 phút tới
                if 0 <= time_diff <= 30:
                    speak_and_display(f"Nhắc nhở: {reminder['task']} vào lúc {reminder['time']}")
                    # Sau khi nhắc thì xóa luôn khỏi danh sách để tránh nhắc lại
                    reminders.remove(reminder)
                    save_reminders(reminders)
            except:
                continue

        time.sleep(60)  # Kiểm tra mỗi phút)

def start_reminder_system():
    thread = threading.Thread(target=reminder_loop, daemon=True)
    thread.start()

def create_reminder_from_speech():
    speak_and_display("Bạn muốn nhắc gì ạ?")
    task = get_text()
    if not task:
        speak_and_display("Mình chưa nghe rõ nội dung nhắc nhở.")
        return

    speak_and_display("Vào lúc mấy giờ?")
    time_str = get_text()  # ví dụ: "8 giờ tối"
    
    # Đơn giản hóa việc nhận giờ
    time_formatted = convert_to_24h(time_str)
    if time_formatted:
        add_reminder(task, time_formatted)
        speak_and_display(f"Đã đặt nhắc nhở {task} vào lúc {time_formatted}")
    else:
        speak_and_display("Xin lỗi, mình không hiểu thời gian bạn nói.")

def convert_to_24h(time_str):
    # TODO: dùng NLP để phân tích linh hoạt hơn
    # Ở đây là ví dụ đơn giản
    if "tối" in time_str:
        hour = int(time_str.split(" ")[0]) + 12
    else:
        hour = int(time_str.split(" ")[0])
    return f"{hour:02d}:00"

def read_all_reminders():
    reminders = load_reminders()
    if not reminders:
        speak_and_display("Hiện tại bạn không có nhắc nhở nào.")
        return

    speak_and_display("Đây là các nhắc nhở bạn đã đặt:")
    for reminder in reminders:
        speak_and_display(f"{reminder['task']} vào lúc {reminder['time']}")

def help():
    speak_and_display("""Lunar có thể làm những việc sau:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, app
    4. Tìm kiếm trên Google
    5. Dự báo thời tiết
    6. Mở video nhạc
    7. Thay đổi hình nền máy tính
    8. Đọc báo hôm nay
    9. Kể bạn biết về thế giới
    10. Nhắc nhở """)
    time.sleep(5)

def time_now():
    return datetime.datetime.now()

def call_lunar():
    # speak("Xin chào, bạn tên là gì nhỉ?")
    # name = get_text()
    # if name:
        # speak("Chào bạn {}".format(name))
        now = time_now()
        if now.hour > 0 and now.hour < 12:
            speak_and_display("""Chào buổi sáng""")
        elif now.hour >= 12 and now.hour < 18:
            speak_and_display("""Buổi chiều vui vẻ""")
        elif now.hour >= 18 and now.hour < 24:
            speak_and_display("""Buổi tối nhẹ nhàng""")
        time.sleep(1)
        start_reminder_system()
        time.sleep(2)
        speak_and_display("Bạn cần Lunar giúp gì ạ!")
        time.sleep(2)
        while True:
            text = get_text()
            if not text:
                break
            # elif "trò chuyện" in text or "nói chuyện" in text:
            #     talk(name)
            elif "dừng" in text or "thôi" in text:
                stop()
                break
            elif "mở" in text:
                if "." in text:
                    open_website(text)
                else:
                    open_application(text)  
            elif "tìm kiếm" in text:
                    google_search(text)
            elif "ngày" in text  or "giờ" in text:
                get_time(text)
            elif "chơi nhạc" in text:
                play_youtube()
            elif "thời tiết" in text:
                weather()
            elif "hình nền" in text:
                chang_wallpaper()
            elif "định nghĩa" in text:
                tell_me()
            elif "có thể làm được gì" in text:
                help()
            elif "nhắc nhở" in text:
                create_reminder_from_speech()
            elif "lịch trình" in text:
                read_all_reminders()

def run_assistant():
    try:
        call_lunar()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

def start_assistant_thread():
    thread = threading.Thread(target=run_assistant)
    thread.start()

# Giao diện GUI
root = tk.Tk()
root.title("Lunar - Trợ lý ảo tiếng Việt")
root.geometry("600x500")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

start_button = tk.Button(
    root, text="Bắt đầu", command=start_assistant_thread,
    width=20, height=2, bg="pink", fg="black", font=("Arial", 14)
)
start_button.pack(pady=10)

root.mainloop()
