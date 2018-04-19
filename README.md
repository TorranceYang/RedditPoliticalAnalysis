# RedditPoliticalAnalysis

Table of Contents
=================

   * [RedditPoliticalAnalysis](#redditpoliticalanalysis)
      * [Problem Description](#problem-description)
      * [Team Members and Roles](#team-members-and-roles)
      * [Data Gathering and Cleaning](#data-gathering-and-cleaning)
         * [The Problem](#the-problem)
         * [The Solution](#the-solution)
      * [Data Processing](#data-processing)
         * [File Description](#file-description)
      * [Data Analysis](#data-analysis)
      * [Comment Generator](#comment-generator)
         * [Notable Results (LANGAUGE WARNING)](#notable-results-langauge-warning)
      * [Replicating Results](#replicating-results)



## Problem Description

The topics of political polarizaiton, party identity, and the power of online communities have become very hot with the last election. This project, done for CS216 - Everything Data, attempts to explore Reddit comments in different idealogical commmunities over time.

Reddit was our community of choice to examine. For those who don't understand what Reddit is, here is their [Frequently Asked Questions](https://www.reddit.com/wiki/faq) page. The basic premise of the website is that users can submit links which other users can like or dislike (called upvoting or downvoting) and can comment on. There are different groups, called subreddits, which serve as a hub to post and discuss a topic (like "politics").

The communities we decided to explore were The_Donald, SandersForPresident, hillaryclinton, worldnews, and politics. The general user for Reddit is a college-aged white American male ([source)](http://response.agency/blog/2014/02/reddit-demographics-and-user-surveys/) and the site generally tends to skew liberal (the popularity of SandersForPresident, hillaryclinton, and arguably politics shows this). However, different subreddits can be in the completely ideaological opposite. The most notorious is [The_Donald](https://en.wikipedia.org/wiki//r/The_Donald) which has attracted large amounts of negative attention. worldnews is believed to be more conservative as well (though definitely not to the same extreme). 

There is a huge BigQuery table which has all the comments posted on Reddit from 2005-2017 [link](https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments). While it would be very interesting to examine _all_ then comments from these communities, the size of the processing issue would be astronomical. Thus, we decided to examine comments from these subreddits from the Octobers of 2015, 2016, and 2017. 

The question we wanted to ask were: What does an average comment of this community look like? Have comments gotten more positive/negative/neutral over time? Have they gotten more polarizing?

## Team Members and Roles

Brian Jiang - Data Analysis

Tatiana Tian - Data Visualization + Presentation

Torrance Yang - Wrote all of the code in this repository

## Data Gathering and Cleaning

Luckily scraping the data has already been done for us, but it needed to be cleaned. This is done mostly in the SQL query to merge the comments from the three months we picked from the subreddits we chose. 

### The Problem

A lot of comments get removed or deleted so there are a lot of comments which show up as `<deleted>` or `<removed>.` Similarly, if a comment violates a subreddit rules, a bot may remove the message and leave a comment. These comments are useless for our examination, so they must be removed as well. 

### The Solution

There's a table within the public BigQuery table called `bots_201505` which contains the names of accounts which belong to bots, the most known of which is **AutoModerator**. The rest of the problems can be resolved uing plain SQL which can be found in `local/setup_new_table.py`. 

This file created a new table within our BigQuery console called `merged_tables` with around 9 million comments.

## Data Processing

Our idea was to do an sentiment and entity analysis on all these comments. Sentiment allows us to view how positive/negative/neutral/polarizing a comment is, and an entity analysis would let us see what subjects comments are talking about. 

So, how do we process 9 million comments in a reasonable amount of time? In trying to solve this, we had to overcome a number of barriers. We eventually found out the power of Google Cloud since we were already using BigQuery. There's a service called Dataproc which allows us to easily spin up a [Apache Spark](https://spark.apache.org/) cluster which can help us parallelize and process huge amounts of data efficiently. 

It was a pain to learn how to initialize the cluster, hook it up to BigQuery, save the results to Google Storage, and then insert it back into BigQuery as a new table, but all the code is in `spark`.

### File Description

`analyze.py` does most of the hard work. Here's an very simplified outline of what it does.

1. Connects to our BigQuery table
2. Processes a row for sentiment analysis
3. At the same time, looks for certain keywords that matches entities.
4. Returns a new row with processed data
5. Repeats until done
6. Starting back at the beginning, tokenizes and cleans the body of each comment
7. Inserts back into the RDD the values (word, 1)
8. Reduces the overall results by summing up the keys (effectively performing a word count)
9. Saves the RDD's of these two different calculations into JSON files on Google Storage

The output files are in a folder called `dataproc-[cluster-hash]-us/hadoop/tmp/bigquery/pyspark_output`. The results of the first RDD are stored in `.../analysis/` while the rest are stored in `.../wordcount/`.

Then, running the file `create_tables.py` will insert the json files one by one into two separate tables, called `comment_analysis` and `word_count`.

The schema for `comment_analysis` is

```
Sentiment Analysis Fields (FLOAT)
===============================
'neg', 'neu', 'pos', 'compound',

//What the above numbers mean: 
//https://stackoverflow.com/questions/40325980/how-is-the-vader-compound-polarity-score-calculated-in-python-nltk
//http://t-redactyl.io/blog/2017/04/using-vader-to-handle-sentiment-analysis-with-social-media-text.html

Comment Metadata (INTEGER, INTEGER, FLOAT, STRING, DATE, INTEGER)
=================================================================================== 
'score', 'gilded', 'controversiality', 'subreddit', 'created_utc', 'comment_length',

Does Comment Contain Topic Mention (BOOLEAN)
============================================
'Trump', 'Hillary', 'Bernie', 'Obama',
'Abortion', 'Immigration', 'Emails', 'Guns',
'Wall', 'Healthcare', 'Taxes', 
'Mexico', 'China', 'Russia', 
'TrumpTalk'

```

It's not the prettiest way to manage this, but creating multiple tables is a hassle, and this will suffice for our purposes. 

`word_count`'s schema is much simpler. 

```
count: INTEGER,
word: STRING
```

## Data Analysis

The analysis for this data is linked elsewhere as it is was done separate from this repository of code. 

However, something fun we generated strictly from this cleaned data is a comment generator/simulator (described below).

[Here are our findings.](https://imgur.com/Egsey7M)


## Comment Generator

The files for this are in `/comment_generator/`. 

With this gigantic corpus of data that we had in BigQuery, we wanted to run sum standard text generation to see what comments are like from different subreddits. For this we used [Markovify](https://github.com/jsvine/markovify). 

It'd be interesting to run this on the entire corpus of data we pulled, but with the amount of data we have and the cost to query the BigQuery database, we wrote a script `generate_corpuses.py` that instead pulls 100,000 random comments from a particular subreddit and saves it into a file. Then you can run the other file `generate_comments.py` with the file as an input to generate some comments.

**Using generate_corpuses.py**

```
usage: generate_corpuses.py [-h] [--subreddit SUBREDDIT]

Generate the text corpuses to generate Markov chains from

optional arguments:
  -h, --help            show this help message and exit
  --subreddit SUBREDDIT, -s SUBREDDIT
                        Input a subreddit you want to generate from
                        (The_Donald, politics, SandersForPresident,
                        hillaryclinton)

```

**Example**

```sh
python generate_corpuses.py -s The_Donald
```

**Using generate_comments.py**

```
usage: generate_comments.py [-h] --file FILE [--num NUM] [--length LENGTH]

Generate the comments

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Input the file you want to generate from
  --num NUM, -n NUM     Number of comments you want to generate
  --length LENGTH, -l LENGTH
                        Number of characters per comment to generate
```

**Example**

```sh
python generate_comments.py -f The_Donald.txt -n 1000
```

### Notable Results (LANGAUGE WARNING)

**/r/politics**


* Yes, because Hillary is a closet Nazi.
* Maybe his only job was to cure neurological illnesses as well cancel the election this year btw? tolerant dems must have been busy voting out every day Pardons are also known for leaving them scrambling to sew itself back together.
* You are a cancer.
* Trump's problem is that apology is not too fond of the article.
* The whole thing was rigged , that was said at one point or argument other than protecting innocent people to all the same attitude Oh, I know were pushed way left after 4 years ago?
* And Trump doesn't write any of their human rights is illegal.
* It's like watching an NFL players kneeling peacefully in protest after the non establishment president in our War for Independence, a Muslim ban or otherwise might be the bush part.


**/r/The_Donald** 


* It's a true sociopath, she is stiff, awkward, and unnatural, and has achieved new lows and attained the rank of King Lear or something, or get your reasoning perfectly and agree with!
* They have continued to say Melania was amazing HELL YEAH!
* Things that make women have regressed from being filled out at teachers.
* They may have come to Vegas caus it's easy to hit my sodium macros for the enemy, not unlike the NYT, and WaPo are alphabet agencies that now that they may turn the other 300 pages 
* THAT'S 81204 BRICKS HANDED OUT!** We are being handed out.**
* Sadly my family back out of a bitch of a judge; when these lefties are so fucking frustrating seeing people make sex tapes for their whims for Americans they take and defeat the political side.

**/r/SandersForPresident**

* No I would much rather let Trump win just because it's not like Bernie did, especially at the water here.
* Excellent history lesson after we defeat them is legitimate healthcare service.
* I'm not delusional for thinking of anarchists.
* The biggest obstacle at this point, but I think it has a far right and he will be tolerated.
* I'm sorry, but O'Malley and Clinton in this conversation from your phone, if you own but don't complain that government intervention in the bag You're saying that it should be discussed.
* Agreed, their stance has opportunity costs, they'd start out strong before faltering immediately after for the lower and working people.

**/r/hillaryclinton**

* Just a reminder, Trump Foundation even though he may encourage people to claim she lacked accomplishments over 30 years now, the assumption it'll be worth seeing if there is a paid reporter for his own name on another channel.
* Trump wants to troll instead of vice versa?
* I've listened to the 538 article about how Pence did nothing wrong with this issue, in spite of all stripes end up primarily running this sub can post images.
* Russia is trying to put her over the course of action to require that any of the popular vote.
* I think most people don't even know who is scared, that doesn't happen.
* KellyAnne is pretty much my entire life and his father did to religion.

**/r/worldnews**
* So find an exxcavator and operator of an idea of China to a flag and when I saw a Brazilian official, was promoted to corporal, and retires as a tax payer Hey but at least on the solid responses on your own barrel or something.
* If there is nothing compared to the New Testament and the crime against Israel in the other 99% of all people.
* Lord, what has been removed because you aren't capable of launching nukes, they may see humans stop fishing due to the Luna 27 mission.
* I hope you are supposedly being killed?
* Or are we only know about the amazing achievement of the predatory paedophile problem and murder problem.
* People know right It's Obama.

## Replicating Results

Due to the nature of the Google Cloud Platform, I'm not sure any of this would work. You'd need to have your own BigQuery datasets for a lot of the Spark jobs to run, and there's a lot of authentication things Google Cloud needs to run that I've already forgotten were. However, I've included a requirements.txt file that should roughly provide the dependencies of the code and some sample command line arguments that run the BigQuery and Spark Jobs.

**Installing local requirements**
```python
pip install -r requirements.txt
```

**Setup Google Cloud**

`gcloud init`

**Setting up Dataproc cluster**

You'll need to upload the `spark/install.sh` file to Google Storage, and then select it as the initialization script when spinning up the cluster

**Sending jobs to cluster**

`gcloud dataproc jobs submit pyspark [file-name] --cluster [cluster-name]
`
