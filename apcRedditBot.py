import praw
import json
import datetime

#get events from event library json file
with open('txtLibrary.txt', encoding="utf8") as f:
  allEvents = json.load(f)

#get "today string" to find today's events in event database:
dt = datetime.datetime.today()
todayString = str(dt.month) + '-' + str(dt.day)
#todayEvents in the form of eventCategory list of objects with category, title, date, description, imgSrc, link (more info), and infoSrc
todayEvents = allEvents[todayString]

reddit = praw.Reddit(client_id="dati0RLqNGHjWw",
                     client_secret="SECRET",
                     user_agent="script:com.apc.apcEvents:v1.0.0 (by /u/A_Peoples_Calendar)",
                     username="A_Peoples_Calendar",
                     password="PASSWORD")

#the following works:
#title = "PRAW test"
#body_ = 'this is a test of praw and the reddit api'
#reddit.subreddit("A_Peoples_Calendar").submit(title, selftext=body_)

#test subreddit flair:
for flair in reddit.subreddit("A_Peoples_Calendar").flair():
    print('testing flair')
    print(flair)

def stripParen(text):
    index = text.find('(')
    return text[:index - 1]

eventList = []

flairDict = {'Revolution': 'afabf016-f70a-11ea-8a09-0e51d2cf5475', 'Rebellion': 'b9de8cce-f70a-11ea-9188-0ea7e1e72d51', 'Labor': 'c256167e-f70a-11ea-9761-0ef06d289e7b', 'Birthdays': 'df35bb32-f70a-11ea-a3a1-0e73aa9b5439', 'Assassinations': 'ce807372-f70a-11ea-a9fb-0ea312e4c14b', 'Other': 'd63e94d6-f70a-11ea-8c09-0e74e1100df7',}

def submitEvents():
    for category in todayEvents:
        #print(todayEvents[category][0]['imgSrc'])
        if not todayEvents[category][0]['description']:
            #we have an empty event category for today's events - don't do anything
            print('no events for category: ' + category)
            pass
        else:
            print('submitting events for ' + todayString + ' ' + category)
            for event_ in todayEvents[category]:
                #do the submit stuff for every event in the category
                title = stripParen(event_['title']) + ', ' + event_['date']
                image = event_['imgSrc']
                reddit.subreddit("A_Peoples_Calendar").submit_image(title, image, flair_id=flairDict[category])
                #add a comment on the post with the detailed event description (race condition?)
                #submitComment(event_)
                #append event_ to list of events, used for making comments
                eventList.append(event_)

def submitComment(event_):
    #get the matching submission
    #TO DO: rather than searching among last twenty posts, can probably just find it by passing thread ID to the eventList, i.e. (eventObject, threadID)
    #without doing that, if you have more than 20 submissions on a single day, comment will miss it
    for submission in reddit.subreddit("A_Peoples_Calendar").new(limit=20):
        if submission.title == stripParen(event_['title']) + ', ' + event_['date']:
            print('adding comment to post with title: ' + submission.title)
            correctPost = reddit.submission(id=submission.id)
            #create the on this day link within the event description:
            otdLink = "https://www.apeoplescalendar.org/day/%s" % (todayString)
            newDescription = event_['description']
            otdIndex = newDescription.find("On this day")
            if otdIndex != -1:
                newDescription = newDescription[:otdIndex] + '[On this day](' + otdLink + ')' + newDescription[otdIndex + 11:]
            else:
                otdIndex = newDescription.find("on this day")
                if otdIndex != -1:
                    newDescription = newDescription[:otdIndex] + '[on this day](' + otdLink + ')' + newDescription[otdIndex + 11:]

            #format the comment using data from the event_ object
            body = '''**%s**\n\n%s\n\n[Primary Source](%s)\n\n[More Info](%s)''' % (event_['title'], newDescription, event_['infoSrc'], event_['link'])
            #make the post reply
            correctPost.reply(body)

submitEvents()
for event_ in eventList:
    submitComment(event_)
