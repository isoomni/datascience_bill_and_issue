# -*- coding: utf-8 -*-
"""
Created on Sat May 15 17:04:26 2021

@author: samsung
"""

#준비과정
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mtbpy import mtbpy

#데이터 준비
data = pd.read_csv(r"C:\\Users\\samsung\\Desktop\\2021 1학기\\데이터베이스\\article_bigkinds_21st.csv")
data = data.copy()

monthly = data[data.date.str.contains('2020년')]
text = ' '.join(monthly['title'])
  

#전처리_stopwords
stopwords = set(STOPWORDS)
stopwords.add('것');stopwords.add('등');stopwords.add('전');stopwords.add("첫");stopwords.add("만에");stopwords.add("관련");stopwords.add("신규");stopwords.add("새");stopwords.add("후");stopwords.add("오늘");stopwords.add("올해");stopwords.add("새해")

#전처리_무의미한 단어 제거
text = text.replace('%','').replace("'","").replace('"',"").replace("·","")
text = text.replace("故","").replace("前","")

#전처리_한자 변환
text = text.replace("文", "문재인 ").replace("英","영국").replace("檢","검찰").replace("野","야당").replace("美","미국").replace("軍","군").replace("北","북한").replace("日","일본").replace("反","반").replace("中", "중국").replace("與", "여당").replace("靑","청와대").replace("尹", "윤석열")

#전처리_stopwords 추가
stopwords.add('문재인');stopwords.add("대통령");stopwords.add("문");stopwords.add("코로나19");stopwords.add("정부");stopwords.add("검찰");stopwords.add("청와대");stopwords.add("의혹");stopwords.add("논란");stopwords.add("야당");stopwords.add("여당")

#stopwords 더 추가
morestop = ['논의', '세계', '발표', '일부', '증가', '감소', '검토', '국내', '여야', '추가', '연기', '사과', '모두', '일부', '반대', '서울', '필요', '통과', '기록', '요청', '역대', '지속', '취소', '내년', '우려','공천', '입국', '붕괴', '결정', '확정', '추경', '추가', '발생', '총선', '제명', '사과', '오거돈', '온라인', '개학','금일', '등교', '중국', '미국','일본', '북한', '사건', '발표', '공방', '회장', '백신', '추진', '내년', '트럼프', '바이든','지시', '혐의', '개최','전국', '시작', '중단', '오늘부터', '발언', '중', '명', '민주당', '통합당','국민의 힘', '최대']
stopwords.update(morestop)

covidstop = ['코로나', '코로나19', '확진자', '확진', '확진자 추가', '확진자 발생', '코로나19 확진자', '신종코로나', '감염', '감염 확산','집단', '집단 감염', '집단감염', '확산', '거리두기', '마스크', '화이자', 'AZ', '접종', '코로나 사망자', '백신 승인', '혈전', '1차', '2차', '3차', '재난지원금', '사회적', '생활 속']
stopwords.update (covidstop)
    

#워드 클라우드 만들기
final_wordcloud = WordCloud(font_path = 'C:\\Users\\samsung\\Desktop\\fonts\\NanumGothic.ttf',stopwords = stopwords, width = 1000, height = 1000, 
                background_color ='white', colormap="Set2",max_words=200,
                min_font_size = 5).generate(text)

#워드 클라우드 설정
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(final_wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()


#키워드 파일 만들기
with open('word2020.txt', 'w') as f:
    for word in final_wordcloud.words_:
        print(word, sep = '\n', file=f)