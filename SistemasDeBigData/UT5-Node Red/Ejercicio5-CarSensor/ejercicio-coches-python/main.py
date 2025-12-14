
import os
import sys
from dotenv import load_dotenv

from config import settings

from consumer.websocket_consumer import WebSocketConsumer

from processors.sensor_event_processor import SensorEventProcessor


def test():
    """ prueba de las conexiones disponibles """

    settings.redis_dao.set('name','mario')
    print(settings.redis_dao.get('name'))
   
    record = {'name':'mario'}
    settings.mongo_dao.inser_one('users',record)
    print(settings.mongo_dao.find_one('users'))

    settings.postgres_dao.insert(sql='insert into users_example(name) values (%s)',values=("mario",)) # type: ignore
    print(settings.postgres_dao.find_all(table='users_example'))

def process():
    """ activa el consumidor de mensajes de WebSocket """
    processor = SensorEventProcessor()

    WebSocketConsumer(
        url=os.getenv('WEBSOCKET_URL'),
        processor=processor.process
    )

def summary():
    data = {}
    """ TODO: preparar las queries necesarias para rellenar el diccionario data con la información """
    mongo_logs_data = settings.mongo_dao.find('events')
    data['historic'] = mongo_logs_data
    
    for i in range(1,9):
        data['count_sensor'+str(i)] = settings.redis_dao.get("count:sensor"+str(i))

    for i in range(1,11):
        if i < 10:
            data['last_sensor_CAR0'+str(i)] = settings.redis_dao.get("v:CAR0"+str(i)+"_sensor")
        else:
            data['last_sensor_CAR'+str(i)] = settings.redis_dao.get("v:CAR"+str(i)+"_sensor")
    
    print(data)

if __name__ == "__main__":
    load_dotenv()
    settings.init()
    match sys.argv[1]:
        case "test":
            test()
        case "process":
            process()
        case 'summary':
            summary()
        