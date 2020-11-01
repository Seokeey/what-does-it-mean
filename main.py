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
from selenium.common.exceptions import NoSuchElementException


CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
DEFAULT_DELAY = 15

        

def speak(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
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


    def wait_and_click(self, xpath, delay=DEFAULT_DELAY):
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
   
    def run(self, seeking_word):
        input_box = self.driver.find_element(
                By.XPATH,
                '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
            )
        input_box.send_keys(f'{seeking_word} meaning')
        input_box.send_keys(Keys.ENTER)


        tolerance = 10

        while tolerance:
            try:
                texts = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="tsuid11"]/span/div/div/div[1]/div/div[2]/div[1]/div/span'
                ).text

                words = ""
                for text in texts:
                    if text.isalpha():
                        words += text
                meaning = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="tsuid11"]/span/div/div/div[1]/div/div[4]/div/div/ol/li/div/div/div[1]/div/div/div[1]/span',
                ).text

                said = f"{words} meaning is {meaning}"
                speak(said)
                return
            except Exception as e:
                tolerance -= 1
                print(f"에러발생 : {e}")
                print(f"현재 남은 재시도 횟수: {tolerance}")
                time.sleep(2)

        speak("검색결과가 존재하지않거나 단어가 아닙니다 다시 입력해주세요", lang='ko')





if __name__ == "__main__":
    auto = AutoBrowser(CHROMEDRIVER_PATH)
    auto.run()
