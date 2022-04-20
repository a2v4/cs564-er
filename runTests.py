#! /usr/bin/python3

import subprocess

tests = {"query1.sql": 13422,
         "query2.sql": 80,
         "query3.sql": 8365,
         "query4.sql": 1046871451,
         "query5.sql": 3130,
         "query6.sql": 6717,
         "query7.sql": 150}

for file in tests:
    command = f"sqlite3 ebay < {file}"
    output = subprocess.run(["bash", "-c", command],
                            capture_output=True).stdout.decode().strip()

    print(
        f"Test: '{file}' - Output: {output}, Expected: {tests[file]} - {['Fail', 'Passed'][tests[file]==int(output)]}")
