import json, os, random, time, uuid
from datetime import datetime, timezone
import pika

# Broker URL comes from an environment variable so it never goes into Git
BROKER = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
EXCHANGE = "rapido-dispatch"
ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield"],
}

conn = pika.BlockingConnection(pika.URLParameters(BROKER))
ch = conn.channel()
ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")

count = 0
while True:
    count += 1
    city = random.choice(["bangalore", "chennai"])
    zone = random.choice(ZONES[city])
    rtype = random.choice(["ride", "food"])
    key = f"{city}.{zone}.{rtype}"
    msg = {"id": str(uuid.uuid4())[:8], "city": city, "zone": zone, "type": rtype,
           "ts": datetime.now(timezone.utc).isoformat()}
    bad = (count % 10 == 0)
    if bad:
        del msg["zone"]  # every 10th message is malformed (D3)
    ch.basic_publish(exchange=EXCHANGE, routing_key=key, body=json.dumps(msg))
    print(f"PUBLISHED{' BAD' if bad else ''} key={key} id={msg['id']}", flush=True)
    time.sleep(2)
