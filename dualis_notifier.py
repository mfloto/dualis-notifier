import pandas as pd
import requests
import re
import os

# CONSTANTS
user = ""
passwd = ""
semester_id = ""
hook_url = ""
user_agent = "Dualis Notifier"


def get_session(user, passwd):
    url = "https://dualis.dhbw.de/scripts/mgrqispi.dll"

    payload = f'usrname={user}%40student.dhbw-mannheim.de&pass={passwd}&APPNAME=CampusNet&PRGNAME=LOGINCHECK&ARGUMENTS=clino%2Cusrname%2Cpass%2Cmenuno%2Cmenu_type%2Cbrowser%2Cplatform&clino=000000000000001&menuno=000324&menu_type=classic&browser=&platform='
    headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    regex_pattern_session = r"ARGUMENTS=(.*?),"

    return {
        "cookie": response.headers["Set-Cookie"].split(";")[0].replace(" ", ""),
        "session": re.search(regex_pattern_session, response.headers["REFRESH"]).group(1)
    }


def get_grades(cookie, session, semester_id):
    url = f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS={session},-N000307,{semester_id}"

    headers = {
        'User-Agent': user_agent,
        'Cookie': f'{cookie}; {cookie}',
    }

    response = requests.get(url, headers=headers)

    with open("grades.html", "w") as f:
        f.write(response.text)

    return response.text


def extract_data_from_html(raw_html):
    tables = pd.read_html(raw_html)
    df = tables[0]
    df.drop(df.columns[df.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    return df


def notify_server(name, hook_url):
    data = {
        "username": "DUALIS"
    }
    data["embeds"] = [
        {
            "description": f"Die Noten für {name} wurden veröffentlicht!",
            "title": name
        }
    ]
    requests.post(hook_url, json=data)


if __name__ == "__main__":
    creds = get_session(user, passwd)
    raw_html = get_grades(
        cookie=creds["cookie"], session=creds["session"], semester_id=semester_id)
    table = extract_data_from_html(raw_html)

    if os.path.exists('grades.csv'):
        old_grades = pd.read_csv('grades.csv', index_col=0)
        res = table.compare(old_grades)
        index_list = res.index.to_list()

        if len(index_list) == 0:
            print("I: No changes")
            os._exit(0)

        for index in index_list:
            name = table.Name[index]
            if name == "Semester-GPA":
                continue
            print(f"I: New grades for {name}")
            notify_server(name, hook_url)

        table.to_csv("grades.csv")
    else:
        print("W: No cache found")
        table.to_csv("grades.csv")
        print("I: Created chache")
