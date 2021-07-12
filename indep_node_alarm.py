import json
import time
import requests # sudo pip3 install requests
import pypd # sudo pip3 install pypd
import subprocess
import shutil

telegram_token = ""
telegram_chat_id = ""
pypd.service_key = ""
pypd.href = ""

my_validator_address = ""
node_name = "<nodename>"

height_increasing_time_period = 600
missing_block_trigger = 10

try:
    status = json.loads(requests.get("http://localhost:26657/status").text)
    last_height = int(status["result"]["sync_info"]["latest_block_height"])
except:
    last_height = 0

while True:
    
    time.sleep(height_increasing_time_period)

    #cmd = "sudo <chain deamon> version --long > /home/ubuntu/ansible/<chain deamon>_version.out"
    #subprocess.check_output(cmd, shell=True)
    #cmd = "sudo <chaincli deamon> version --long > /home/ubuntu/ansible/<chaincli deamon>_version.out"
    #subprocess.check_output(cmd, shell=True)
    #cmd = "sudo python3 /home/ubuntu/ansible/indep_node_alarm_check.py"
    #subprocess.check_output(cmd, shell=True)

    alarm = False
    alarm_content = ""
    total, used, free = shutil.disk_usage("/")
    
    try:
        current_height = int(json.loads(requests.get("http://localhost:26657/status").text)["result"]["sync_info"]["latest_block_height"])
    except:
        current_height = last_height
    if (free//(2**30)) < 10:
        alarm = True
        alarm_content = node_name + ": disk free 9GB"
    # height doesn't change
    if current_height == last_height:
        alarm = True
        alarm_content = node_name + ": height stucked!"
    else:
        # missing count
        missing_block_cnt = 0
        for height in range(last_height+1,current_height+1):
            precommit_match = False
            try:
                precommits = json.loads(requests.get("http://localhost:26657/commit?height=" + str(height)).text)["result"]["signed_header"]["commit"]["signatures"]
                for precommit in precommits:
                    try:
                        validator_address = precommit["validator_address"]
                    except:
                        validator_address = ""
                    if validator_address == my_validator_address:
                        precommit_match = True
                        break
                if precommit_match == False:
                    missing_block_cnt += 1
            except:
                alarm = True
                alarm_content = node_name + ": chain daemon dead!"
        if missing_block_cnt >= missing_block_trigger:
            alarm = True
            alarm_content = node_name + ": missing blocks >= 10"

    if alarm:

        result = pypd.Event.create(data={
            'service_key': pypd.service_key,
            'event_type': 'trigger',
            'description': alarm_content,
            'contexts': [
                  {
                      'type': 'link',
                      'href': pypd.href,
                      'text': 'View in Control Server',
                  },
            ],
        })

        try:
            requestURL = "https://api.telegram.org/bot" + str(telegram_token) + "/sendMessage?chat_id=" + telegram_chat_id + "&text="
            requestURL = requestURL + str(alarm_content)
            response = requests.get(requestURL, timeout=1)
        except:
            pass

    last_height = current_height
