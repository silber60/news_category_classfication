from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

category = ['Politics', 'Economic', 'Social', 'Culture', 'Word', 'IT']

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' #주소
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
# 검사 - header - 아무거나 - 맨 아래 user-agent
resp = requests.get(url)
# print(resp)
# print(list(resp))
# print(resp)

soup = BeautifulSoup(resp.text)
# print(soup)

for i in range(6) :
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i) # 100-101-102 로 갈 수 있게

    title_tags = soup.select('.cluster_text_headline') #기사 제목들에 모두 들어감
    print(title_tags)

    titles = []
    for title_tag in title_tags : #제목만 들어올 수 있도록
        title = re.compile('[^가-힣 ]'.sub(title_tag.text))
        title.append(title)
        df_section_titles = pd.DataFrame(titles, columns=['titles'])
        df_section_titles['category'] = category[i]
        df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                              ignore_index=True) #인덱스도 새로 만들어지게(원래는 무시)
    #이 문장에서 한글과 띄어쓰기를 제외한(^제외의 뜻)나머지를 뺀다
# 문장부호 같은건 삭제할 필요가 있음
# 협의된 -> 협의 된 / 형태소 단위로 잘라줘야함(조사는 버리기)
# re를 활용해서 영어나 특수문자 다 빼고 한글만 남김
# 이걸 데이터프레임을 만들고 카테고리를 만들어서 각 사항에 넣어줄 예정

print(titles)
df_titles.info()
print(df_titles['category'].value_counts())


