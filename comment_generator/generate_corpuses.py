import argparse
from google.cloud import bigquery

parser = argparse.ArgumentParser(description='Generate the text corpuses to generate Markov chains from ')
parser.add_argument("--subreddit", "-s", 
					help="Input a subreddit you want to generate from (The_Donald, politics, SandersForPresident, hillaryclinton)",
					default="politics")

args = parser.parse_args()

client = bigquery.Client()
query_job = client.query("""
	SELECT body 
	FROM `cs216-199722.reddit_political_sentiments.merged_tables`
	WHERE subreddit = \'{}\'
	ORDER BY RAND()
	LIMIT 100000""".format(args.subreddit))

results = query_job.result()


with open("{}.txt".format(args.subreddit), "a+") as text_file:
	for row in results:
		text_file.write(row["body"].encode("utf-8") + "\n")		
    