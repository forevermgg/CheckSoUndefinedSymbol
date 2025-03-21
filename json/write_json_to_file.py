import json

control = {"bw": 100, "delay": "10ms", "jitter": None, "loss": 0, "max_queue_size": None,
           "speedup": 0, "use_htb": True}

# data={"bw": 100,"delay": "1ms","jitter": None,"loss": 0,"max_queue_size": None,"speedup": 0,
#        "use_htb": True}
json.dump(control, open('version.json', 'w'), indent=4)
# json.dump(data,open('configuration.json','w'),indent=4)
