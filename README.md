# dualis-notifier
Sends a discord-notification when ever new grades are available on ```dualis.dhbw.de```. This script runs periodically via a cronjob (e.g. every 15 minutes), saving the current grades as a .csv everytime they change.

## about the semester_id
- ```-N000000015088000``` -> WiSe 21/22
- ```-N000000015098000``` -> SoSe 2022
- ```-N000000015118000``` -> SoSe 2023

## other constants
- user: this is the username in the form of sXXXXXX
- passwd: your password for dualis
- hook_url: the webhook url from discord
