# Bidirectional Job Matching
Version 0.5

## Contents
* 1.0	Direction
* 2.0	Semantic Comparisons
* 2.1	Job Descriptions to Job Descriptions
* 2.2	Job Descriptions to Resumes
* 3.0	Methodology
* 3.1	Mechanics
* 3.2	Data Science
* 4.0	Next Steps


## 1.0 Direction

The inspiration of this exercise is a paper that is a part of a PhD thesis: Bidirectional Job Matching through Unsupervised Feature Learning.
 
The goal is to implement the ideas from this paper in part, adding to the project piece by piece.
 
The most effective and obvious task involves taking the text from large number of resumes and comparing them one by one to the text from a large number of job descriptions. The idea is that the best match for an individual will be the job description with the most similar textual content.
 
The job descriptions are collected from a particular search in Indeed, downloaded using an automated technique in Python.

Initially the resumes are gathered from a Kaggle competition for proof of concept. Once the direction has been shown to be valid, it will be a platform that can used to collect resumes and use them as a pool to have matched to a group of job descriptions.


## 2.0 Semantic Comparisons

### 2.1 Job Descriptions to Job Descriptions

Initially, the resume import was not yet complete, but 6,786 unique job descriptions have been loaded into the Python environment. We created a similarity generator to begin with, comparing JDs to JDs. What this is, in effect, is the basis of a Recommendation Engine, that recommends based solely on similarity of job description text.
 
Initially, we show a visual comparison of JDs by a semantic analysis of the text section of the resume.
 
It is not a fast process, about ten seconds per comparison on my personal laptop. I initially ran it on only 10 job descriptions, and the comparison can be represented in a heatmap as thus:

![JD2JD Small Heatmap](https://github.com/deepersideoflearning/bidirectional-job-search/tree/master/images/JD2JD_small_Heatmap.jpg)
 
 
On this heatmap, the darker coordinates identify higher similarity. Job descriptions 1 and 2 are similar, as well as 8 and 9. As well, every job description is similar to itself. Verifying that these similarities are actually accurate is quite easy, taking a look directly at the job descriptions compared. See attached for the associated Job Descriptions.

Next, we ran it on 100 job descriptions, comparing them to each other, making 100x100 (10,000) comparisons. This took 10 hours to run on my laptop, and produced the following heatmaps on two sets of data, the first generating the reflexive section as well:
 
![JD2JD Heatmap 1](https://github.com/deepersideoflearning/bidirectional-job-search/tree/master/images/JD2JD_Heatmap.jpg)
![JD2JD Heatmap 2](https://github.com/deepersideoflearning/bidirectional-job-search/tree/master/images/JD2JD_Heatmap2.jpg)
  
 
## 2.1 Resumes to Job Descriptions

Lastly, after pulling a set of annotated 219 unique resumes found on Kaggle, the raw content was separated and then compared to the job descriptions using the same distance measurement. The resulting heat map on 100 of the 219 is as follows:

![JD2Res heatmap](https://github.com/deepersideoflearning/bidirectional-job-search/tree/master/images/JD2Res_heatmap.jpg)

 
The vertical striped shape indicates that some of the resumes were very different from all of the job descriptions collected, where some resumes matched more closely across the board. The horizontal bright stripes would indicate job descriptions that are not closely matching any or many of the resumes.

## 3.0 Methodology

### 3.1 Mechanics

* Python 3.7 on HP Pavilion Windows 10
* Django API attached to sqlite3 database
* HTML front end
* Elastic Beanstalk deployment from AWS


## 3.2 Data Science

This methodology of semantic similarity employs the latest in deep learning research from Stanford University, using GloVe embeddings to convert the descriptions to numerical representations. GloVe embeddings were developed by a Stanford NLP team, applying word-word co-occurrence probability to build the embedding. In other word, if two words are co-exist many time, both words may have similar meaning so the matrices will be closer.
 
Here we used a 50 dimension vector to represent each word in a job description, and then a total distance measure between the vector sets. The usual methods for distance employ Euclidian (spacial) Distance, or alternatively Cosine Distance. A more accurate methodology for distance is Word Mover’s Distance. This method assumes similar words should have similar vectors.
 
## 4.0 Next Steps

Much work is to be done (not in this order) including:
* Review results, noting and counting all similar job descriptions for verification.
* Sorting on distance combinations of similar job descriptions, resulting in a recommendation engine.
* Further cleaning of textual data, removing duplicates and reducing corpus size by simplifying the word list with different standard and specific preprocessing methods.
* Adding statistical analysis and analytics of datasets.
* Trying different word embeddings for speed and accuracy of measurement.
* Trying different distance measures for speed and accuracy.
* Pulling more and varied job descriptions.
* Pull job descriptions from other repositories (besides Indeed).
* Gathering resumes for matching.
* Adding other components described in source paper (Bidirectional Job Matching through Unsupervised Feature Learning)
* Moving to AWS and creating API for deployment via Elastic Beanstalk.
* Deploy simple Java Script front end to extend the user base.
* Add continual building of job descriptions database to productionalize pipeline.

## 5.0 References

* [Stanford GloVe Embeddings] (https://nlp.stanford.edu/projects/glove/)
* [Bidirectional Job Matching through Unsupervised Feature Learning] (https://pdfs.semanticscholar.org/31b7/2f37331323d5562815b99d0be38ef6e17dc3.pdf)

