from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans
import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
import numpy as np
import re

categories = ['Business', 'Entertainment', 'Living', 'Metro', 'Shopping', 'Sports', 'Tech']

data = load_files(container_path='text_all', categories=categories, shuffle=True,
                    encoding='utf-8', decode_error='replace')

# TODO - Data preprocessing and clustering
def preprocessing(text):
    text = re.sub('[^a-zA-Z0-9 \n\.]+', '', text)
    words = word_tokenize(text)
    tokens = [word.lower() for word in words]
    tokens = [token for token in tokens if len(token)>=3]
    st = LancasterStemmer()
    tokens = [st.stem(token) for token in tokens]
    return tokens

def data_processor(raw_data):
    df = pd.DataFrame(raw_data.data, columns=['article'])
    df['article'] = df['article'].apply(lambda x: preprocessing(x))
    df['article'] = df['article'].apply(lambda x: ' '.join(x))
    return df

df = data_processor(data)
new_data = np.asarray(df['article'])
vectorizer = CountVectorizer(stop_words='english', max_df=0.7)
transformer = TfidfTransformer()
data_trans = transformer.fit_transform(vectorizer.fit_transform(new_data))
clst = KMeans(n_clusters=7, n_init = 10, max_iter= 300, random_state=33)
clst.fit(data_trans)

print(metrics.v_measure_score(data.target, clst.labels_))

#클러스터별 대표 단어 추출
'''features = vectorizer.get_feature_names()
result = pd.DataFrame()
for i in range(7):
    center = clst.cluster_centers_[i]
    sorted_center = np.argsort(center)[::-1][:20]
    best_feature = [features[i] for i in sorted_center]
    result['cluster%i' % i] = best_feature
result'''

#PCA를 활용한 차원 축소 후 클러스터 시각화
'''from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans
import os


clusters = clst.labels_.tolist()
labels = categories
colors = {0: 'black', 1: 'red', 2: 'yellow', 3: 'green', 4:'blue', 5: 'purple', 6: 'pink'}

pca = PCA(n_components=2).fit_transform(data_trans.toarray())
xs, ys = pca[:, 0], pca[:, 1]
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))
# df = pd.DataFrame(dict(x=xs, y=ys, label=labels))
groups = df.groupby('label')

# set up plot
fig, ax = plt.subplots(figsize=(17, 9))  # set size
ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

# iterate through groups to layer the plot
for idx, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=8,
            color=colors[idx], mec='none')
    ax.set_aspect('auto')
    ax.tick_params( \
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params( \
        axis='y',  # changes apply to the y-axis
        which='both',  # both major and minor ticks are affected
        left='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelleft='off')

plt.show()  # show the plot
print(metrics.v_measure_score(data.target, clst.labels_))'''