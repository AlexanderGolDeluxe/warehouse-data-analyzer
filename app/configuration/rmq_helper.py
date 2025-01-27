import aio_pika
from aiormq import AMQPConnectionError
from loguru import logger

from app.config import RMQ_URL


class RabbitMQHelper:

    def __init__(self, rmq_url: str):
        self.__rmq_url = rmq_url

    async def __set_connection(self):
        try:
            self.connection = await aio_pika.connect(
                self.__rmq_url
            )
            logger.info("RabbitMQ connect successfully")
        except AMQPConnectionError as e:
            logger.critical(
                f"RabbitMQ connection error: {e}. {RMQ_URL=}")

    async def __set_channel(self):
        self.channel = await self.connection.channel()

    async def init_connect(self):
        await self.__set_connection()
        if hasattr(self, "connection"):
            await self.__set_channel()

    async def close_connect(self):
        await self.channel.close()
        await self.connection.close()

    def get_channel(self):
        return self.channel

    async def ack_messages(self, messages: list):
        for message in messages:
            await message.ack()

    async def nack_messages(self, messages: list, requeue: bool = True):
        for message in messages:
            await message.nack(requeue=requeue)


rmq_helper = RabbitMQHelper(rmq_url=RMQ_URL)
