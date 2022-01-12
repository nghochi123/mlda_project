import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import gradio as gr
from heapq import nlargest
import time


def summarize(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # GET RID OF THE \n's as well.

    punc = punctuation + '\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punc:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}

    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.3)

    summary = nlargest(select_length, enumerate(
        sentence_scores.items()), key=lambda x: x[1][1])

    # summary = nlargest(select_length, enumerate(sentence_scores), key=lambda x: x[1])

    summary = sorted(summary, key=lambda x: x[0])

    # final_summary = '\n\n'.join([str.strip(word.text) for word in summary])

    final_summary = '\n\n'.join(
        [str.strip(word[1][0].text) for word in summary])

    return final_summary


gr.Interface(fn=summarize,
             inputs='textbox',
             outputs='textbox').launch()
