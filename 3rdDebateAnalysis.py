# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:29:19 2016

@author: Leon
"""
###########################  
# progress bar and percentage status
# time counter for the entire running time
import time
from datetime import datetime, timedelta
import sys

"""
for i in range(51):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-50s] %d%%" % ('='*i, 2*i))
    sys.stdout.flush()
    sleep(0.25)
"""
### set the progress bar
def update_progress(job_title, progress):
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()




# set a stopwacht ON
StartTime = datetime.now()
    
    
###########################   
# start first by uploading json and pandas using the commands below:
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob


###########################   
# read the data in into an array that we call tweets
# tweets_data_path1 ='C:\\Users\\Leon\\AppData\\Local\\Programs\\Python\\Python35-32\\3rdDebate.txt'

# N = 1
# tweets_file = open(tweets_data_path, "r")
# for i in range(0,N):
#   tweets_file.readline()


"""
with open(tweets_data_path) as tweets_file:
    head = [next(tweets_file) for x in range(N)]
"""


AllFiles = glob.glob('*.txt')
PATH = 'C:\\Users\\Leon\\AppData\\Local\\Programs\\Python\\Python35-32\\TweetData\\temp.txt'
tweets_data = []
with open(PATH,'w') as outfile:
    for file in AllFiles:
        with open(file, "r") as tweets_file:
            for line in tweets_file:
                try:
                    tweet = json.loads(line) 
                    tweets_data.append(tweet)
                except:
                    continue

"""
with open(tweets_data_path, "r") as tweets_file1:
    for line in tweets_file1:
        try:
            tweet = json.loads(line) 
            tweets_data.append(tweet)
        except:
            continue
"""
outfile.close() 
tweets_file.close()  
 
TweetsNumber = len(tweets_data)
print ("\n" + "Total Number of Tweets (imported lines) = " + str(TweetsNumber))
    
# get time and date
def get_date(tweet):
    try:
        t = datetime.strptime('2016 ' +' '.join(tweet['created_at'].split('+')[0].split(' ')[1:-1]),\
                '%Y %b %d %H:%M:%S')
    except:
        t = 'none'
        
    return t
 
### progress status for loading file
for i in range(100):
    time.sleep(0.1)
    update_progress("Loading Data Files", i/100.0)
update_progress("Loading Data Files", 1)

      
    
###########################    
# Build Datefrme from Tweets

text = []
lang = []
date = []
geo  = []
user_name = []

for tweet in tweets_data:
    try:
        text_ = tweet['text']
        lang_ = tweet['lang']
        date_ = get_date(tweet)
        geo_  = tweet['geo']
        user_name_ = tweet['user']["screen_name"]

        text.append(text_)
        lang.append(lang_)
        date.append(date_)
        geo.append(geo_)
        user_name.append(user_name_)
    except:
        pass
    
df = pd.DataFrame()
df['user_name'] = user_name
df['text'] = text
df['lang'] = lang
df['date'] = date
df['geo']  = geo

# to see the matirx, but don't do it
# df.head() or df
# to see the matrix, use .shape as shown below

# to see the matrice index, rows x columns
print("\n" + "Inital Dataframe (rows x columns):")
print(df.shape)


### progress status for building dataframe
for i in range(100):
    time.sleep(0.1)
    update_progress("Building Dataframe", i/100.0)
update_progress("Building Dataframe", 1)


###########################
# organizing the data

# create a .pkl dataframe file
df.to_pickle('final_non_processed.pkl')

# cleaning dupblications
no_duplicates = df.drop_duplicates(['text', 'user_name'])


"""
With double "user_name" in th drop_duplicates
Total Number of Tweets (imported lines) = 185525
Inital Dataframe (rows x columns):
(171257, 5)
The Dataframe (rows x columns) after removing duplications:
(171008, 5)
The Dataframe (rows x columns) after removing retweets:
(44820, 5)

After testing out with only one "user_name" filter, the result no difference.
"""

# to see the matrice after dropping duplicated entries
print("\n" + "The Dataframe (rows x columns) after removing duplications:")
print(no_duplicates.shape)

# reset index
reset_df = no_duplicates.reset_index(drop = True)

# Deleting Retweets
df = reset_df[['RT @' not in i for i in reset_df.text]]
# to see the matrice index, rows x columns
print("\n" + "The Dataframe (rows x columns) after removing retweets:")

print(df.shape[0])

# import the result into a final .pkl dataframe file
df.to_pickle('final_df.pkl')

###########################
#
   
import re
def word_in_text(words, text):
    words = [word.lower() for word in words]
    text = text.lower()
    
    for word in words:
        if re.search(word, text):
            return True
    return False


### progress status for organizing dataframe
for i in range(100):
    time.sleep(0.1)
    update_progress("Organizing Dataframe", i/100.0)
update_progress("Organizing Dataframe", 1)

    
############################## 
########## Analysis ##########  
##############################

# read from the final .pkl dataframe file and insert new 'df'
df = pd.read_pickle('final_df.pkl')
df['new_date'] = [datetime.strptime(date.strftime('%Y %b %d, %H:%M'), '%Y %b %d, %H:%M') - timedelta(hours = 4)\
                  for date in df.date]
df['debate'] = [1 if word_in_text(['#debate'], text) else 0 for text in df.text]
df['debate2016'] = [1 if word_in_text(['#debate2016'], text) else 0 for text in df.text]
df['hillaryclinton'] = [1 if word_in_text(['@hillaryclinton'], text) else 0 for text in df.text]
df['realdonaldtrump'] = [1 if word_in_text(['@realdonaldtrump'], text) else 0 for text in df.text]

# to optimize plot looking
rc={'xtick.labelsize': 30, 'ytick.labelsize': 30, 'axes.labelsize': 20, 'font.size': 20, 'legend.fontsize': 20, 'axes.titlesize': 35, "figure.figsize": [35, 14]}
sns.set(rc = rc)

# set plot specs, for total tweets collected over time
# matplotlib qt #plot in a separated window
fig1 = plt.figure()
df.groupby('new_date').count()['text'][:-1].plot()
plt.title('# of Tweets Collected During the Debate')
plt.xlabel('Time')
plt.ylabel('# of Tweets')


# set plot specs, for #debate
# matplotlib qt #plot in a separated window
fig2 = plt.figure()
df[df.debate == 1].groupby('new_date').count()['text'][:-1].plot()
plt.title('# of Tweets That Hashtagged #debate')
plt.xlabel('Time')
plt.ylabel('# of Tweets')

# to see total # of tweets mention #debate
print("\n" + "The total # of tweets with '#debate':")
print(df[df.debate == 1].shape[0])
# Mdebate = listdebate.shape
# print(Mdebate[0])


# set plot specs, for #debate2016
fig3 = plt.figure()
df[df.debate2016 == 1].groupby('new_date').count()['text'][:-1].plot()
plt.title('# of Tweets That Hashtagged #debate2016')
plt.xlabel('Time')
plt.ylabel('# of Tweets')

# to see total # of tweets mention #debate2016
print("\n" + "The total # of tweets with '#debate2016':")
print(df[df.debate2016 == 1].shape[0])

# set plot specs, for @hillary and @trump
fig4 = plt.figure()
df[df.hillaryclinton == 1].groupby('new_date').count()['text'][:-1].plot(label = '@hillaryclinton', color = 'blue')
df[df.realdonaldtrump == 1].groupby('new_date').count()['text'][:-1].plot(label = '@realdonaldtrump', color = 'red')
plt.legend(title = '@candidates')
plt.title('# of Tweets @ Each Candidate')
plt.xlabel('Time')
plt.ylabel('# of Tweets')

# to see total # of tweets mention #debate
print("\n" + "The total # of tweets with '@hillaryclinton':")
print(df[df.hillaryclinton == 1].shape[0])
print("\n" + "The total # of tweets with '@realdonaldtrump':")
print(df[df.realdonaldtrump == 1].shape[0])


### progress status for tweet # analysis 
for i in range(100):
    time.sleep(0.1)
    update_progress("Analyzing Tweet #", i/100.0)
update_progress("Analyzing Tweet #", 1)


###########################
########## Emoji ##########
###########################

# Scrapping the Emoji Chart

import requests
from bs4 import BeautifulSoup as bf
x = bf(requests.get('http://unicode.org/emoji/charts/full-emoji-list.html').text, 'lxml')
code = []
unicode_ = []
name = []
for i in x.find_all('tr'):
    try:
        code.append('U000'+i.find('td', class_ = 'code').a.text.split(' ')[0].split('U+')[1])
        unicode_.append(i.find('td', class_ = 'chars').text)
        name.append(i.find('td', class_ = 'name').text)
    except:
        pass
    
    
# The Emoji Dataframe    
emoji = pd.DataFrame({'code': code, 'names': name, 'unicode' : unicode_})

# Function to See if a String has an Emoji in It
def check_emoji_lst(string):
    for emoji_utf in emoji['unicode']:
        if emoji_utf in string:
            return True
    return False

# Function to see if USA Flag emoji is in the tweet
"""
USAcode = ['U+1F1FA', 'U+1F1F8']
def check_USA(string):
    for Unicode in USAcode:
        if Unicode in string:
            return True
    return False
"""
        
# The Emoji Dataframe 
# emoji.shape

# Make a Column if a tweet has an Emoji
# df['if_emoji'] = [1 if check_emoji_lst(i) == True else 0 for i in df.text]
df['if_emoji'] = [1 if check_emoji_lst(i) == True else 0 for i in df.text]

# Normalize the data so that it's easier to compare
# Or else total tweets would overshadow the ones with emojis
em = df[df.if_emoji == 1].groupby('new_date').count()
all_ = df.groupby('new_date').count()

em_max = em.text.max()
em['adjust_tweets'] = [i/float(em_max) for i in em.text]

all_max = all_.text.max()
all_['adjust_tweets'] = [i/float(all_max) for i in all_.text]

# set plot specs, for @hillary and @trump, ones with vs without emojis
fig5 = plt.figure()
em.adjust_tweets.plot(label = 'Collected Tweets with Emojis')
all_.adjust_tweets.plot(label = 'Collected Tweets')
plt.legend(title = '')
plt.title("Collected Tweets vs. Collected Tweets w/ Emojis" )
plt.xlabel('Time')
plt.ylabel('Normalized Percentage to the Peak')


# Dataframe with Only Emoji Tweets
emoji_only_df = df[[check_emoji_lst(i) for i in df.text]].reset_index(drop=True)

print (emoji_only_df.shape)


# Make Column that Lists the Unique Emojis in the Tweet
x = {}
master_lst = []
for index,text in enumerate(emoji_only_df.text):
    temp = []
    for i,uni in  enumerate(emoji['unicode']):
        if uni in text:
            temp.append(uni)
            
            try:
                x[index] += [uni]
            except:
                x[index] = [uni]
    master_lst.append(temp)
    
emoji_only_df['emojis'] = master_lst

# New Dataframe
print(emoji_only_df[['text', 'emojis', 'new_date']].head())


emoji_only_df.to_pickle('only_emoji_df.pkl')

trump_emoji = emoji_only_df[(emoji_only_df.hillaryclinton == 0 )&(emoji_only_df.realdonaldtrump == 1 )]
hillary_emoji = emoji_only_df[(emoji_only_df.hillaryclinton == 1 )&(emoji_only_df.realdonaldtrump == 0 )]

#### import counter 
from collections import Counter

# top emojis in tweets @trump
trump_flat = [val for sublist in trump_emoji.emojis for val in sublist]
top_emoji_trump = Counter(trump_flat).most_common()[:15]
trump_emoji_df = pd.DataFrame({'emoji': [i[0] for i in top_emoji_trump], '#':[i[1] for i in top_emoji_trump] })
print (trump_emoji_df)

fig6 = plt.figure()
sns.barplot(x = trump_emoji_df.emoji, y = trump_emoji_df['#'])
_ = plt.title("# Top 15 Emojis for Trump" )


# top emojis in tweets @clinton
hillary_flat = [val for sublist in hillary_emoji.emojis for val in sublist]
top_emoji_hillary = Counter(hillary_flat).most_common()[:15]
hillary_emoji_df = pd.DataFrame({'emoji': [i[0] for i in top_emoji_hillary], '#':[i[1] for i in top_emoji_hillary] })
print (hillary_emoji_df)

fi7 = plt.figure()
sns.barplot(x = hillary_emoji_df.emoji, y = hillary_emoji_df['#'])
_ = plt.title("# Top 15 Emojis for Hillary" )


### progress status for emoji analysis 
for i in range(100):
    time.sleep(0.1)
    update_progress("Analyzing Emoji #", i/100.0)
update_progress("Analyzing Emoji #", 1)



########
# Normalizing Data to Make Trend Comparisons Easier
"""
df['usa'] = [1 if check_USA(i) == True else 0 for i in df.text]
groupby_trump = df[(df.realdonaldtrump == 1) & (df.hillaryclinton == 0)].groupby('new_date').count()
groupby_trump['adjusted_tweets'] = [i/float(groupby_trump.text.max()) for i in groupby_trump.text]

groupby_hillary = df[(df.realdonaldtrump == 0) & (df.hillaryclinton == 1)].groupby('new_date').count()
groupby_hillary['adjusted_tweets'] = [i/float(groupby_hillary.text.max()) for i in groupby_hillary.text]

groupby_usa = emoji_only_df[df.usa == 1].groupby('new_date').count()
groupby_usa['adjusted_tweets'] = [i/float(groupby_usa.text.max()) for i in groupby_usa.text]


groupby_total_emojis = df[df.if_emoji == 1].groupby('new_date').count()
groupby_total_emojis['adjusted_tweets'] = [i/float(groupby_total_emojis.text.max()) for i in groupby_total_emojis.text]

# set plot specs for Mentions of USA Flag over the Total Tweets
fig8 = plt.figure()
groupby_total_emojis.adjusted_tweets.plot()
groupby_usa.adjusted_tweets.plot()
plt.legend(title = 'Candidates')
plt.title('Comparing Mentions of USA Flag over Total Tweets')
plt.xlabel('Time')
plt.ylabel('Normalized Percentage to the Peak')
"""


####################
##### Trends   #####
####################
df['hillary'] = [1 if ('hillary' in i) == True else 0 for i in  df.text] 
df['trump'] = [1 if ('trump' in i) == True else 0 for i in  df.text] 
df['hombre'] = [1 if ('hombre' in i) == True else 0 for i in  df.text] 
df['white'] = [1 if ('white' in i) == True else 0 for i in  df.text] 
df['puppet'] = [1 if ('puppet' in i) == True else 0 for i in  df.text] 
df['ripped'] = [1 if ('ripped' in i) == True else 0 for i in  df.text] 
df['chinese'] = [1 if ('chinese' in i) == True else 0 for i in  df.text] 
df['rigged'] = [1 if ('rigged' in i) == True else 0 for i in  df.text] 
df['nasty'] = [1 if ('nasty' in i) == True else 0 for i in  df.text] 
df['handshake'] = [1 if ('handshake' in i) == True else 0 for i in  df.text] 
df['sexual'] = [1 if ('sexual' in i) == True else 0 for i in  df.text] 
df['women'] = [1 if ('women' in i) == True else 0 for i in  df.text] 
df['vegas'] = [1 if ('vegas' in i) == True else 0 for i in  df.text] 
df['bigly'] = [1 if ('bigly' in i) == True else 0 for i in  df.text] 
df['sniff'] = [1 if ('sniff' in i) == True else 0 for i in  df.text] 
df['abortion'] = [1 if ('abortion' in i) == True else 0 for i in  df.text] 

fig9 = plt.figure()
df[df.hillary == 1].groupby('new_date').count()['text'].plot(label = 'hillary')
df[df.trump == 1].groupby('new_date').count()['text'].plot(label = 'trump')
df[df.hombre == 1].groupby('new_date').count()['text'].plot(label = 'hombre', color= 'black')
df[df.white == 1].groupby('new_date').count()['text'].plot(label = 'white', color = 'white')
df[df.puppet == 1].groupby('new_date').count()['text'].plot(label = 'puppet', color = 'grey')
df[df.rigged == 1].groupby('new_date').count()['text'].plot(label = 'rigged')
df[df.nasty == 1].groupby('new_date').count()['text'].plot(label = 'nasty', color = 'brown')
df[df.sexual == 1].groupby('new_date').count()['text'].plot(label = 'sexual', color = 'purple')
df[df.women == 1].groupby('new_date').count()['text'].plot(label = 'women')
df[df.bigly == 1].groupby('new_date').count()['text'].plot(label = 'bigly')
df[df.sniff == 1].groupby('new_date').count()['text'].plot(label = 'sniff')
df[df.abortion == 1].groupby('new_date').count()['text'].plot(label = 'abortion', color = 'pink')
plt.legend(title = "Keywords:")
plt.title('Trends with Keywords')
plt.xlabel('Time')
plt.ylabel('# of Tweets')




# set a stopwacht OFF
print (datetime.now() - StartTime)
# previous running time: 0:01:35.618282 (~ 1 min 35 sec)