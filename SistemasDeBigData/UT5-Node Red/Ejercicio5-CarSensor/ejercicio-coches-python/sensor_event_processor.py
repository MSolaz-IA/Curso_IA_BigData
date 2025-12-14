from config import settings

class SensorEventProcessor:
    def __init__(self):
        pass

    def process(self,event):
        """ TODO: realizar el procesamiento del evento que se recibe por WebSocket """
        """ todas las conexiones a las bases de datos estan accesibles mediante la variable settings """
        print(event) 
        #MongoDB
        settings.mongo_dao.inser_one('events',event)
        #Redis
        settings.redis_dao.increment(f'count:{event['sensor']}')
     
        settings.redis_dao.set(f'v:{event['vehicle']['id']}_sensor', event['sensor'])
        