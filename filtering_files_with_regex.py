#!/usr/bin/env python3

import re
import operator
import csv

error = {}
error_columns = ['Error', 'Count']
per_user_columns = ['Username', 'INFO', 'ERROR']
per_user = []
pattern = r"ticky: (INFO|ERROR) ([\w ]*).*\((.*)\)"
with open('syslog.log', 'r') as log_f:
    reader = log_f.readlines()
    for err in reader:
        entry = re.search(pattern, err)
        msg_type, message, user = entry.groups()
        if msg_type == "ERROR":
            if message in error:
                error[message] += 1
            else:
                error[message] = 1
        index = next((i for i, item in enumerate(per_user) if item["Username"] == user), -1)
        if index != -1:
            per_user[index][msg_type] += 1
        else:
            per_user.append({"Username": user, "ERROR": 0, "INFO": 0})
            per_user[len(per_user)-1][msg_type] += 1

errors = sorted(error.items(), key = operator.itemgetter(1), reverse=True )
per_users = sorted(per_user, key = operator.itemgetter("Username"))

with open('user_statistics.csv', 'w') as users_s:
        writer = csv.DictWriter(users_s, fieldnames=per_user_columns)
        writer.writeheader()
        writer.writerows(per_users)

with open('error_message.csv', 'w') as errors_s:
        writer = csv.writer(errors_s)
        writer.writerow(error_columns)
        writer.writerows(errors)
