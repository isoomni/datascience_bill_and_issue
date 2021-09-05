# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 18:58:30 2021

@author: samsung
"""


#2020 뉴스 제목 데이터 파일을 연다 (사전에 자연어추출로 단어만 뽑아낸 input 파일)
n_data = open("C:\\Users\\samsung\\Desktop\\2021 1학기\\데이터베이스\\기사제목단어.txt", 'rt', encoding='UTF8')
news = n_data.readlines()

#2020 법률안 내용 데이터 파일을 연다 (사전에 자연어추출로 단어만 뽑아낸 input 파일)
l_data = open("C:\\Users\\samsung\\Desktop\\2021 1학기\\데이터베이스\\발의법의안내용.txt",'rt', encoding='UTF8')
law = l_data.readlines()



#뉴스와 법률 데이터에서 stopwords를 지정한다
with open("C:\\Users\\samsung\\Desktop\\2021 1학기\\데이터베이스\\stopwords-ko.txt", encoding="utf8") as f:
    stopwords = f.readlines()

stopwords= [x.strip() for x in stopwords]
n_stopwords =['것' , '등', '전', '첫', '만에', '관련', '신규', '새', '후', '오늘', '올해', '새해', '문재인', '대통령', '문 대통령', '코로나19', '정부', '검찰', '청와대', '의혹', '논란', '야당', '여당', '논의', 
                   '논의', '세계', '발표', '일부', '증가', '감소', '검토', '국내', '여야', '추가', '연기', '사과', '모두', '일부', '반대', '서울', '필요', '통과', '기록', '요청', '역대', '지속', '취소', '내년', '우려',
                   '공천', '입국', '붕괴', '결정', '확정', '추경', '추가', '발생', '총선', '제명', '사과', '오거돈', '온라인', '개학','금일', '등교', '중국', '미국','일본', '북한', '사건', '발표', '공방', '회장', '백신',
                   '추진', '내년', '트럼프', '바이든','지시', '혐의', '개최','전국', '시작', '중단', '오늘부터', '발언', '중', '명', '민주당', '통합당','국민의 힘', '최대',
                    '코로나', '코로나19', '확진자', '확진', '확진자 추가', '확진자 발생', '코로나19 확진자', '신종코로나', '감염', '감염 확산','집단', '집단 감염', '집단감염', '확산', '거리두기', '마스크', '화이자', 'AZ', '접종', '코로나 사망자', '백신 승인', '혈전', '1차', '2차', '3차', '재난지원금', '사회적', '생활 속' ]

l_stopwords = ['관한','구조구','법률','법','및','관','지원','관리','특례법','특별법','제안이유','주요내용','\n','함','것임',
'및','의','등','위','것','그','수','이','로','뿐','은','안','항','임','대한','관','못','또','다시','를','중','제안','이유','규정','처벌',
'제공','단계','관련','포함','성과','국가','위해','과','때','명','로부터','내용','삭제','발생','후','년','현행법','현재','실행','상황',
'최근','위해','국민','경우','또한','해당']

for stopword in n_stopwords:
    stopwords.append(stopword)
    
for stopword in l_stopwords:
    stopwords.append(stopword)
    
    


#뉴스 데이터에서 stopwords를 제외하고, unique words 모두 찾는다
n_words = []
for line in news:
    words= line.split()
    for word in words:
        if word not in stopwords:
            if word not in n_words:
                n_words.append(word)

#print(set(n_words)) 뉴스 데이터에 나온 모든 단어 목록 확인 후 저장하기
with open('news2020_uniquewords.txt', 'w',encoding="utf8") as f1:
    for element in n_words:
        f1.write(element + "\n")
    f1.close()

fin_news_data = str(n_words)
            
            
#법률 데이터에서 stopwords 제외하고 unique words 모두 찾는다
            
l_words = []
for line in law:
    words= line.split()
    for word in words:
        if word not in stopwords:
            if word not in l_words:
                l_words.append(word)

#print(set(l_words)) 법의안 내용에 나온 모든 단어 목록 확인 후 저장하기
with open('law2020_uniquewords.txt', 'w',encoding="utf8") as f2:
    for element in l_words:
        f2.write(element + "\n")
    f2.close()

fin_law_data = str(l_words)           


#jaccard 정의하기
def jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    print ("Jaccard Simliarity index is", float(len(c)) / (len(a) + len(b) - len(c)))
    print ("There are " + len(c)+ " common words.")  #겹치는 단어 갯수 출력하기 
   
		with open('words in law and news.txt','w', encoding='utf8') as f3:
        f3.write(str(c))   #겹치는 단어 목록 저장하기 
        f3.close()

#jaccard similarity 적용해보기
jaccard_sim(fin_news_data, fin_law_data)