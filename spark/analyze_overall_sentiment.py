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

def process(x):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(x["body"])

    return (ss["neg"], ss["neu"], ss["pos"], ss["compound"], x["created_utc"], x["subreddit"])

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
    'mapred.bq.input.table.id': 'test_table',
    'mapred.bq.input.table.id': 'merged_tables'
}

# Load data in from BigQuery.
table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf)

#Map through data
overall_sentiments = (
    table_data
    .map(lambda record: process(json.loads(record[1]))))

#Act on data
pprint.pprint(overall_sentiments.take(10))


# Display 10 results from each for debugging
pprint.pprint(overall_sentiments.take(10))
# pprint.pprint(entity_sentiments.take(10))

# Stage data formatted as newline-delimited JSON in Cloud Storage.
output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output'.format(bucket)
output_files = output_directory + '/part-*' 

# Output Parameters.
output_dataset = 'reddit_political_sentiments'
output_table = 'sentiment_analysis'

sql_context = SQLContext(sc)
(overall_sentiments
.toDF(['neg', 'neu', 'pos', 'compound', 'created_utc', 'subreddit'])
.write.format('json').save(output_directory)) 

# Shell out to bq CLI to perform BigQuery import.
subprocess.check_call(
    'bq load --source_format NEWLINE_DELIMITED_JSON '
    '--replace '
    '--autodetect '
    '{dataset}.{table} {files}'.format(
        dataset=output_dataset, table=output_table, files=output_files
    ).split())

# Manually clean up the staging_directories, otherwise BigQuery
# files will remain indefinitely.
input_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
input_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(input_path, True)
output_path = sc._jvm.org.apache.hadoop.fs.Path(output_directory)
output_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(
    output_path, True)  