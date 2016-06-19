#!/usr/bin/python3 -u

import os
import time
import datetime
from twitter import *
from pit import Pit

config = Pit.get('your pit label')

# sampl pit default.yaml
#
#your pit label:
#    ConsumerKey: your consumer key of twitter app
#   ConsumerSecret: your consumer secret of twitter app
#   AccessToken: your Access token of twitter app
#   AccessTokenSecret: access token secret of twitter app
#


cursor = -1
num = 1
sleeptime = 5

friendsList =[]
rmlist = []

now = datetime.datetime.today()

# last tweet day
# This app remove friend who didn't tweet after the limit day.
limitday = datetime.timedelta(days=90)

borderday = now - limitday


twitter = Twitter(auth=OAuth(config['AccessToken'], config['AccessTokenSecret'], config['ConsumerKey'],config['ConsumerSecret']))


# Now work with Twitter
#twitter.statuses.update(status='test2')


print("--- step1 get my friends ids -------")


while cursor != 0:
    res=twitter.friends.ids(cursor=cursor)

    cursor = res['next_cursor'] 
#    print(cursor)

    ids=res['ids']
    for id in ids:
        print(id)


print("------------------------------------")
print("total ids:",len(res['ids']))
print()

print("--- step2 check last tweet date ----")


for id in ids:
    st =''
    #print("%4d %15s" % (num,id),end='')
    res=twitter.statuses.user_timeline(_id=id)
    #print(id," ",res[1])
    if len(res) != 0:
        created_at = res[0]['created_at']
        name = res[1]['user']['name']
        st = datetime.datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
        friendsList.append({'id':id,'tweet_at':st,'name':name})
        
        print("%4d %15s %s %s" % (num,id,st,name))
    else :
        
        print('\n')

 
    num+= 1
    time.sleep(sleeptime)
  

print("--- step3 fetch no tweet friends ---")
num = 1

for item in friendsList:
    print(item['tweet_at'])
    st = datetime.datetime.strptime(str(item['tweet_at']),'%Y-%m-%d %H:%M:%S')
    #print(st)
    if st < borderday:
        print("%4d %15s %s %s" % (num,item['id'],item['tweet_at'],item['name']))
        rmlist.append({'id':item['id'],'name':item['name']}) 

    num+=1


print("--- step4 remove  friends ----------")

num = 1

for item in rmlist:
    res=twitter.friendships.destroy(_id=item['id'])

    if len(res) != 0:
        if res['id_str']:
            if str(item['id']) == res['id_str']:
                print("%4d success:%15s %s" % (num,item['id'],item['name']))
            else:
                print("%4d failer :%15s %s" % (num,item['id'],item['name']))
        else:
            print("%4d failer :%15s %s" % (num,item['id'],item['name']))
    num+=1

print("done")

    
