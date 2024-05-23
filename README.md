# OpenStack notifications bridge to Kafka

Sometimes you might need to fetch events from nova (or even neutron) and then push all of them to another MQ. This implements sending notifications to Kafka as a more reliable solution. tenant_id is used as topic, instance uuid used as key to keep the same partition for consistent messages order.

## [airtai/faststream](https://github.com/airtai/faststream) is used here
FastStream is a powerful and easy-to-use Python framework for building asynchronous services interacting with event streams such as Apache Kafka, RabbitMQ, NATS and Redis.
