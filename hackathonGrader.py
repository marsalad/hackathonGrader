import requests
from bs4 import BeautifulSoup
import csv

user_pre = 'https://devpost.com/'          # url prefix for devpost username
proj_pre = 'https://devpost.com/software/' # url prefix for devpost project id
in_file  = 'apps.csv'                      # csv file of applicant devpost usernames
out_file = 'scraped.csv'                   # csv file to write scraped data to

# returns user data as dictionary object:
#   'proj_num' is the number of projects posted
#   'hack_num' is the number of hackathons attended
#   'projects' is a list of devpost project ids
def user_data(user):
    soup_page = BeautifulSoup(requests.get(user_pre + user).content, 'html.parser')
    totals = soup_page.find_all('span', attrs={'class' : 'totals'})
    projects = soup_page.find_all('', attrs={'class' : 'gallery-item'})
    return {
        'proj_num' : int(totals[0].text),
        'hack_num' : int(totals[1].text),
        'projects' : [project['data-software-id'] for project in projects]
    }

# returns project data as dictionary object:
#   'event' is the name of the event submitted to
#   'event_url' is the url of the event submitted to
#   'awards' is a list of awards won
#   'like' is the number of likes the project recieved
# error if the project has not been submitted to a hackathon
def proj_data(proj_id):
    soup_page = BeautifulSoup(requests.get(proj_pre + proj_id).content, 'html.parser')
    data = soup_page.find('div', attrs={'class' : 'software-list-content'})
    return {
        'event'     : data.find('a').text,
        'event_url' : data.find('a')['href'],
        'awards'    : [proj.contents[2].strip() for proj in data.find_all('li')],
        'like'      : int(soup_page.find('span', attrs={'class' : 'side-count'}).text)
    }

# returns number of participants at an event given the devpost url
def event_partic(event_url):
    soup_page = BeautifulSoup(requests.get(event_url + "participants").content, 'html.parser')
    event_data = soup_page.find('div', attrs={'id' : 'participants'})
    return int(event_data.findChildren()[0].text.split()[0])

# returns number of submissions at an event given the devpost url
def event_submits(event_url):
    soup_page = BeautifulSoup(requests.get(event_url + "submissions").content, 'html.parser')
    event_data = soup_page.find('span', attrs={'class' : 'items_info'})
    return int(event_data.findChildren()[0].findChildren()[1].text)

# returns devpost user summary as list:
#   [username, proj_num, hack_num, event, event_size, awards_won, likes]
#   (event, event_size, awards_won, likes) is a repeating sequence, with exactly proj_num reps
#   awards_won is a comma-separated list of awards
def user_summary(user):
    res = [user]
    data = user_data(user)
    res.append(data['proj_num'])
    res.append(data['hack_num'])

    for proj_id in data['projects']:
        try:
            data = proj_data(proj_id)
        except:
            res[1] -= 1
            continue
        event_size = event_submits(data['event_url'])
        awards_won = ','.join(map(str, data['awards']))
        res.extend([data['event'], event_size, awards_won, data['like']])

    return res

# scrape applicant data
with open(in_file, 'r') as f:
    reader = csv.reader(f)
    user_apps = list(reader)
with open(out_file, 'w') as f:
    writer = csv.writer(f)
    for user in user_apps:
        writer.writerow(user_summary(user[0]))