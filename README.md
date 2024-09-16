# dualis-notifier
Sends a discord-notification when ever new grades are available on ```dualis.dhbw.de``` (module grades only). This script runs periodically via a cronjob (e.g. every 15 minutes), saving current grades as a .csv everytime they change. It is designed to be as simple and easy to understand as possible.

## usage
```bash
docker run -e DUALIS_USER="your_username" -e DUALIS_PASSWD="your_password" -e SEMESTER_ID="-N000000015088000" -e DISCORD_WEBHOOK="your_webhook" dualis-notifier
```

## configuration
This is done using environment variables passed through docker.

- ```DUALIS_USER``` -> your dualis username
- ```DUALIS_PASSWD``` -> your dualis password
- ```SEMESTER_ID``` -> the semester_id of the semester you want to get the grades from
- ```DISCORD_WEBHOOK``` -> the webhook url to send the notifications to
- ```AGENT_NAME``` -> user agent string included in the request (defaults to "Dualis Notifier")

## about the semester_id
- ```-N000000015088000``` -> WiSe 21/22
- ```-N000000015098000``` -> SoSe 2022
- ```-N000000015108000``` -> WiSe 22/23
- ```-N000000015118000``` -> SoSe 2023
- ```-N000000015128000``` -> WiSe 23/24
- ```-N000000015138000``` -> SoSe 2024

## current deployment
At the moment the script runs on a Standard B1s Azure-Instance.

## TODO
- [x] containerize
- [ ] aggregate data from multiple accounts (to cover retaken exams)
- [ ] handle changed grades (apparently if the grade of a single person is changed, the dhbw unpublishes and republishes everyone’s grades for that module)
