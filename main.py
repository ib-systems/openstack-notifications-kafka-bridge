import json
import argparse
import configparser
from faststream import FastStream, Logger
from faststream.rabbit import (
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
    ExchangeType,
    RabbitMessage,
)
from faststream.confluent import KafkaBroker


parser = argparse.ArgumentParser()
parser.add_argument("--config-file", help="Config file path", default="events-bridge.conf")
known_args, extra = parser.parse_known_args()

config = configparser.ConfigParser()
config.read(known_args.config_file)
kafka_conf = config["kafka"]
amqp_conf = config["amqp"]
ignored_events = amqp_conf.get('ignore_events', "").split(',')
print("AMQP", ignored_events)
kafka_broker = KafkaBroker(kafka_conf["bootstrap_servers"])
rabbit_broker = RabbitBroker(
    (
        f"amqp://{amqp_conf["username"]}:{amqp_conf["password"]}"
        "@"
        f"{amqp_conf["host"]}:{amqp_conf["port"]}"
    ),
    virtualhost=amqp_conf["vhost"],
)

exch = RabbitExchange(amqp_conf['nova_exchange_name'], type=ExchangeType.TOPIC, passive=True)
nova_queue = RabbitQueue(
    amqp_conf['consumer_queue_name'],
    auto_delete=False,
    routing_key="versioned_notifications.info",
)
app = FastStream(rabbit_broker)


@rabbit_broker.subscriber(queue=nova_queue, exchange=exch, no_ack=False)
async def handle_nova_event(data, logger: Logger, msg: RabbitMessage):
    oslo_message = json.loads(data.get("oslo.message"))
    event_type = oslo_message.get("event_type")
    if event_type is not None:
        if event_type not in ignored_events:
            nova_data = oslo_message.get("payload").get("nova_object.data")
            instance_uuid = nova_data.get("uuid")
            logger.info(f"Event {event_type} for instance {instance_uuid} received")
            try:

                await kafka_broker.publish(
                    oslo_message, key=instance_uuid.encode("utf-8"),
                    topic=nova_data.get("tenant_id"),
                    headers={"event-name": event_type},
                )
                await msg.ack()
            except Exception:
                pass
        else:
            logger.info(f"Event {event_type} is in list of ignored event types")
            await msg.ack()


@app.on_startup
async def on_start():
    # Use case to create subscriber programmatically.

    # nova_sub = rabbit_broker.subscriber(queue=nova_queue,
    #    exchange=exch, no_ack=False
    # )
    # nova_sub(handle_nova_event)
    # rabbit_broker.setup_subscriber(subscriber=nova_sub)
    await kafka_broker.start()
