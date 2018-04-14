 #!/usr/bin/python
"""Sometimes analyze.py returns an empty json which will cause an error if you try to load it into BigQuery.
Thus, we need to manually delete the empty files and then run this file"""

from __future__ import absolute_import
import json
import pprint
import subprocess
import pyspark
from pyspark.sql import SQLContext

sc = pyspark.SparkContext()

bucket = sc._jsc.hadoopConfiguration().get('fs.gs.system.bucket')
project = sc._jsc.hadoopConfiguration().get('fs.gs.project.id')

input_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_input'.format(bucket)

# Stage data formatted as newline-delimited JSON in Cloud Storage.
sentiment_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/sentiment'.format(bucket)
count_output_directory = 'gs://{}/hadoop/tmp/bigquery/pyspark_output/wordcount'.format(bucket)

# Output Parameters.
output_dataset = 'reddit_political_sentiments'

sentiment_output_table = 'sentiment_analysis_extra'
count_output_table = 'word_count'

# Stage data formatted as newline-delimited JSON in Cloud Storage.
# Shell out to bq CLI to perform BigQuery import.
output_files = sentiment_output_directory + '/part-*' 
subprocess.check_call(
    'bq load --source_format NEWLINE_DELIMITED_JSON '
    '--replace '
    '--autodetect '
    '{dataset}.{table} {files}'.format(
        dataset=output_dataset, table=sentiment_output_table, files=output_files
    ).split())

output_files = count_output_directory + '/part-*' 
subprocess.check_call(
    'bq load --source_format NEWLINE_DELIMITED_JSON '
    '--replace '
    '--autodetect '
    '{dataset}.{table} {files}'.format(
        dataset=output_dataset, table=count_output_table, files=output_files
    ).split())

# Manually clean up the staging_directories, otherwise BigQuery
# files will remain indefinitely.
input_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
input_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(input_path, True)
output_path = sc._jvm.org.apache.hadoop.fs.Path(sentiment_output_directory)
output_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(
    output_path, True)  
output_path = sc._jvm.org.apache.hadoop.fs.Path(count_output_directory)
output_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(
    output_path, True)  