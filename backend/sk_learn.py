# Implementation of the various Natural Language Processing Algorithms using exisiting python libraries

import networkx as nx
import numpy as np
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

# Implementation of the textrank algorithm based on the tutorial provided by 
# http://joshbohde.com/blog/document-summarization

def textrank(document, output_file = "sk_summary.txt"):
    # Divide a text into a list of sentences using an unsupervised algorithm to build 
    # a model for abbreviation words, collocations, and words that start sentences.
    sentence_tokenizer = PunktSentenceTokenizer()
    # Separate the text into sentences based on the trained model
    sentences = sentence_tokenizer.tokenize(document)
    
    # Text feature extraction, allowing us to build SciPy matrices out of a collections of texts
    bow_matrix = CountVectorizer().fit_transform(sentences)
    # Normalize the graph based upon its tf-idf, which will dimish the effect of words common to each sentence.
    normalized = TfidfTransformer().fit_transform(bow_matrix)
    # Transform the text into a graph relating the sentences to each other
    similarity_graph = normalized * normalized.T
    # print similarity_graph
    
    # Use Pagerank to score the sentences in graph.
    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    
    # Sort the sentences into list of tuples(score, sentence)
    sorted_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

    # Get top N ranked sentences
    N = 5
    top_ranked_sentences = []
    for j in range(N):
        top_ranked_sentences.append(sorted_sentences[j][1])

    # Save the sentences into an output file
    # np.savetxt(output_file, top_ranked_sentences, delimiter = ",", fmt = "%s")
    position = 1
    record = open(output_file, "w")
    for i in range(len(top_ranked_sentences)):
        record.write(top_ranked_sentences[i]+ 'XXXXXX')
    record.write(str(position)+ 'XXXXXX')
    record.close()

