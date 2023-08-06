import json
from pymcure.client.publisher.sync import SyncPublisher
from pymcure.client.message import Message

def exec():
    data = json.dumps({'status': 'test'})
    msg = Message(['mytopicname'], data)
    publisher = SyncPublisher('http://127.0.0.1:3000','OmarksMerconSysteme')
    publisher.publish