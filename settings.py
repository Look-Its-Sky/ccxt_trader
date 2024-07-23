import json, os

pairs = json.loads(os.environ['PAIRS'])
sleep_time = int(os.environ['SLEEP_TIME'])
