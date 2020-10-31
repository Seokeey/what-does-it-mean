import os
import time
import playsound
import speech_recognition as sr

from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")

        

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.MicroPhone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print(f"Exception : {str(e)}")

    return said

class AutoBrowser:

    def __init__(self, path):
        self.driver = webdriver.Chrome(path)
        self.driver.get('https://www.google.com')


    def wait_and_click(self, xpath, delay=15):
        try:
            w = WebDriverWait(self.driver, delay)
            elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()
        except Exception as e:
            print(f'클릭 지연시간 초과 - {xpath}')
            print('브라우저를 새로고침중입니다')
            self.driver.refresh()
            time.sleep(2)
            return self.wait_and_click(xpath)

    def run(self):
        input_box = self.driver.find_element(
                By.XPATH,
                '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
            )
        input_box.send_keys('unleash meaning')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        words = self.driver.find_element(
            By.XPATH,
            '//*[@id="tsuid11"]/span/div/div/div[1]/div/div[2]/div[1]/div/span'
        ).text

        result = ""
        for word in words:
            if word.isalpha():
                result += word

        speak(result)







    

        

#        pronounce = self.driver.find_element(
#                By.XPATH,
#                '//*[@id="tsuid22"]/span/div/div/div[1]/div/div[1]/div/div[5]'
#            )
#
#        pronounce.send_keys('click')





auto = AutoBrowser(CHROMEDRIVER_PATH)
auto.run()
