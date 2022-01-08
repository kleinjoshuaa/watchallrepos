# lets you watch all the repos of a github account

# import the http client
import http.client
import json
import sys
import base64

# name of the github account to subscribe to
TARGET_ACCOUNT = "<Interesting Person's GH Account>"

# your github username
GITHUB_USERNAME = "<Youre GH Login Email Address>"




if len(sys.argv) < 2:
    print("You must supply a personal access token via the cmdline with -token <apiToken> \n (you can use a shell variable if you are concerend about shell history)")
    exit()

accessToken = sys.argv[2]


def subscribe(repo, token, username, account):
    conn = http.client.HTTPSConnection("api.github.com")
    payload = json.dumps({
    "subscribed": True
    })
    headers = {
    'Accept': 'application/vnd.github.v3+json"',
    'Authorization': 'Basic '+base64.b64encode((username+":"+token).encode('ascii')).decode('ascii'),
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    conn.request("PUT", "/repos/"+account+"/"+repo+"/subscription", payload, headers)
    res = conn.getresponse()
    status = res.status
    if status == 200:
        print("Successfully subscribed user {} to {}'s repo: {}".format(username, account, repo) )
    else:
        print("Error subscribing to repo \n\t {}", res.reason )
    conn.close()

def amISubscribed(repo, token, username, account):
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {
        'Authorization': 'Basic '+base64.b64encode((username+":"+token).encode('ascii')).decode('ascii'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    conn.request("GET", "/repos/"+account+"/"+repo+"/subscription", '', headers)
    res = conn.getresponse().status
    conn.close()
    if res == 200:
        return True
    else:
        return False




conn = http.client.HTTPSConnection("api.github.com")
payload = ''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
conn.request("GET", "/orgs/"+TARGET_ACCOUNT+"/repos", payload, headers)
res = conn.getresponse()
data = res.read()

jsonRepos = json.loads(data.decode('utf-8'))
conn.close()

repositories = []

# get all of the repos for that account that I am not subscribed to, and subscribe!
for k,v in enumerate(jsonRepos):
    print(v['name'])
    if not amISubscribed(v['name'], accessToken, GITHUB_USERNAME, TARGET_ACCOUNT):
        subscribe(v['name'], accessToken, GITHUB_USERNAME, TARGET_ACCOUNT)




