from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
#Ended up not using this because of the API call limit

def process(x):
    #Analyze overall entity sentiment
    document = language.types.Document(
           content=x["body"],
           type='PLAIN_TEXT')
    print "processing"
    #Calculate overall sentiment of document 
    overall_sentiment = client.analyze_sentiment(
       document=document,
       encoding_type='UTF32')
    #print(overall_sentiment)
    return (overall_sentiment.document_sentiment.magnitude, overall_sentiment.document_sentiment.score, x["subreddit"])
    #return (1, 1, 'The_Donald')
client = language.LanguageServiceClient()
x = {'body': "That requires the Republican criminals in Congress to grow some balls. So that ain't gonna happen. Vote them out, investigate them, and if found guilty throw the book at every single one of", 'subreddit': "politics"}
print x
print(process(x))
