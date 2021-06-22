import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
import CustomScoring as scoring
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

noun_tag=['NN', 'NNS', 'NNP', 'NNPS']
verb_tag=['VB', 'VBD', 'VBG', 'VBP', 'VBN', 'VBZ']
ad_tag=['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']

st = PorterStemmer()
lt = WordNetLemmatizer()

from nltk.corpus import wordnet

def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")

    with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        # with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:
        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup.factory(0.93))
        stopWords = set(stopwords.words('english'))
        stopWords.update(['would'])

        for qid, q in query_dict.items():
            new_q=""

            tagged_list = pos_tag(q.split(' '))
            for word_tag in tagged_list:
                if word_tag[0].lower() not in stopWords:
                    if word_tag[1] in noun_tag:
                        syn_list = []
                        for syn in wordnet.synsets(word_tag[0]):
                            for l in syn.lemmas():
                                word = l.name()
                                syn_list.append(word)

                        for syn_l in syn_list:
                            length = len(syn_list)
                            w = '^' + str(1 / length)
                            new_q += syn_l + w + ' '
                            pass
                        w = '^2.758'
                    elif word_tag[1] in ad_tag:
                        w = '^2.293'
                    elif word_tag[1] in verb_tag:
                        w = '^1'

                    word = word_tag[0]
                    word = st.stem(word)
                    word = lt.lemmatize(word)

                    new_q += word + w + ' '

            query = parser.parse(new_q.lower())
            results = searcher.search(query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]
    return result_dict
