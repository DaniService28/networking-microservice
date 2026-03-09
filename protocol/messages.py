import json

def encode_message(action, payload=None):
    if payload is None:
        payload = {}
    message = {
        "action": action,
        "payload": payload
    }
    return json.dumps(message).encode("utf-8")

def decode_message(raw_data):
    try:
        return json.loads(raw_data.decode("utf-8"))
    except:
        return None