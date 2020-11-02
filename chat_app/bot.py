import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import random
import numpy as np
import string

import bs4 as bs
import urllib
import requests
import re

url = 'https://en.wikipedia.org/wiki/Dermatitis'

raw_html = urllib.request.urlopen(url)
raw_html = raw_html.read()

article_html = bs.BeautifulSoup(raw_html, 'html.parser')

article_paragraphs = article_html.find_all('p')

article_text = ''

for para in article_paragraphs:
    article_text += para.text

article_text = article_text.lower()

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

article_sentences = nltk.sent_tokenize(article_text)
article_words = nltk.word_tokenize(article_text)

wnlemmatizer = nltk.stem.WordNetLemmatizer()


def perform_lemmatization(tokens):
    return [wnlemmatizer.lemmatize(token) for token in tokens]


punctuation_removal = dict((ord(punctuation), None)
                           for punctuation in string.punctuation)


def get_processed_text(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))


greeting_inputs = ("hey", "good morning", "good evening",
                   "morning", "evening", "hi", "whatsup")
greeting_responses = ["hey", "hello, how you doing",
                      "hello", "Welcome, I am good and you"]


def generate_greeting_response(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs:
            return random.choice(greeting_responses)


def generate_response(user_input):
    robo_response = ''
    article_sentences.append(user_input)

    word_vectorizer = TfidfVectorizer(
        tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(article_sentences)
    similar_vector_values = cosine_similarity(
        all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        robo_response = robo_response + "I am sorry, I could not understand you"
        return robo_response
    else:
        robo_response = robo_response + \
            article_sentences[similar_sentence_number]
        return robo_response


word_vectorizer = TfidfVectorizer(
    tokenizer=get_processed_text, stop_words='english')
all_word_vectors = word_vectorizer.fit_transform(article_sentences)


similar_vector_values = cosine_similarity(
    all_word_vectors[-1], all_word_vectors)

similar_sentence_number = similar_vector_values.argsort()[0][-2]
