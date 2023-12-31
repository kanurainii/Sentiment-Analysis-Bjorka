# -*- coding: utf-8 -*-
"""Sentiment Analysis Bjorka.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZHoQ-2fwwtlD0VnIiUxUc-XYc7Q6GAjs

# **1. Load Dataset**
"""

# Mengimport data
import pandas as pd
data = pd.read_csv('/content/cleaned_dataset baru (4).csv')
data

"""# **2. Data Exploration**"""

# Mengetahui Informasi Dataset yang digunakan
data.info()

# Melihat data yang kosong
data.isna().sum()

# Menampilkan diagram batang jumlah dataset
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(7,6))
stars_histogram = data["Label"].value_counts().sort_index()
stars_histogram.plot(kind='bar', width=0.7, color='green')
plt.xlabel('Label')
plt.ylabel('Komentar')

plt.tight_layout()
plt.show()

# Menghitung jumlah label
x = data.drop(['Label'], axis=1)
y = data['Label']
y.value_counts()

"""# **3. Ubah Label Kategorik Menjadi Angka**"""

data['Sentimen'] = data['Label'].apply(lambda x: 1 if x == 'positive' else 0)
data = data.drop(columns = 'Label')
data.head()

"""# **4. Preprocessing Data**

# Case Folding
"""

#proses case folding
import re
def casefolding(comment):
  comment = comment.lower() # mengubah huruf besar menjadi huruf kecil
  comment = comment.strip(" ") # menghilangkan spasi berlebih
  comment = re.sub(r'[^a-zA-Z\s]', '', comment) # menghilangkan karakter selain huruf

  return comment

data ['Komentar'] = data['Komentar'].apply(casefolding)
data.head(10)

"""# Tokenizing"""

# proses tokenizing
def token(comments):
  nstr = comments.split(' ')
  dat= []
  a = -1
  for hu in nstr:
    a = a + 1
  if hu == '':
    dat.append(a)
  p = 0
  b = 0
  for q in dat:
    b = q - p
    del nstr[b]
    p = p + 1
  return nstr

data ['Komentar'] = data['Komentar'].apply(token)
data.head(10)

"""# Filtering / Stopword Removing"""

!pip install sastrawi

#proses filtering/stopword removing
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def stopwords_removal(comments):
  filtering = stopwords.words('indonesian','english')
  x = []
  data = []
  def myFunc(x):
    if x in filtering:
      return False
    else:
        return True
  fit = filter(myFunc, comments)
  for x in fit:
    data.append(x)
  return data

data ['Komentar'] = data['Komentar'].apply(stopwords_removal)
data.head(10)

"""# **Stemming**"""

# proses stemming
from sklearn.pipeline import Pipeline
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming(comments):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    for w in comments:
      dt = stemmer.stem(w)
      do.append(dt)
    d_clean=[]
    d_clean=" ".join(do)
    print(d_clean)
    return d_clean

data ['Komentar'] = data['Komentar'].apply(stemming)
data.head(10)

"""# **5. Menampilkan Wordcloud**"""

!pip install wordcloud

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
import pandas as pd
import matplotlib.pylab as plt
from PIL import Image
import numpy as np

from wordcloud import WordCloud

# kata yang sering muncul (positif dan negatif)
wordcloud = WordCloud(width = 1200, height= 1200, background_color = 'white', max_words = 1000, min_font_size = 18).generate(str(data))

fig = plt.figure(figsize = (8,8), facecolor = None)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

"""# **6. Unduh Data Clean**"""

data.to_csv('data_clean.csv', index=False)
data_clean = pd.read_csv('data_clean.csv', encoding='latin1')
data_clean.head()

"""# **7. Mengubah Data Menjadi Numpy Array**"""

# Mengubah data menjadi numpy array
Komentar = data['Komentar'].values
Sentimen = data['Sentimen'].values

Komentar

Sentimen

"""# **8. Splitting Dataset**"""

#splitting data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split (Komentar, Sentimen, test_size=0.2, random_state = 42)

len(X_train)

len(X_test)

"""# **9. Pembobotan TF-IDF**"""

from sklearn.feature_extraction.text import TfidfVectorizer

h_tfidf = TfidfVectorizer()

# Mengubah data latih menjadi vektor TF-IDF
X_train = h_tfidf.fit_transform(X_train)

# Mengubah data uji menjadi vektor TF-IDF
X_test = h_tfidf.transform(X_test)

print(h_tfidf)

"""# **10. Naive Bayes**

# Modelling Classification: Naive Bayes
"""

from sklearn.naive_bayes import MultinomialNB

# Initialize and train the Naive Bayes classifier
nb_classifier = MultinomialNB()

# Training Model
nb_classifier.fit(X_train, y_train)

# Perform predictions on test data
y_prednb = nb_classifier.predict(X_test)

"""# Evaluasi Model: Naive Bayes"""

from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

# Menampilkan Confusion Matrix Model Gaussian Naive Bayes
conf_matrixgnb = confusion_matrix(y_test, y_prednb)
fig, ax = plot_confusion_matrix(conf_mat=conf_matrixgnb, figsize=(6, 6), cmap=plt.cm.Greens)
plt.xlabel('Predictions', fontsize=14)
plt.ylabel('Actuals', fontsize=14)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

from sklearn.metrics import classification_report
print(classification_report(y_test, y_prednb, target_names = ['0','1']))

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Pisahkan data berdasarkan label sentimen (misalnya 1 untuk positif, 0 untuk negatif)
positive_data = data[data['Sentimen'] == 1]
negative_data = data[data['Sentimen'] == 0]

# Menggabungkan kata-kata untuk word cloud positif dan negatif
positive_text = ' '.join(positive_data['Komentar'])
negative_text = ' '.join(negative_data['Komentar'])

# Buat word cloud untuk kata-kata positif
wordcloud_positive = WordCloud(width=1200, height=1200, background_color='white', max_words=1000, min_font_size=18).generate(positive_text)

# Buat word cloud untuk kata-kata negatif
wordcloud_negative = WordCloud(width=1200, height=1200, background_color='white', max_words=1000, min_font_size=18).generate(negative_text)

# Tampilkan word cloud kata-kata positif
fig = plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud_positive)
plt.axis('off')
plt.title('Word Cloud Kata Positif')
plt.show()

# Tampilkan word cloud kata-kata negatif
fig = plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud_negative)
plt.axis('off')
plt.title('Word Cloud Kata Negatif')
plt.show()

"""# **11. C.45**

# **Modelling Classification: Decision Tree**
"""

from sklearn.tree import DecisionTreeClassifier

# Initialize and train the decision tree classifier
dt_classifier = DecisionTreeClassifier()

# Training Model Decision Tree
dt_classifier.fit(X_train, y_train)

# Perform predictions on test data
y_preddt = dt_classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

# Menampilkan Confusion Matrix Model Gaussian Naive Bayes
conf_matrixgnb = confusion_matrix(y_test, y_preddt)
fig, ax = plot_confusion_matrix(conf_mat=conf_matrixgnb, figsize=(6, 6), cmap=plt.cm.Greens)
plt.xlabel('Predictions', fontsize=14)
plt.ylabel('Actuals', fontsize=14)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

from sklearn.metrics import classification_report
print(classification_report(y_test, y_preddt, target_names = ['0','1']))

"""# **Knowladge Presentation**"""

X = data.drop(['Sentimen'], axis=1)
y = data['Sentimen']

y.value_counts()

# Show pie plot (Approach 1)
y.value_counts().plot.pie(autopct='%.2f')