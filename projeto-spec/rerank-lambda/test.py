from src.event_ import RagEvent
event = {
    "query": 'who proposed the geocentric theory',
    "index": "1234",
    "kTopPassages": 10,
    "reRankConfig": {"kTopPassages": 2,"minScore": -20 },
    "minScore": 0,"adjacentPassages": 1
}
import requests

def run():
    B = requests.post(
        url="http://localhost:9000/2015-03-31/functions/function/invocations",
        json=event
        )
    print(B)
    print(B.json())
    return B
run()
# from app import handler
# a = handler(event, {})
# print(a)


