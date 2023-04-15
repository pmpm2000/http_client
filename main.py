import sys
import requests
import json
import time
from datetime import datetime

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You have to specify the host as a launching parameter.")
        exit(0)
    host = sys.argv[1]
    delay = 5  # delay between requests
    num_checks = 10  # number of requests to send

    log_file = open('log.txt', 'a')

    sent = 0
    received = 0
    lost = 0
    min_ping = float('inf')
    max_ping = 0
    sum_ping = 0
    is_json = False

    for i in range(num_checks):
        # send the request
        start_time = time.time()
        response = requests.get(host)
        end_time = time.time()

        # measure response time and extract status code
        response_time = end_time - start_time
        status_code = response.status_code

        # check if the response is json
        content_type = response.headers.get('Content-Type')
        if content_type == 'application/json':
            is_json = True

        # validate json syntax
        try:
            json.loads(response.content)
            is_valid_json = True
        except ValueError:
            is_valid_json = False

        # log
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] status_code={status_code}, is_json={is_json}, is_valid_json={is_valid_json}, response_time={response_time:.2f}s\n'
        print(log_entry, end='')
        log_file.write(log_entry)

        # ping statistics
        sent += 1
        if status_code == 200:
            received += 1
            min_ping = min(min_ping, response_time)
            max_ping = max(max_ping, response_time)
            sum_ping += response_time
        else:
            lost += 1

        time.sleep(delay)

    if sent > 0:
        packet_loss = lost / sent * 100
        avg_ping = sum_ping / received
        log_entry = f'Ping statistics: sent={sent}, received={received}, lost={lost} ({packet_loss:.1f}% loss), min_ping={min_ping:.2f}s, max_ping={max_ping:.2f}s, avg_ping={avg_ping:.2f}s\n'
        print(log_entry, end='')
        log_file.write(log_entry)

    log_file.close()
