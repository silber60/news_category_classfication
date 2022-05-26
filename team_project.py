from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

pages = [110, 110, 110, 78, 110, 66] #아무 페이지 누르고 위 주소를 500으로 변환
# 모두 비슷한 데이터량일 수 있게 110로 통일
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'

options = webdriver.ChromeOptions() #크롬드라이버 설치
options.add_argument(('lang=ko_KR')) #브라우저 언어 설정을 한국어로
options.add_argument('--no-sandbox') #다른 시스템에선 이게 필요
options.add_argument('--disable-dev-shm-usage') #리눅스에서 필요
options.add_argument('disable-gpu') #다른 시스템에서 열릴 수 있게 모두 준비

driver = webdriver.Chrome('./chromedriver', options=options) #exe제외
df_titles = pd.DataFrame() # 빈 데이터프레임 제작
# 색션별로 돌아가는 for문과 색션안에서 돌아가는 for문 필요
for i in range(0, 6) :
    titles = []
    for j in range(1, pages[i]+1) : #색션별 모든 페이지 크롤링 가능
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5) :
            for l in range(1, 6) :
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
                try :
                    title = driver.find_element_by_xpath(x_path).text #text만 갖고오기
                    title = re.compile('[^가-힣 ]').sub('', title)
                    titles.append(title) # 먼저 list에 넣기
                except NoSuchElementException as e : # x_path가 없는 페이지
                    time.sleep(0.5)
                    try :
                        title = driver.find_element_by_xpath(x_path).text
                        title = re.compile('[^가-힣 ]').sub('', title)
                        titles.append(title)
                    except :
                        try :
                            x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                            title = re.compile('[^가-힣 ]').sub('', title)
                            titles.append(title)
                        except :
                            print('no such enlement')
                except StaleElementReferenceException as e : #로딩 중 페이지가 안만들어짐
                    print(e)
                    print(category[i], j, 'page', k * l ) # 몇 페이지인지, 몇번째 기사인지
                except :
                    print('error')
        if j % 30 == 0 :
            df_section_titles = pd.DataFrame(titles, columns=['titles']) #list들을 데이터프레임에 넣기
            df_section_titles['category'] = category[i]
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
            df_titles.to_csv('./crawling_data_{}_{}'.format(category[i], j), index=False) #인덱스 없이 데이터만 저장
            titles = [] #저장하고 clear
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
    df_titles.to_csv('./crawling_data_{}_{}.csv'.format(category[i], j), index=False)
    titles = []
driver.close()

