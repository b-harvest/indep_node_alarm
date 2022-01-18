cd /home/ubuntu/indep_node_alarm;echo "[Unit]
Description=indep_node_alarm
After=network-online.target
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/indep_node_alarm
ExecStart=/usr/bin/python3 /home/ubuntu/indep_node_alarm/indep_node_alarm.py
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=indep_node_alarm
Restart=always
RestartSec=200
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target" > indep_node_alarm.service;sudo mv indep_node_alarm.service /etc/systemd/system/;sudo systemctl enable indep_node_alarm.service

cd /home/ubuntu/indep_node_alarm;echo "[Unit]
Description=indep_node_alarm_check
After=network-online.target
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/indep_node_alarm
ExecStart=/usr/bin/python3 /home/ubuntu/indep_node_alarm/indep_node_alarm_check.py
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=indep_node_alarm_check
Restart=always
RestartSec=200
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target" > indep_node_alarm_check.service;sudo mv indep_node_alarm_check.service /etc/systemd/system/;sudo systemctl enable indep_node_alarm_check.service

