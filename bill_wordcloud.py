import numpy as np
import pandas as pd

from konlpy.tag import Okt
from wordcloud import WordCloud,STOPWORDS
from wordcloud import ImageColorGenerator

from sklearn.feature_extraction.text import TfidfVectorizer

%matplotlib inline  

import matplotlib as mpl  # 기본 설정 만지는 용도
import matplotlib.pyplot as plt # 그래프 그리는 용도
import matplotlib.font_manager as fm # 폰트 관련 용도
import seaborn as sns

import plotly.express as px
import plotly.graph_objs as go
import plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import re
from collections import Counter
import pyperclip
from PIL import Image

from tqdm.notebook import tqdm

import warnings
warnings.filterwarnings('ignore')

#데이터 
process_raw = pd.read_csv(r'/content/process.csv', encoding='UTF8')
suggest_raw = pd.read_csv('/content/suggest.csv', encoding='UTF8')
process = process_raw.copy()
suggest = suggest_raw.copy()
print(process_raw.shape)
print(suggest_raw.shape)

#suggest 파일에서 필요한 행과 열 추출
suggest.PROC_RESULT.unique()

suggest['PROC_RESULT_COMB'] = suggest['PROC_RESULT'].replace({'원안가결':'가결',
             #대안 반영 폐기와 수정안반영폐기의 경우 다른 의안과 통합된 케이스이므로 가결에 포함시킨다                                                 '수정가결':'가결',
suggest.PROC_RESULT_COMB.unique()                                                              '대안반영폐기':'가결',
                                                              '수정안반영폐기':'가결',
plt.subplot(1,2,1)

ax1 = sns.countplot(data = suggest, x = 'PROC_RESULT_COMB', palette = 'husl')
plt.title('전체 발의안 처리 결과')
plt.xlabel('')
plt.ylabel('')

suggest_notnull = suggest[suggest.PROC_RESULT_COMB.notnull()].shape[0]
for p in ax1.patches:
    ax1.annotate('{:.2f}%'.format(p.get_height()/suggest_notnull * 100), (p.get_x()+0.15, p.get_height()+1))    
    
plt.subplot(1,2,2)  

suggest_final = suggest[(suggest.PROC_RESULT_COMB == '가결')|(suggest.PROC_RESULT_COMB == '부결')]
ax2 = sns.countplot(data = suggest_final, x = 'PROC_RESULT_COMB', palette = 'husl')
plt.title('본회의 상정 발의안 처리 결과')
plt.xlabel('')
plt.ylabel('')

suggest_final_notnull = suggest_final[suggest_final.PROC_RESULT_COMB.notnull()].shape[0]
for p in ax2.patches:
    ax2.annotate('{:.2f}%'.format(p.get_height()/suggest_final_notnull * 100), (p.get_x()+0.3, p.get_height()+1))                                                              '임기만료폐기':'폐기',
                                                           '회기불계속폐기':'폐기'})

#가결을 기준으로 행렬 추출하기
suggest_soom = suggest.loc[:, ['AGE', 'BILL_NAME', 'PROPOSE_DT', 'PROC_RESULT']]

# 21대에서 발의한 법의안만 선택
suggest_soom_21 = suggest_soom[suggest_soom['AGE'] == 21]

# 21대에서 발의한 법의안 중 그 결과가 '가결'에 해당하는 것만 남긴다.
suggest_soom_21_nonpass = suggest_soom_21[suggest_soom_21['PROC_RESULT'].isin(['철회', '폐기', '임기만료폐기', '부결', '비상국무회의로이관', '회기불계속폐기']) ].index
suggest_soom_21_pass = suggest_soom_21.drop(suggest_soom_21_nonpass)
suggest_soom_21_pass = suggest_soom_21_pass.dropna()
suggest_soom_21_pass = suggest_soom_21_pass.reset_index(drop=True)  # reset_index : index를 reset해야 온전한 데이터 프레임이 되고 후에 자연어 처리 할 때 사용 가능해 진다.
suggest_soom_21_pass

#법안 제목 분석
okt = Okt()
suggest_soom_21_pass_name = ''.join(suggest_soom_21_pass['BILL_NAME'])
suggest_soom_21_pass_name = suggest_soom_21_pass_name.replace('일부개정법률안','')
suggest_soom_21_pass_noun = okt.nouns(suggest_soom_21_pass_name)

stopwords = set(STOPWORDS) 
stopwords.add('관한'); stopwords.add('구조구'); stopwords.add('법률'); stopwords.add('법'); stopwords.add('및'); stopwords.add('관')
stopwords.add('특례법'); stopwords.add('특별법');
# 글꼴 저장
font_path = '/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'

#워드 클라우드 생성
worldcloud_suggest_soom_21_pass = WordCloud(font_path=font_path,stopwords=stopwords,background_color='white',
                     width=1000,height=1000, max_words =100, min_font_size = 10).generate(' '.join(suggest_soom_21_pass_noun))

plt.figure(figsize=(15,15))
plt.subplot(1, 2, 1)
plt.imshow(worldcloud_suggest_soom_21_pass, interpolation='lanczos') #이미지의 부드럽기 정도
plt.axis('off') #x y 축 숫자 제거