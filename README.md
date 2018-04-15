# RedditPoliticalAnalysis

Table of Contents
=================
  * [RedditPoliticalAnalysis](#redditpoliticalanalysis)
      * [Comment Generator](#comment-generator)
         * [Notable Results (LANGAUGE WARNING)](#notable-results-langauge-warning)

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
python generate_comments.py -f The_Donald -n 1000
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
