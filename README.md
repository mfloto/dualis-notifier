# dualis-notifier
Sends a discord-notification when ever new grades are available on ```dualis.dhbw.de```. This script runs periodically via a cronjob (e.g. every 5 minutes), saving current grades as a .csv everytime they change. It is designed to be as simple and easy to understand as possible.

## future plans
In the future this script will be migrated to GCP (or similar): It will run as a Cloud Function triggered periodically by the Cloud Scheduler and stores its state using FireStore. <br>
(Alternatively everything could run as is on an e2-micro-instance)

## about the semester_id
- ```-N000000015088000``` -> WiSe 21/22
- ```-N000000015098000``` -> SoSe 2022
- ```-N000000015118000``` -> SoSe 2023

## other constants
- user: username in the form of sXXXXXX
- passwd: password for dualis
- hook_url: webhook url from discord
