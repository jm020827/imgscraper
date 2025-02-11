from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import sys


# headless 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("headless") # 크롬 창이 뜨지 않고 실행될 수 있도록 설정
driver = webdriver.Chrome(options=options)

# 검색 페이지 접속
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")



def search_image(inputQuery):
    # 검색 페이지 접속
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    # 검색어 입력
    search_query = inputQuery[0]
    elem = driver.find_element(By.CSS_SELECTOR,"#APjFqb")
    elem.send_keys(search_query + "나무위키")
    elem.send_keys(Keys.RETURN)
    print(search_query, "의 이미지를 검색합니다.")

    # 이미지 검색 결과 수집
    time.sleep(1)
    images = driver.find_elements(By.XPATH, "//div[@class='H8Rx8c']")
    print("images ", images)
    print("images length", len(images))

    # 저장할 이미지 개수 입력 및 저장 디렉토리 생성
    count = 1
    desired_count = 1#int(input("저장할 이미지 개수를 입력하세요: "))
    save_dir = "./images"
    if not os.path.exists(save_dir):
        print("images 디렉토리를 생성합니다.")
        os.makedirs(save_dir)

    print(desired_count, "개의 이미지를 저장합니다.")

    # 이미지 저장 반복문
    for image in images:
        if count > desired_count: # 저장할 이미지 개수를 초과하면 종료
            break
        try:
            # 이미지 클릭 후 이미지 URL 추출
            image.click()
            time.sleep(2)
            imgUrl = driver.find_element(By.CSS_SELECTOR,"#Sva75c > div.A8mJGd.NDuZHe > div.LrPjRb > div > div.BIB1wf.EIehLd.fHE6De.Emjfjd > c-wiz > div > div.v6bUne > div.p7sI2.PUxBg > a > img.sFlh5c.FyHeAf.iPVvYb").get_attribute("src")
            print("이미지 URL: ", imgUrl)


            # 이미지 저장
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            save_path = os.path.join(save_dir,search_query + ".jpg")
            urllib.request.urlretrieve(imgUrl, save_path)

            count = count + 1
        except:
            pass
        if count > desired_count:
            break

        
        

while(True):
    n = int(input("데이터의 수(엔터로 구분) : "))
    input_query = [str(sys.stdin.readline().strip()).split(" ") for i in range(n)]
    for i in range(n):
        search_image(input_query[i])
    
    if input_query == "exit":
        # 크롬 드라이버 종료
        print("이미지 저장이 완료되었습니다.")
        driver.quit()
        break