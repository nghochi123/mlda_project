# Text Summariser

Link to the Text Summariser can be found [here](https://colab.research.google.com/drive/1oSCNngYRFW5tdEDTO2-qVIAYmZensSTe?usp=sharing)
The Text Summariser shortens a block of text input by retrieving the most significant and important sentences in a text chunk. The project was created with the aid of the python SpaCy library.

## Introduction

Natural Language Processing (NLP) refers to the branch of artificial intelligence concerned with giving computers the ability to interpret and understand text and spoken words in the same way that human beings can. Natural Language Processing has a variety of different applications including chatbots and customer service programs. In our project, we've harnessed the technology of NLP to develop a text summariser bot.

## Method/Approach

In solving this problem, we decided to utilise the python SpaCy library, which is an industrial-strength NLP library specifically tailored for complex NLP tasks. For our text summariser bot, the input data is run through a series of processing steps before the final summarised text is derived.

### Step 1: Tokenization

In order for the computer to interpret our data, our text chunk has to first be broken down into smaller semantic chunks or clauses (also known as tokens). This step of breaking down our text chunk into smaller units is also known as tokenization. Conveniently, SpaCy provides a handy way of breaking down our text chunk into tokens.

```
tokens = [token.text for token in doc] # creates a list of tokens from our text input
```

### Step 2: Stop Word Removal & Punctuation Removal

In determining which sentences add the most value, we have to remove the words that add little to no value to the overall text chunk, in a process known as stop word removal. Common prepositions and articles (eg. a or the or at) are filtered out from the overall text chunk. Conveniently, the list of stop words can be imported from the SpaCy library:

```
from spacy.lang.en.stop_words import STOP_WORDS
```

The broken down tokens from Step 1 unfortunately still contains punctuation (eg. full stops or commas) that we have to remove. Thankfully, the English language has a small list of punctuation that we can easily import from the default python string library.

```
from string import punctuation
```

### Step 3: Frequency Calculation

After filtering our stop words and punctuation, the frequency of the remaining words are calculated and stored in a word_frequencies array.
```
if word.text not in word_frequencies.keys():
        word_frequencies[word.text] = 1
      else:
        word_frequencies[word.text] += 1
```

### Step 4: Frequency sentence analysis

The frequency of each word is then analysed. In this analysis step, we break down the input text into separate sentences, and determines which sentence contains the most significant words.

```
for sent in sentence_tokens:
  for word in sent:
    if word.text.lower() in word_frequencies.keys():
      if sent not in sentence_scores.keys():
        sentence_scores[sent] = word_frequencies[word.text.lower()]
      else:
        sentence_scores[sent] += word_frequencies[word.text.lower()]
```

### Step 5: Sentence filtering and summarised text generation

Each sentence from the original text input is tagged with a "significance" score to see which sentences are the most significant amongst the text input. The most significant sentences are extracted from the original text input and then parsed back together to form the final summarised text. Here, we import the heapq (heap queue algorithm) library to aid us in sorting out the most significant sentences. 

```
from heapq import nlargest
summary = nlargest(select_length, enumerate(sentence_scores.items()), key=lambda x: x[1][1])
summary = sorted(summary, key=lambda x: x[0])
```
