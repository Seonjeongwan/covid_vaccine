from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions

import time
import pyperclip #자동 입력 방지를 위해 사용
import keyboard #키보드 입력 확인을 위해

#cmd 실행 명령어 - 크롬으로 위치 이동 후 실행 명령어
# cd C:\Program Files (x86)\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")

# headless 옵션 설정
chrome_options.add_argument('headless')
chrome_options.add_argument("no-sandbox")

chrome_options.add_argument("disable-gpu")   # 가속 사용 x
chrome_options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재

chrome_driver = "C:/Users/admin/Desktop/chromedriver/chromedriver"
driver = webdriver.Chrome(chrome_driver,options=chrome_options)

URL = "https://www.naver.com/"

driver.get(url = URL)

#2초 기다리기
driver.implicitly_wait(2)
try :
    driver.find_element_by_xpath('//*[@id="account"]/a').click()

    driver.implicitly_wait(2)

    while True:
        tag_id = driver.find_element_by_name('id')
        tag_pw = driver.find_element_by_name('pw')

        tag_id.clear() #있는거 제거    
    
        # id 입력
        tag_id.click()
        print("네이버 아니디를 입력 하세요 : ")
        pyperclip.copy(input())
        tag_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        print("비밀번호를 입력 하세요 : ")
        pyperclip.copy(input())
        tag_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="log.login"]').click()

        driver.implicitly_wait(2)

        if (driver.current_url == URL):
            break;

except exceptions.NoSuchElementException :
    print("이미 로그인 되어있습니다. 백신 맵 이동")

#print("사이트에서 아이디 비밀번호를 입력해주십시오")

tag_search = driver.find_element_by_name('query')
tag_search.send_keys("잔여백신예약" + Keys.ENTER)
time.sleep(1)

driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div/div/div[3]/ul/li[1]/a/span').click()

print("원하는 검색 장소로 지도를 이동시켜주신 후 \"현 지도에서 검색\" 클릭 진행")
print("주기적 새로고침을 위해 F2 누르면 됨")

refresh_yn = keyboard.read_key()
print(refresh_yn)
#print(fresh_yn) #입력된 키가 f2일 경우만 계속해서 돌리기

map_url = "" #맵 url 이동용

refresh_btn = '' #새로고침 버튼 만들기
refresh_cnt = 1

#병원리스트를 불러오는 함수
def find_all_vaccine():
    vaccine_list = driver.find_elements_by_class_name("_3sd6u")
    # print("리스트 출력")
    # print(vaccine_list)
    for x in vaccine_list:
        # print(str(x.text))
        # print (x.text != "대기중"  and x.text != "")
        # print(x.text == "0\n개")
        if (x.text != "대기중" and x.text != "" and x.text != "마감" and x.text != "0" and x.text != "0\n개"):
            print(x.text)
            x.click()

            return x.text
    
    return False

def get_map_url():
    cur_map_url = driver.current_url
    return cur_map_url

def reserve_start():

    try:
        #전체동의 체크
        all_check_btn = driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div[2]/div/div/label')
        all_check_btn.click()

    except exceptions.NoSuchElementException :
        print("이미 전체동의 완료됨. 바로 예약 버튼 클릭 진행")
    
    reserve_url = driver.current_url

    try:
        #예약 버튼 클릭
        reservation_confirm_btn = driver.find_element_by_xpath('//*[@id="reservation_confirm"]')
        reservation_confirm_btn.click()

        #예약 버튼을 클릭했으나 반응이 없는것으로 백신 예약 다참 다시 예약 시작
        time.sleep(1)
        if (reserve_url == driver.current_url):
            driver.get(url = map_url)
            #이전페이지 이동을 위해 1초 대기
            time.sleep(1)
            return "full_reserve"

    #예약버튼마저 없는 경우는 아예 나가리 임으로 내가 임의로 페이지 이동을 한거
    except exceptions.NoSuchElementException :
        print("예약 버튼 없음으로 인한 페이지 이동")
        return "wrong_page"
    
    #예약버튼 있는경우는
    #페이지 이동 1초 기다림
    time.sleep(1)
    #예약 버튼이 있고 클릭이 되었다면 페이지 이동이 됨으로 URL 비교 안되면 이전페이지로 이동
    if (reserve_url == driver.current_url):
        driver.get(url = map_url)
        print(map_url)
        #이전페이지 이동을 위해 1초 대기
        time.sleep(1)
        return "full_reserve"
    else: #url이 다른경우
        try :
            last_message = driver.find_element_by_class_name("h_title")
            print(last_message.text())
            time.sleep(3) #3초 시간을 주고
            ########if로 처리 빞요
            print("백신 잔여 수량 없음")
            driver.get(url = map_url) #다시 맵으로가서 검색함
            time.sleep(1)
            
            return "full_reserve"
        except exceptions.NoSuchElementException :
            print("백신 예약 완료")


while True:
    #버튼을 눌렸을떄 그게 f2이라면 -> 새로고침 버튼을 찾아보고 -> 있으면 새로고침 / 없으면 다시 키입력받기 
    if refresh_yn == 'f2':
        try: 
            #새로고침 버튼 찾기
            refresh_btn = driver.find_element_by_xpath('//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/div[2]/a')
            
            #맵 url 저장
            map_url = get_map_url()
            
            refresh_btn.click()
            
            time.sleep(1)
            
            print("새로고침중" + str(refresh_cnt))
            vacine_found = find_all_vaccine()
            if vacine_found == False: 
                refresh_cnt += 1
            else: 
                reserve_btn = driver.find_element_by_xpath('//*[@id="app-root"]/div/div/div[3]/div/div/ul/li/div[2]/div[1]/a')
                reserve_btn.click()
                #예약 결과 값을 집어넣어줌
                result_reserve = reserve_start()
                
                print(result_reserve)
                
                if result_reserve == "wrong_page":
                    refresh_yn = keyboard.read_key()
                    refresh_cnt = 1
                elif result_reserve == "full_reserve":
                    refresh_yn = "f2"
                    refresh_cnt = 1
                continue
        
        except exceptions.NoSuchElementException as e:
            print("페이지 변경으로 인해 새로고침 종료")
            result_reserve = reserve_start()
            if result_reserve == "full_reserve":
                refresh_yn = "f2"
                refresh_cnt = 1
                continue
            else :
                refresh_yn = keyboard.read_key()
                refresh_cnt = 1
                continue
        except exceptions.ElementClickInterceptedException :
            print("페이지 클릭으로 인한 새로고침 종료 재시작 위해 press F2")
            refresh_yn = keyboard.read_key()
            refresh_cnt = 1
            print("새로고침 카운트 재시작")
            continue
        except exceptions.StaleElementReferenceException :
            print("페이지 StaleElementReferenceException 으로 인한 재시작")
            # refresh_yn = keyboard.read_key()
            # refresh_cnt = 1
            # print("새로고침 카운트 재시작")
            continue
        except exceptions.WebDriverException :
            driver.get(url = map_url)
            #이전페이지 이동을 위해  1초 대기
            time.sleep(1)
            
    else :
        refresh_yn = keyboard.read_key()
        #print(refresh_yn)
