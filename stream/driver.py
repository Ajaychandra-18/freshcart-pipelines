import json, os, sys
import pika

BROKER = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
EXCHANGE = "rapido-dispatch"

if len(sys.argv) != 3:
    sys.exit("usage: python driver.py NAME PATTERN")
name, pattern = sys.argv[1], sys.argv[2]

conn = pika.BlockingConnection(pika.URLParameters(BROKER))
ch = conn.channel()
ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")

# private queue: server-named and exclusive to this driver
queue = ch.queue_declare(queue="", exclusive=True).method.queue
ch.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)
print(f"[{name}] waiting on pattern {pattern}", flush=True)


def on_message(channel, method, properties, body):
    msg = json.loads(body)
    if "zone" not in msg:
        # bad message: reject and do NOT requeue
        print(f"[{name}] REJECTED (nack) key={method.routing_key} id={msg['id']} - missing zone", flush=True)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        print(f"[{name}] processed key={method.routing_key} id={msg['id']} zone={msg['zone']}", flush=True)
        channel.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
ch.start_consuming()
