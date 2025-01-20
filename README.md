# OpenStack notifications bridge to Kafka

Sometimes you might need to fetch events from nova (or even neutron) and then push all of them to another MQ. This implements sending notifications to Kafka as a more reliable solution. tenant_id is used as topic, instance uuid used as key to keep the same partition for consistent messages order.

# Deployment
1. git clone
```
git clone https://github.com/ib-systems/openstack-notifications-kafka-bridge
```
2. Build Docker image
```
docker compose build
```
3. Run
```
docker compose up onkb
```

# Params
`--config-file` allows to provide custom config path

## [airtai/faststream](https://github.com/airtai/faststream) is used here
FastStream is a powerful and easy-to-use Python framework for building asynchronous services interacting with event streams such as Apache Kafka, RabbitMQ, NATS and Redis.


# Notes
- WIP: There is ability to manually create subscribers that could be used to mount to multiple nova_cell* vhosts in case of large deployments;
  ```python
  subscriber = broker.subscriber("dynamic")
  subscriber(handler_method)
  ...
  broker.setup_subscriber(subscriber)
  await subscriber.start()
  ...
  await subscriber.close()
  ```