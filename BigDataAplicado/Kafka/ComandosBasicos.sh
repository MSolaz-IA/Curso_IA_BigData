###########
#TOPICS
###########

#Crear topic
kafka-topics.sh --bootstrap-server localhost:9092 --topic prueba --create

#Obtener el detalle de un topic
kafka-topics.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --describe

#Lista de topics creados
kafka-topics.sh --bootstrap-server localhost:9092 --list 

#Eliminar un topic 
kafka-topics.sh --bootstrap-server localhost:9092 --topic prueba --delete

#Crear un topic indicando el número de particiones
kafka-topics.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --create --partitions 2

#Crear un topic indicando el número de particiones y réplicas
kafka-topics.sh --bootstrap-server localhost:9092 --topic pruebareplicas --create --partitions 3 --replication-factor 2



###########
#PRODUCERS
###########

#Producir para un topic (si el topic no existe se creará automáticamente)
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones 
> Mensaje de Prueba

#Producir para un topic con keys. Las keys son interesantes ya que como estás usando claves (deporte y pais), los mensajes se agrupan en particiones según la clave. Kafka garantiza que los mensajes con la misma clave siempre se asignen a la misma partición, lo cual es útil para mantener el orden de los mensajes dentro de una clave específica.
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --property parse.key=true --property key.separator=:
>clave:valor
>deporte:baloncesto
>deporte:futbol
>deporte:natacion
>deporte:judo
>pais:colombia
>pais:espanya
>pais:portugal
>pais:italia

#acks - The number of acknowledgments the producer requires the broker leader to have received before considering a request complete. This controls the durability of records that are sent.
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --producer-property acks=all
# No existe una manera de comprobar que se reciben los ACKs de los Brokers pero se puede revisar los logs o con aplicaciones de terceros. También podemos configurar el producer para si no recibe los ACKs que reintente enviar los datos "retries=3" definiendo este parámetro desde el producer.properties o desde la CLI.


###########
#CONSUMERS
###########

#Consumir los mensajes que se reciben en un topic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones

#Consumir todos los mensajes de un topic des del inicio
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --from-beginning

#Mostrar propiedades de los mensajes recibidos
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --formatter org.apache.kafka.tools.consumer.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true --property print.partition=true --from-beginning


###########
#CONSUMER GROUPS
###########

#Antes de lanzar productores y consumidores, creo un topic con 3 particiones.
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic topicgrupo --partitions 3

#Lanzamos productor normal.
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic topicgrupo

#Lanzamos 3 consumidores cada uno en una consola diferente:
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topicgrupo --group testgrupoconsumers #Esto hacerlo x3

#¿Qué consumidor está recibiendo los datos? ¿Es siempre el mismo? ¿Por qué?
#Si no configuramos un particionador explícito o no usamos claves para los mensajes, existe el riesgo de que todos los mensajes vayan a la misma partición, y solo un consumidor en el grupo procese los mensajes. Usar RoundRobinPartitioner o claves adecuadas es clave para garantizar una distribución uniforme.
# Resumen: Si no usamos --producer-property partitioner.class=org.apache.kafka.clients.producer.RoundRobinPartitioner todos los mensajes irán a la misma partición y por ende los solo un consumidor del grupo leerá de esa partición.

# Monitorizamos el reparto de los mensajes
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topicgrupo --formatter org.apache.kafka.tools.consumer.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true --property print.partition=true --from-beginning

#Productor balancea aleatoriamente mensajes entre particiones de un mismo topic
kafka-console-producer.sh --bootstrap-server localhost:9092 --producer-property partitioner.class=org.apache.kafka.clients.producer.RoundRobinPartitioner --topic topicgrupo

#Iniciar un consumidor asociado a un grupo
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topicgrupo --group testgrupoconsumers

#Listar los grupos
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

#Monitorizamos detalles de un grupo de consumidores
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group testgrupoconsumers

###########
#CONSUMER GROUPS
###########

#Monitorizamos detalles de un grupo de consumidores
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group testgrupoconsumers

#Intentamos leer desde el principio del topic. Pero solo conseguiremos leer desde la última posición del offset
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topicgrupo --group testgrupoconsumers --from-beginning

#PARECE SER QUE EN LA VERSION 3.9.0 de kafka ya no hay que ejecutar el --DRY-RUN, SOLO CON --execute funciona.
#Mover el offset a la posición cero (no se formaliza hasta que se lanza el "--execute")
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group testgrupoconsumers --reset-offsets --to-earliest --topic topicgrupo --dry-run

#Mover el offset a la posición cero
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group testgrupoconsumers --reset-offsets --to-earliest --topic topicgrupo --execute

###########
# HERRAMIENTAS OPEN SOURCE PARA MONITORIZAR CLUSTERS DE KAFKA
###########

https://github.com/obsidiandynamics/kafdrop

https://github.com/provectus/kafka-ui

https://github.com/theurichde/kowl

https://www.elastic.co/blog/monitoring-kafka-with-elasticsearch-kibana-and-beats

###########
# HERRAMIENTAS DE PAGO PARA MONITORIZAR CLUSTERS DE KAFKA
###########

https://www.datadoghq.com/blog/monitor-kafka-with-datadog/

https://www.redpanda.com/

https://newrelic.com/instant-observability/kafka

https://www.kadeck.com/blog/introducing-kadeck-5
