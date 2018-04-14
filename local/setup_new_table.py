#!/usr/bin/python
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from google.cloud.bigquery import table


# Create a new Google BigQuery client using Google Cloud Platform project
# defaults.
bigquery_client = bigquery.Client()

# The name for the new dataset.
dataset_id = 'reddit_political_sentiments'

# Prepare a reference to the new dataset.
dataset_ref = bigquery_client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)

# Create the new BigQuery dataset.
#dataset = bigquery_client.create_dataset(dataset)

# In the new BigQuery dataset, create a new table.
table_ref = dataset.table('merged_tables_timestamped')
# The table needs a schema before it can be created and accept data.
# Create an ordered list of the columns using SchemaField objects.
SCHEMA = []
SCHEMA.append(SchemaField('body', 'string'))
SCHEMA.append(SchemaField('author', 'string'))
SCHEMA.append(SchemaField('score', 'integer'))
SCHEMA.append(SchemaField('gilded', 'integer'))
SCHEMA.append(SchemaField('controversiality', 'integer'))
SCHEMA.append(SchemaField('subreddit', 'string'))
SCHEMA.append(SchemaField('created_utc', 'string'))

# Assign the schema to the table and create the table in BigQuery.
table = bigquery.Table(table_ref, schema=SCHEMA)
table = bigquery_client.create_table(table)

# Set up a query in Standard SQL.
# The query selects the fields of interest.
QUERY = """
SELECT body, author, score, gilded, controversiality, subreddit, created_utc
FROM `fh-bigquery.reddit_comments.2015_10`
WHERE subreddit = 'The_Donald' OR subreddit = 'politics' OR subreddit = 'SandersForPresident' OR subreddit = 'hillaryclinton' OR subreddit = 'worldnews'
AND body IS NOT NULL
AND author IS NOT NULL
AND score IS NOT NULL
AND gilded IS NOT NULL
AND controversiality IS NOT NULL
AND subreddit IS NOT NULL
UNION ALL SELECT 
body, author, score, gilded, controversiality, subreddit, created_utc
FROM `fh-bigquery.reddit_comments.2016_10`
WHERE subreddit = 'The_Donald' OR subreddit = 'politics' OR subreddit = 'SandersForPresident' OR subreddit = 'hillaryclinton' OR subreddit = 'worldnews'
AND body IS NOT NULL
AND author IS NOT NULL
AND score IS NOT NULL
AND gilded IS NOT NULL
AND controversiality IS NOT NULL
AND subreddit IS NOT NULL
UNION ALL SELECT 
body, author, score, gilded, controversiality, subreddit, created_utc
FROM `fh-bigquery.reddit_comments.2017_10`
WHERE subreddit = 'The_Donald' OR subreddit = 'politics' OR subreddit = 'SandersForPresident' OR subreddit = 'hillaryclinton' OR subreddit = 'worldnews'
AND body IS NOT NULL
AND author IS NOT NULL
AND score IS NOT NULL
AND gilded IS NOT NULL
AND controversiality IS NOT NULL
AND subreddit IS NOT NULL
"""
# Configure the query job.
job_config = bigquery.QueryJobConfig()
# Set the output table to the table created above.
dest_dataset_ref = bigquery_client.dataset('reddit_political_sentiments')
dest_table_ref = dest_dataset_ref.table('merged_tables')
job_config.destination = dest_table_ref
# Allow the results table to be overwritten.
job_config.write_disposition = 'WRITE_TRUNCATE'
# Use Standard SQL.
job_config.use_legacy_sql = False
# Run the query.
query_job = bigquery_client.query(QUERY, job_config=job_config)