from config import settings

class SensorEventProcessor:
    def __init__(self):
        pass

    def process(self,event):
        """ TODO: realizar el procesamiento del evento que se recibe por WebSocket """
        """ todas las conexiones a las bases de datos estan accesibles mediante la variable settings """
        settings.mongo_dao.inser_one('matriculas',event)

        settings.redis_dao.increment(event['sensor'])
    
        settings.redis_dao.set(f"last_sensor_info_{event['vehicle']['id']}", event['sensor'])

        print('------VEHICULO REGISTRADO------')
        print(settings.mongo_dao.find_one(
            'matriculas',
            filter={"timestamp": event['timestamp']}
        ))

        print('------SENSOR COUNT------')
        print(settings.redis_dao.get(event['sensor']))

        print('------LAST SENSOR ACTIVATED INFO------')
        print(settings.redis_dao.get(f"last_sensor_info_{event['sensor']}"))

