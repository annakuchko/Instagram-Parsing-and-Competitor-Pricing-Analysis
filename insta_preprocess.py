#!/usr/bin/env python
# coding: utf-8

import pandas as pd
get_ipython().system('pip install pymystem3')
import re
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('wordnet')
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv('insta_comments.csv')
df = df.drop('Unnamed: 0', axis = 1).drop_duplicates()

def clear_comm(s):
    s = re.sub(r"₽", ' ', s)
    s = s.replace(r".", '')
    s = re.sub(r"\b\d(?: ?\d{2,5})\b год", '', s)
    s = re.sub(r"\b\d(?: ?\d{2,5})\b-", '', s)
    s = re.sub(r"\b\d(?: ?\d{2,5})\b кв м", '', s)
    s = re.sub(r"\b\d(?: ?\d{2,5})\b см", '', s)
    s = re.sub(r"артикул \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"размер \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Размер \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"сек.\b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Артикул \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Размеры – \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"офис \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Артикул: \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Доставки от \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"артикул-\b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"рост \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"секции \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"секция \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"Цена доставки \b\d(?: ?\d{2,5})\b", '', s)
    s = re.sub(r"2021", '', s)
    s = re.sub(r"2020", '', s)
    s = re.sub(r"2019", '', s)
    s = re.sub(r"1997", '', s)
    s = re.sub(r"666", '', s)
    s = re.sub(r"210", '', s)
    s = re.sub(r"158", '', s)
    s = re.sub(r"101", '', s)
    s = re.sub(r"106", '', s)
    s = re.sub(r"147", '', s)
    s = re.sub(r"777", '', s)
    s = re.sub(r"р", ' р ', s)
    s = re.sub(r"руб", ' руб ', s)
    s = re.sub(r"Ново-Садовая 305", '', s)
    
    
    return s

df['comments_p'] = df['comments'].apply(clear_comm)
def extract_price(s):
    #save the first price mentioned
    r = re.search(r"\b\d(?: ?\d{2,4})\b", s)
    if r:
        result = (str(r.group(0)).replace(" ", ""))
    else:
        result = 0
    return result

def extract_hashtag(s):
    hashtags = re.findall(r"#(\w+)", s)
    return hashtags


df['price'] = df['comments_p'].apply(extract_price)
df['hashtag'] = df['comments'].apply(extract_hashtag)
df['price'] = df.price.astype(int)
df = df[df.price!=0]
df['comments']=[re.sub(r"[-()\"#/@;:<>[] < > {}`+=~|.!?,]", " ", item) for item in df['comments']]

def clear_comm1(s):
    s = re.sub(r"😍", ' ', s)
    s = re.sub(r"❤", ' ', s)
    s = re.sub(r"🌲", ' ', s)
    s = re.sub(r"\n", ' ', s)
    s = re.sub(r"▶", ' ', s)
    s = re.sub(r"♥️", ' ', s)
    s = re.sub(r"#", ' ', s)
    
    
    return s
    
df['comments'] = df['comments'].apply(clear_comm1)


def extract_likes(s):
    s = re.search(r"\b\d(?: ?\d{1,4})\b", s)
    if s:
        s = (s.group(0)).replace(" ", "")
    else:
        s = 0
    
    return int(s)
df['likes'] = df['likes'].apply(extract_likes)


df_profiles = pd.read_csv('df_profiles.csv')
df_profiles = df_profiles.join(df_profiles.stats.str.split('\n',expand=True))
df_profiles.columns = ['user_id', 'stats', 'posts', 'публикации','subscribers','подписчики', 'subscriptions', 'подписки']
df_profiles=df_profiles.drop(['stats', 'публикации', 'подписчики', 'подписки'], axis = 1)

def extract_zeros(s):
    s = re.sub(r"тыс.", '000', s)
    s = re.sub(r"млн.", '000000', s)
    s = re.sub(r",", '', s)
    s = re.sub(r" ", '', s)
    return s

df_profiles['subscribers'] = df_profiles['subscribers'].apply(extract_zeros)
df_profiles['posts'] = df_profiles.posts.apply(lambda s: int(re.sub(r" ", '', s)))
df_profiles['subscriptions'] = df_profiles.subscriptions.apply(lambda s: int(re.sub(r" ", '', s)))


df = df.merge(df_profiles, on = 'user_id')


#функция для лемматизации и удаления стоп-слов
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

#Preprocess function
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords              and token != " "               and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    
    return text

import numpy as np

df['desc_pr'] = np.nan
for i, row in enumerate(df['desc']):
    if i%1==0:
        print(i)
    df['desc_pr'][i] = preprocess_text(row)

    
df['comments_pr'] = np.nan
for i, row in enumerate(df['comments']):
    if i%1 ==0:
        print(i)
    df['comments_pr'][i] = preprocess_text(row)
    
df.to_csv('df_with_lemmas.csv')

