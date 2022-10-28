# Independatn Node Alarm

## Overview

indep_node_alarm is a python script to detect abnormality on tendermint node and notify via Telegram and PagerDuty. 

- indep_node_alarm.py : It detects missed block signings, block height stuck, and low free disk space.
- indep_node_alarm_check.py : It detects inactivated daemon services.

## Installation

```bash
git clone https://github.com/b-harvest/indep_node_alarm.git
cd indep_node_alarm

sudo apt-get -y install python3-pip && sudo pip3 install requests pypd
sudo -H pip3 install -r requirements.txt

```

## Customize as your need

```bash

export YOURHOME=/home/ubuntu
export NODE_NAME="<your hostname>"
export DAEMON_NAME="<your chain daemon name : eg. gaiad>"
export CHAIN_NAME="<the chain name : eg. Cosmos"

export MY_VALIDATOR_ADDRESS="<yout validator address>"
# export MY_VALIDATOR_ADDRESS=$(gaiad status | egrep "Address" | awk -F : '{print $2}' | awk -F \" '{print $2}')

export TG_CRITICAL_TOKEN="<Telegram Token for Critical Notification>"
export TG_CRITICAL_CHAT_ID="<Telegram Chat ID for Critical Notification>"
export TG_INFO_TOKEN="<Telegram Token for Normal Notification>"
export TG_INFO_CHAT_ID="<Telegram Chat ID for Normal Notification>"

export PYPD_API_KEY="<PagerDuty Api Key>"
export PYPD_SERVICE_KEY="<PagerDuty Service Key>"

export MISSING_BLK=15 # This is a threshold to trigger the block missing alarm

# indep_node_alarm.py 
sed -i -e "s/telegram_token =.*/telegram_token = \"$TG_CRITICAL_TOKEN\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/telegram_chat_id =.*/telegram_chat_id = \"$TG_CRITICAL_CHAT_ID\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/pypd.api_key =.*/pypd.api_key = \"$PYPD_API_KEY\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/pypd.service_key =.*/pypd.service_key = \"$PYPD_SERVICE_KEY\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/pypd.href =.*/pypd.href = \"$NODE_NAME\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py

sed -i -e "s/my_validator_address =.*/my_validator_address = \"$MY_VALIDATOR_ADDRESS\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/node_name = \"<nodename>\"/node_name = \"$NODE_NAME\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/missing_block_trigger = 10/missing_block_trigger = $MISSING_BLK/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py
sed -i -e "s/<chainname>/$CHAIN_NAME/g" $YOURHOME/indep_node_alarm/indep_node_alarm.py

# indep_node_alarm_check.py
sed -i -e "s/telegram_token =.*/telegram_token = \"$TG_INFO_TOKEN\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm_check.py
sed -i -e "s/telegram_chat_id =.*/telegram_chat_id = \"$TG_INFO_CHAT_ID\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm_check.py

sed -i -e "s/node_name = \"<nodename>\"/node_name = \"$NODE_NAME\"/g" $YOURHOME/indep_node_alarm/indep_node_alarm_check.py
sed -i -e "s/<daemonname>/$DAEMON_NAME/g" $YOURHOME/indep_node_alarm/indep_node_alarm_check.py

```

## Create service files and start

```bash

cd $YOURHOME/indep_node_alarm
bash indep_node_alarm_service.sh

sudo systemctl daemon-reload

sudo systemctl start indep_node_alarm
sudo systemctl status indep_node_alarm

sudo systemctl start indep_node_alarm_check
sudo systemctl status indep_node_alarm_check

```
