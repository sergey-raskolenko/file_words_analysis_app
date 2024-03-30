import re
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('russian')

REGULAR = r'[^\w\s]'
REGULAR_URL = r'(http\S+)|(www\S+)|([\w\d]+www\S+)|([\w\d]+http\S+)'


def clean_text(text) -> List[str]:
    """
    Функция очищает текст от специальных символов, ссылок, чисел и пробелов.
    """
    text = text.lower()

    text = re.sub(REGULAR, '', text)
    text = re.sub(REGULAR_URL, r'', text)
    text = re.sub(r'(\d+\s\d+)|(\d+)', '', text)
    text = re.sub(r'\s+', ' ', text)

    tokenized_text = word_tokenize(text, language='russian')

    return [word for word in tokenized_text if word not in stop_words]
