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

Torrance Yang - Wrote all of the code in this repository except the R code

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

//Trump talk is a series of words that Trump supporters like to use, i.e. MAGA, centipede, cuck, etc

```

It's not the prettiest way to manage this, but creating multiple tables is a hassle, and this will suffice for our purposes. 

`word_count`'s schema is much simpler. 

```
count: INTEGER,
word: STRING
```

## Data Analysis

We've linked a couple different analyses upon this data. The R analysis for this project is included within the r_data_analysis folder.

Something fun also did that we generated strictly from this cleaned data is a comment generator/simulator (described in the section below).

![Here are our findings.](https://i.imgur.com/Egsey7M.jpg)

In addition, based on our findings from R, we found a great deal of quantitative support behind what causes certain comments to be popular or polarizing. Listed below are some of our most notable findings. The accompanying graphs for these results can be found in the r_data_analysis folder. 

To begin our regression analysis, we created 15 indicators to determine if comments had specific words within them, specifically: Abortion, Emails, Russia, China, Mexico, Wall, Immigration, Guns, Healthcare, Taxes, Trump, Hillary, Obama, Bernie, and TrumpTalk. (Note: TrumpTalk is a collection of expletives commonly used by or in reference to Trump). 

For our first regression type, we did a very basic model, where we simply looked at the impact of all of these indicators on the variable of interest. We used this model for the following variables: comment_length, score, neu, neg, pos, and compound. Where neu, neg, and pos are all values ranging from 0 to 1 that represent the the neutrality, negativity, and positivity of a certain comment, respectively. Furthermore, compound was a value ranging from -1 to 1 that represented how negatively or positively impactful a comment was, namely, it was our closest rendition of polarity. 

For our second regression type, we had a more advanced, modified model that included interactions between indicators. Simply put, an interaction is interpreted as the product of a series of indicators. Since all indicators have a value of 0 or 1, an interaction effect can only be 1 if all its component indicators are 1. This allows us to determine the effect when multiple indicators are present in the same comment, hence the terminology, interaction effect. The interactions we used were all combinations of President name indicators, specifically: Trump * Hillary, Trump * Obama, Trump * Bernie, Hillary * Obama, Hillary * Bernie, Obama * Bernie, Trump * Obama * Hillary, Trump * Obama * Bernie, Trump * Hillary * Bernie, Obama  * Hillary * Bernie, and Trump * Obama * Hillary * Bernie. After including these additional indicators in our model, we looked at their effects on the same variables we tested in our first model. 

Finally, for our third regression type, we added another layer of complexity onto the previously mentioned interaction model. We decided to include a few more interactions to look for effects that may have stemmed from geopolitical relations or the Hillary email debacle. Namely, we decided to include an interaction between the Russia and China indicators and an interaction between the TrumpTalk, Emails, and Hillary indicators. Specifically, our new indicators were: Russia * China, TrumpTalk * Emails, TrumpTalk * Hillary, Emails * Hillary, TrumpTalk * Emails * Hillary. After adding these new interactions onto our previous model, we ran the regression on the same variables we have been working on since the beginning. 

Listed below are some of our more notable findings regarding popularity (scores variable) and polarity (compound variable). 

**Scores**

* In our first, basic model, the intercept was 9.41, suggesting that the baseline score was, on average, very high for the comments we selected. Simply looking at the coefficent from our regression, we see that some indicators had a significant impact on the score of a comment. For example, the "Obama" indicator had a coefficent of 3.72, meaning that any comment with mention of Obama, would on average be 3.72 points higher than a comment that excluded his name. Similarily, the "Trump" indicator had a coefficent of 4.17, suggesting comments with our current POTUS would increase the score of a comment by that much. This finding raises questions regarding what would happen if we saw both names included in the same comment, which, fortunately, is covered in the next bullet point. Finally, we also see some negative effects on scores within this regression. Namely, any mention of "Guns," which has a coefficent of -1.49, would drop the average score of a comment by almost 1.5 points, suggesting that comments mentioning guns were generally less popular within the Reddit community.  

* In our second model, the intercept was 9.37, suggesting that the baseline score was actually relatively high. Initally, we see the impact of a couple indicators. For example, the indicator of "Obama" has a coefficent of 4.00, which means that any mention of Obama would typically increase the score of a comment by that much. Similarily, the indicator of "Trump" had a coefficent of 4.557, which suggested that the mention of Trump would also increase the score of a comment. In addition, the interaction effect of Trump * Obama also had a positive coefficent of 2.69, which suggests that mention of both names, as opposed to one or the other, would on average, increase the score on the comment. On the flip side, the interaction effect of Trump * Hillary had a negative coefficent of -2.60, which suggests that mention of both names would decrease the score of a comment more than if either name was mentioned individually. These trends suggest that comments mention both Obama and Trump were, on average, far more favorable in popularity than if Trump and Hillary were mentioned together. However, a very interesting note was the interaction of Trump * Obama * Bernie * Hillary, which had an interaction effect of 5.03, which suggests that mentioning all four president names would greatly increase the score of a comment. One can specualte that this may be because a comment with such breadth may garner a lot more popularity than a comment with less diverse material, at least in terms of President name inclusion.

* Within the third model, the intercept was again 9.37. Right off the bat, we see that the most intense coefficent comes from the interaction effect of TrumpTalk * Emails, with a value of 8.08. This means that any mention of TrumpTalk and Emails would overall increase the score of the comment significantly than if the either of the two topics were mentioned without the other. Pure speculation suggests that comments using harsh expletives (TrumpTalk) about the email debacle (Emails) would garner more points (score) from likeminded members within the Reddit community. Another pretty powerful coefficent comes from the interaciton between Obama * Bernie * Trump, which had a value of -5.87. This suggests that any mention of all three topics would result in a lower score than if just a combination of the topics were mentioned alone. Similarily, the interaction between Bernie * Obama had a similar negative effect of -5.98 as a coefficent. This trend suggests that mentioning Obama and Bernie together would generally decrease the score of a comment, and mentioning Trump on top of that would further decrease a comment's score. 

**Compound**

* In our first, basic model, we see that the intercept is 0.0045, which suggests, that generally the comments were relatively neutral (close to 0) in this regression. The two most polarizing indicators we see are "Bernie" and "Guns", which have coefficent values of 0.17 and -0.298 respectively. For the "Bernie" indictor, the positive coefficent suggests that whenever Bernie is mentioned in a comment, the comment was generally viewed in a more positive light in terms of sentiment and polarity. On the flip side, whenever Guns are mentioned the polarity of the comment is negatively affected and drops greatly by almost 0.3. Since we are simply looking at indicators without interactions, we cannot deduce too much yet. Fortunately, the next couple sections cover the effects of interaction effects.   

* In our second model, we see that the intercept is 0.0059, which suggests that in general, all comments were relatively neutral (close to 0 in score). This provides us with a good baseline. Immediately, we see that the "Guns" indicator had a coefficent of -0.29, suggesting that any mention of guns would drastically cause the polarity of the comment to lean negatively. On the flip side, the interaction effect of Obama * Bernie had a coefficent value of 0.129, which suggests that any mention of the two topics together would further increase the polarity in a positive light than if the topics were mentioned without the other. 

* Within the third model, the intercept was 0.0057, which suggests that in general, all comments were relatively neutral (close to 0 in score), much like in the second model. However, again, the "Guns" indicator had a coefficent of -0.299, suggesting that any mention of guns would drastically cause the polarity of the comment to lean negatively. On the flip side, the "Bernie" indicator had a coefficent of 0.152, meaning any mention of Bernie would drive the polarity of the comment up positively. An interesting find stemmed from the TrumpTalk * Hillary interaction effect, which had a value of -0.114. This means that any mention of both Hillary and TrumpTalk would decrease the polarity of the comment more than if either was just mentioned without the other. We can interpret this interaction to say that when these two topics came were meshed together, the tone was generally more negative. Surprisingly, the interaction effect of TrumpTalk * Emails actually had a value of 0.107, which suggests that when both topics were in the same comment, the polarity was actually more positive. 


Again, these findings only demonstrate a snapshot of all the data that was generated from the regression models. To further examine the data and recreate our results, the accompanying r-script is included in r_data_analysis. 

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
