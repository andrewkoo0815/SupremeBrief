# Implementation of the Summarization Algorithms using the Python sumy Library
# Reference: https://github.com/miso-belica/sumy/blob/dev/README.rst

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# Import list of Summarizers
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import numpy as np

# Create the summarizer based on the selected algorithm
def create_summarizer(algorithm, stemmer):
    options = ["lsa", "edmundson", "lex", "luhn", "random", "text"]
    if (algorithm == options[0]):
        summarizer = LsaSummarizer(stemmer)
    elif (algorithm == options[1]):
        summarizer = EdmundsonSummarizer(stemmer)
    elif (algorithm == options[2]):
        summarizer = LexRankSummarizer(stemmer)
    elif (algorithm == options[3]):
        summarizer = LuhnSummarizer(stemmer)
    elif (algorithm == options[4]):
        summarizer = RandomSummarizer(stemmer)
    elif (algorithm == options[5]):
        summarizer = TextRankSummarizer(stemmer)
    return summarizer


def create_summary(algorithm, input_file, output_file = "sumy_summary.txt"):
    
    # Set language
    LANGUAGE = "english"
    # Get top N ranked sentences
    N = 5

    stemmer = Stemmer(LANGUAGE)
    parser = PlaintextParser.from_file(input_file, Tokenizer(LANGUAGE))
    summarizer = create_summarizer(algorithm, stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    all_sentences = []
    # Separate the paragraph into sentences
    for paragraph in parser.document.paragraphs:
        for sentence in paragraph.sentences:
            all_sentences.append(str(sentence))

    top_ranked_sentences = []
    # Use the summarizer to get the top ranked sentences
    for sentence in summarizer(parser.document, N):
        top_ranked_sentences.append(str(sentence))

    # Find the top ranked sentence
    for sentence in summarizer(parser.document, 1):
        top_sentence = str(sentence)
    
    # Find the position (between 0 to 4) of the top ranked sentence
    position = top_ranked_sentences.index(top_sentence)

    # Save the sentences into an output file
    # np.savetxt(output_file, top_ranked_sentences)
    record = open(output_file, "w")
    for i in range(len(top_ranked_sentences)):
        record.write(top_ranked_sentences[i]+ 'XXXXXX')
    record.write(str(position)+ 'XXXXXX')
    record.close()