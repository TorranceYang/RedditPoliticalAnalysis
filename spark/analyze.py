 #!/usr/bin/python
"""Base files taken from BigQuery I/O PySpark example."""
from __future__ import absolute_import
import json
import pprint
import subprocess
import pyspark
from pyspark.sql import SQLContext

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#For entity analysis
primary_dict = {
    #People
    "Trump": ["donald", "trump"],
    "Hillary": ["hillary", "clinton", "rodham"],
    "Bernie": ["bernie", "sanders"],
    "Obama": ["barack", "obama"],
    #Policy
    "Abortion": ["abortion", "pro-life", "pro-choice"],
    "Immigration": ["immigrant", "immigrants", "immigration"],
    "Emails": ["emails", "email"],
    "Guns": ["guns", "gun", "weapon", "bullets", "bullet", "nra", "shooting"],
    "Wall": ["walls", "wall"],
    "Healthcare": ["healthcare", "obamacare", "premiums", "aca", "medicare", "medicaid"],
    "Taxes": ["tax", "taxes"],
    #Other Countries
    "Mexico": ["mexico", "mexican"],
    "China": ["china", "chinese"],
    "Russia": ["russia", "russian"],
    #Slang (https://www.attn.com/stories/6789/trump-supporters-language-reddit)
    "TrumpTalk": ["maga", "centipede", "centipedes", "cuck", "cucks", "cuckold", "cuckolds"]
 }

#Inverts a dictionary (https://stackoverflow.com/questions/34780253/efficiently-string-searching-in-python)
def invert_dict(src):
    dst = {}
    for key, values in src.items():
        for value in values:
            dst[value] = key
    return dst

inverted_dict = invert_dict(primary_dict)

stop_words = set(stopwords.words('english'))
inverted_keys = set(inverted_dict.keys())

def process(x):
    #Tokenizes and cleans strings 
    #Converts to lowercase words
    #Looks for our predetermined entities using set logic
    #Returns dictionary where key = entity, value = was found in body text
    def rough_entity_extraction(body):
        word_tokens = word_tokenize(body)
        filtered_words = {w.lower() for w in word_tokens if not w in stop_words and w.isalpha()}
        intersection = inverted_keys & filtered_words

        result_dict = {key: False for key in primary_dict.keys()}

        for r in intersection:
            result_dict[inverted_dict[r]] = True

        return result_dict

    #Analyzes comment sentiment    
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(x["body"])

    entities = rough_entity_extraction(x["body"])

    return (ss["neg"], ss["neu"], ss["pos"], ss["compound"], 
            x["score"], x["gilded"], x["controversiality"], x["subreddit"], x["created_utc"], len(x["body"]),
            entities["Trump"], entities["Hillary"], entities["Bernie"], entities["Obama"],
            entities["Abortion"], entities["Immigration"], entities["Emails"], entities["Guns"],
            entities["Wall"], entities["Healthcare"], entities["Taxes"],
            entities["Mexico"], entities["China"], entities["Russia"], 
            entities["TrumpTalk"])

#Cleans, tokenizes, and lowers strings similar to above 
#but is not a set to preserve accurate word count
def remove_stops(body):
    return [w.lower() for w in body if not w in stop_words and w.isalpha()]

#Create a Spark context
sc = pyspark.SparkContext()

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the InputFormat. This assumes the Cloud Storage connector for
# Hadoop is configured.
bucket = sc._jsc.hadoopConfiguration().get('fs.gs.system.bucket')
project = sc._jsc.hadoopConfiguration().get('fs.gs.project.id')

input_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_input'.format(bucket)

conf = {
    # Input Parameters.
    'mapred.bq.project.id': project,
    'mapred.bq.gcs.bucket': bucket,
    'mapred.bq.temp.gcs.path': input_directory,
    'mapred.bq.input.project.id': 'cs216-199722',
    'mapred.bq.input.dataset.id': 'reddit_political_sentiments',
    #'mapred.bq.input.table.id': 'test_data',
    'mapred.bq.input.table.id': 'merged_tables'
}

# Load data in from BigQuery.
table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf)

#Run full analysis
overall_analysis = table_data.map(lambda record: process(json.loads(record[1])))

#Perform word count
word_counts = table_data.flatMap(lambda line: remove_stops(word_tokenize(json.loads(line[1])["body"]))) \
                .map(lambda word: (word, 1)) \
                .reduceByKey(lambda a, b: a + b)

#Act on data and display 10 results from each for debugging
pprint.pprint(overall_analysis.take(10))
pprint.pprint(word_counts.take(10))

# Stage data formatted as newline-delimited JSON in Cloud Storage.
analysis_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/analysis'.format(bucket)
count_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/wordcount'.format(bucket)

sql_context = SQLContext(sc)

#Convert to DataFrame, same to Google Storages as a Json
(overall_analysis
.toDF(['neg', 'neu', 'pos', 'compound', 
    'score', 'gilded', 'controversiality', 'subreddit', 'created_utc', 'comment_length',
    'Trump', 'Hillary', 'Bernie', 'Obama',
    'Abortion', 'Immigration', 'Emails', 'Guns',
    'Wall', 'Healthcare', 'Taxes', 
    'Mexico', 'China', 'Russia', 
    'TrumpTalk'])
.write.format('json').save(analysis_output_directory))

(word_counts    
.toDF(['word', 'count'])
.write.format('json').save(count_output_directory))
