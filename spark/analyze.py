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

def process(x):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(x["body"])

    return (ss["neg"], ss["neu"], ss["pos"], ss["compound"], x["score"], x["gilded"], x["controversiality"], x["subreddit"], x["created_utc"], len(x["body"]))

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
    #'mapred.bq.input.table.id': 'test_table',
    'mapred.bq.input.table.id': 'merged_tables'
}

# Load data in from BigQuery.
table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf)

#Map through data
overall_sentiments = table_data.map(lambda record: process(json.loads(record[1])))

#Perform word count
word_counts = table_data.flatMap(lambda line: word_tokenize(json.loads(line[1])["body"])) \
                .map(lambda word: (word, 1)) \
                .reduceByKey(lambda a, b: a + b)

#Act on data and display 10 results from each for debugging
pprint.pprint(overall_sentiments.take(10))
pprint.pprint(word_counts.take(10))

# Stage data formatted as newline-delimited JSON in Cloud Storage.
sentiment_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/sentiment'.format(bucket)
count_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/wordcount'.format(bucket)

sql_context = SQLContext(sc)

(overall_sentiments
.toDF(['neg', 'neu', 'pos', 'compound', 'score', 'gilded', 'controversiality', 'subreddit', 'created_utc', 'comment_length'])
.write.format('json').save(sentiment_output_directory))

(word_counts    
.toDF(['word', 'count'])
.write.format('json').save(count_output_directory))
