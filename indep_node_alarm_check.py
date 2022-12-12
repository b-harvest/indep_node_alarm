import subprocess
import requests # sudo pip3 install requests
import time

telegram_token = ""
telegram_chat_id = ""

node_name = "<nodename>"
check_internal = 300


def main() :
    while True:
        check_daemon("indep_node_alarm")
        check_daemon("<servicename>")

        time.sleep(check_internal)


def check_daemon(daemon_name):

    daemon_status = subprocess.check_output(eval(f'f"""service {daemon_name} status | grep Active"""'), shell=True).decode('utf-8')
    daemon_status = str(daemon_status).split(":")[1].strip()[:6]

    if daemon_status != "active":

        if daemon_name == "indep_node_alarm":
            subprocess.check_output(eval(f'f"""sudo systemctl start {daemon_name}"""'), shell=True)
            alarm_content = daemon_name + " has started : " + node_name
            send_alarm(alarm_content)

        else:
            alarm_content = daemon_name + " is NOT active, check this node : " + node_name
            send_alarm(alarm_content)


def send_alarm(alarm_content):
    try:
        requestURL = "https://api.telegram.org/bot" + str(telegram_token) + "/sendMessage?chat_id=" + telegram_chat_id + "&text=" + str(alarm_content)
        requests.get(requestURL, timeout=3)

    except Exception as e:
        print(f'Exception: {e}')


if __name__ == "__main__":
    main()
