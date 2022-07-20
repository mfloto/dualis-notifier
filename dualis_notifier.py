import pandas as pd
import requests
import re
import os.path

#CONSTANTS
#should use .env instead...
user=""
passwd=""
hook_url=""

def get_session(user, passwd):
    url = "https://dualis.dhbw.de/scripts/mgrqispi.dll"

    payload=f'usrname={user}%40student.dhbw-mannheim.de&pass={passwd}&APPNAME=CampusNet&PRGNAME=LOGINCHECK&ARGUMENTS=clino%2Cusrname%2Cpass%2Cmenuno%2Cmenu_type%2Cbrowser%2Cplatform&clino=000000000000001&menuno=000324&menu_type=classic&browser=&platform='
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dualis.dhbw.de/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://dualis.dhbw.de',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    regex_pattern_session = r"ARGUMENTS=(.*?),"

    return {
        "cookie" : response.headers["Set-Cookie"].split(";")[0].replace(" ", ""),
        "session" : re.search(regex_pattern_session, response.headers["REFRESH"]).group(1)
    }

def get_grades(cookie, session):
    url = f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS={session},-N000307,"

    payload={}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dualis.dhbw.de/',
    'Connection': 'keep-alive',
    'Cookie': f'{cookie}; {cookie}',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1'
    }

    response = requests.get(url, headers=headers, data=payload)

    return response.text

def extract_data_from_html(raw_html):
    tables = pd.read_html(raw_html)
    df = tables[0]
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    return df

def notify_server(name, hook_url):
    data = {
        "username" : "DUALIS"
    }
    data["embeds"] = [
        {
            "description" : f"Die Noten für {name} wurden veröffentlicht!",
            "title" : name
        }
    ]
    result = requests.post(hook_url, json = data)

if __name__ == "__main__":
    creds = get_session(user, passwd)
    raw_html = get_grades(cookie=creds["cookie"], session=creds["session"])
    table = extract_data_from_html(raw_html)

    file_exists = os.path.exists('grades.csv')

    if file_exists:
        old_grades = pd.read_csv('grades.csv', index_col=0)
        res = table.compare(old_grades)
        index_list = res.index.to_list()
        if len(index_list) == 0:
            print("I: No changes")
        for index in index_list:
            name = table.Name[index]
            print(f"I: New grades for {name}")
            notify_server(name, hook_url)
        table.to_csv("grades.csv")
    else:
        print("W: No cache found")
        table.to_csv("grades.csv")
        print("I: Created chache")
