import json
import os
import sys
from dotenv import load_dotenv

from config import settings

from consumer.websocket_consumer import WebSocketConsumer

from processors.sensor_event_processor import SensorEventProcessor


def test():
    """ prueba de las conexiones disponibles """

    settings.redis_dao.set('name','maria')
    print(settings.redis_dao.get('name'))
   
    record = {'name':'maria'}
    settings.mongo_dao.inser_one('users',record)
    print(settings.mongo_dao.find_one('users'))

    settings.postgres_dao.insert(sql='insert into users_example(name) values (%s)',values=("maria",))
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
    contador_sensores = {}
    last_car_sensored = {}

    data['matriculas'] = settings.mongo_dao.find('matriculas')

    sensor = [i for i in range(1,10)]   
    coches = [f'CAR{i:02}' for i in range(1, 11)]

    for s in sensor:
        contador_sensores[f'sensor{s}'] = (settings.redis_dao.get(f'sensor{s}'))
  
    for s in coches:        
        last_car_sensored[f'{s}'] = (settings.redis_dao.get(f"last_sensor_info_{s}"))
    
    data['contador_sensores'] = contador_sensores
    data['last_car_sensored'] = last_car_sensored

    print(json.dumps(data, indent=4, ensure_ascii=False))



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
        