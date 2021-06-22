import os.path
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC,NGRAMWORDS

schema = Schema(docID=NUMERIC(stored=True), contents=TEXT, tags=NGRAMWORDS(stored=True))
index_dir = "D:/2020/학교/2학기/데이터관리와분석/DMA_project3/DMA_project3/SE/index"

if not os.path.exists(index_dir):
    os.makedirs(index_dir)

ix = create_in(index_dir, schema)
writer = ix.writer()

st = PorterStemmer()
lt = WordNetLemmatizer()

with open('D:/2020/학교/2학기/데이터관리와분석/DMA_project3/DMA_project3/SE/doc/document.txt', 'r') as f:
    text = f.read()
    docs = text.split('   /\n')[:-1]
    stopWords = set(stopwords.words('english'))
    stopWords.update(['would'])
    for doc in docs:
        br = doc.find('\n')
        docID = int(doc[:br])
        doc_text = doc[br + 1:]

        pre_doc = []
        doc_text = doc_text.replace('\n', ',')
        doc_text = doc_text.replace(' ', ',')
        l = doc_text.split(',')
        try:
            for x in range(len(l)):
                l.remove('')
        except:
            pass

        for word in l:
            if word.lower() not in stopWords:
                word = lt.lemmatize(word)
                word = st.stem(word)
                pre_doc.append(word)

        doc_text = ' '.join(pre_doc)
        writer.add_document(docID=docID, contents=doc_text)

writer.commit()