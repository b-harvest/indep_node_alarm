import subprocess
import time

nodealarm_status = subprocess.check_output("sudo service indep_node_alarm status | grep Active", cwd='/home/ubuntu/indep_node_alarm', shell=True).decode('utf-8')
nodealarm_status = str(nodealarm_status).split(":")[1].strip()[:6]
if nodealarm_status == "active":
    nodealarm_status = str(time.time())
else:
    nodealarm_status = "False"
with open("/home/ubuntu/indep_node_alarm/indep_node_alarm_status.log", "w+") as f:
    f.write(nodealarm_status)