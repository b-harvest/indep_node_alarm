import json
import time
import requests # sudo pip3 install requests
import pypd # sudo pip3 install pypd
import shutil

telegram_token = ""
telegram_chat_id = ""
pypd.api_key = ""
pypd.service_key = ""
pypd.href = ""

my_validator_address = ""
node_name = "<nodename>"

height_increasing_time_period = 600
missing_block_trigger = 10
free_disk_trigger = 10 # GB

def main() :

    node_list = []

    node_list.append(NodeInfo("<chainname>", "http://localhost:26657", my_validator_address))
    
    while True:

        # Disk Free Check
        check_freedisk("/")
        check_freedisk("/data")

        # Last Height Check
        for node in node_list:
            node.get_last_height()

        # ***** Wait *****
        time.sleep(height_increasing_time_period)

        # Check : stuck, block missing
        for node in node_list:
            if node.get_current_height() :
                node.check_height_stuck()
                node.check_block_missing()
                node.update_last_height()


class NodeInfo:

    def __init__(self, chain, rpc_url, validator_address):
        self.chain = chain
        self.rpc_url = rpc_url
        self.last_height = 0
        self.current_height = 0
        self.validator_address = validator_address

    def get_last_height(self):
        try:
            status = json.loads(requests.get(self.rpc_url + "/status", timeout=5).text)
            last_height = int(status["result"]["sync_info"]["latest_block_height"])

            self.last_height = last_height

        except Exception as e:
            alarm_content = f'{node_name} : {self.chain} - get_last_height - Exception: {e}'
            send_alarm(False, True, alarm_content)

    def get_current_height(self):
        try:
            status = json.loads(requests.get(self.rpc_url + "/status", timeout=15).text)
            current_height = int(status["result"]["sync_info"]["latest_block_height"])

            self.current_height = current_height
            return True

        except Exception as e:
            alarm_content = f'{node_name} : {self.chain} - get_current_height - Exception: {e}'
            send_alarm(False, True, alarm_content)
            return False
      
    def update_last_height(self):
        self.last_height = self.current_height

    def check_height_stuck(self): 

        if self.last_height == self.current_height :
            alarm_content = node_name + ": height stucked!"
            send_alarm(True, True, alarm_content)


    def check_block_missing(self):

        if self.validator_address == "":
            return

        missing_block_cnt = 0

        for height in range(self.last_height+1, self.current_height+1):
            precommit_match = False
            precommits = json.loads(requests.get(self.rpc_url + "/commit?height=" + str(height), timeout=5).text)["result"]["signed_header"]["commit"]["signatures"]
            
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

        if missing_block_cnt >= missing_block_trigger:
            
            alarm_content = f'{node_name} : {self.chain} - missing block count({missing_block_cnt}) >=  threshold({missing_block_trigger})'
            send_alarm(True, True, alarm_content)

## Functions
def check_freedisk(disk_location):
    total, used, free = shutil.disk_usage(disk_location)
    
    if (free//(2**30)) < free_disk_trigger:
        alarm_content = f'{node_name} : disk free is less than {free_disk_trigger} GB'
        send_alarm(True, True, alarm_content)


def send_alarm(b_pagerduty, b_telegram, alarm_content) :

    if b_pagerduty:

        pypd.Event.create(data={
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

    if b_telegram:
        try:
            requestURL = "https://api.telegram.org/bot" + str(telegram_token) + "/sendMessage?chat_id=" + telegram_chat_id + "&text="
            requestURL = requestURL + str(alarm_content)
            requests.get(requestURL, timeout=5)
        except Exception as e:
            print(f'Exception: {e}')    


if __name__ == "__main__":
    main()

