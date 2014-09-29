# Implementation of the Summarization Algorithms using the Python sumy Library
# Reference: https://github.com/miso-belica/sumy/blob/dev/README.rst
# Same as sumy_learn except using "class" instead of "module"

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# List of Summarizers
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import numpy as np

class Summarizer: 
    def __init__(self, algorithm):
        self.__language = "english"
        self.__sumySummarizer = self.__create(algorithm)
        self.__summary = []
        self.__top = ""

    def createSummary(self, input_file):
        parser = PlaintextParser.from_file(
            input_file, Tokenizer(self.__language))
        self.__sumySummarizer.stop_words = get_stop_words(self.__language)

        all_sentences = []
        for paragraph in parser.document.paragraphs:
            for sentence in paragraph.sentences:
                all_sentences.append(str(sentence))

        N = 5
        top_ranked_sentences = []
        for sentence in self.__sumySummarizer(parser.document, N):
            top_ranked_sentences.append(str(sentence))
        self.__summary = top_ranked_sentences

        for sentence in self.__sumySummarizer(parser.document, 1):
            self.__top = str(sentence)

    def __create(self, algorithm):
        stemmer = Stemmer(self.__language)
        if (algorithm == "lsa"):
            return LsaSummarizer(stemmer)
        elif (algorithm == "edmundson"):
            summarizer = EdmundsonSummarizer(stemmer)
        elif (algorithm == "lex"):
            summarizer = LexRankSummarizer(stemmer)
        elif (algorithm == "luhn"):
            summarizer = LuhnSummarizer(stemmer)
        elif (algorithm == "random"):
            summarizer = RandomSummarizer(stemmer)
        elif (algorithm == "text"):
            summarizer = TextRankSummarizer(stemmer)
        else: 
            raise ValueError("Invalid input algorithm.")
        
    def printSummary(self):
        print (self.__summary)

    def printTop(self):
        print (self.__top)

    def outputToFile(self, output_file):
        try:
            topPosition = self.__summary.index(self.__top)
        except ValueError:
            print ("top sentence not in summary")

        # Save the sentences into an output file
        # np.savetxt(output_file, top_ranked_sentences)
        record = open(output_file, "w")
        for i in range(len(self.__summary)):
            record.write(self.__summary[i]+ 'XXXXXX')
        record.write(str(topPosition)+ 'XXXXXX')
        record.close()


