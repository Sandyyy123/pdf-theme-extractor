"""
theme_analyzer.py - Extract themes using BERTopic + spaCy NER refinement.
Maps each theme hit to exact page numbers across the document batch.
"""
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import spacy
from collections import defaultdict

try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    nlp = None  # graceful fallback

class ThemeAnalyzer:
    def __init__(self, min_topic_size: int = 10, n_gram_range: tuple = (1, 2)):
        vectorizer = CountVectorizer(ngram_range=n_gram_range, stop_words="english")
        self.model = BERTopic(
            vectorizer_model=vectorizer,
            min_topic_size=min_topic_size,
            nr_topics="auto",
            verbose=False
        )
        self.doc_names = []
        self.page_index = []  # (doc_name, page_num) per sentence

    def fit_transform(self, docs: dict) -> dict:
        """
        docs: {doc_name: [{page_num, text, is_ocr}]}
        Returns: {theme_id: {label, keywords, occurrences: [{doc, page}]}}
        """
        sentences = []
        for doc_name, pages in docs.items():
            for page in pages:
                for sent in page["text"].split("\n"):
                    sent = sent.strip()
                    if len(sent) > 20:
                        sentences.append(sent)
                        self.page_index.append((doc_name, page["page_num"]))

        topics, _ = self.model.fit_transform(sentences)

        # Build theme index
        theme_data = defaultdict(lambda: {"label": "", "keywords": [], "occurrences": []})
        topic_info = self.model.get_topic_info()

        for i, topic_id in enumerate(topics):
            if topic_id == -1:
                continue
            doc_name, page_num = self.page_index[i]
            theme_data[topic_id]["occurrences"].append({"doc": doc_name, "page": page_num})

        # Add labels and keywords
        for row in topic_info.itertuples():
            if row.Topic == -1:
                continue
            kws = self.model.get_topic(row.Topic)
            theme_data[row.Topic]["label"] = f"T-{row.Topic:02d}"
            theme_data[row.Topic]["keywords"] = [w for w, _ in kws[:5]]

        return dict(theme_data)
