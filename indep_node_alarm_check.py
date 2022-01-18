import subprocess
import requests # sudo pip3 install requests
import time

telegram_token = ""
telegram_chat_id = ""

node_name = "<nodename>"
check_internal = 300

while True:
    nodealarm_status = subprocess.check_output("service indep_node_alarm status | grep Active", shell=True).decode('utf-8')
    nodealarm_status = str(nodealarm_status).split(":")[1].strip()[:6]

    if nodealarm_status != "active":

        alarm_content = "indep_node_alarm is NOT active, check this node : " + node_name

        try:
            requestURL = "https://api.telegram.org/bot" + str(telegram_token) + "/sendMessage?chat_id=" + telegram_chat_id + "&text="
            requestURL = requestURL + str(alarm_content)
            response = requests.get(requestURL, timeout=1)
        except:
            pass

    time.sleep(check_internal)