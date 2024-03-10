import json


def handler(event, context):
    print(f"[DEBUG] event: {event}")
    print(f"[DEBUG] context: {context}")
    return {"statusCode": 200, "body": json.dumps(event)}
