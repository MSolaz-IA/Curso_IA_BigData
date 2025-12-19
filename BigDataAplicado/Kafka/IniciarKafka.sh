#Crear nuevo Cluster Kafka con un ID random.
kafka-storage.sh random-uuid

#Configurar directorio Logs. Es necesario porque inicializa el almacenamiento de logs de Kafka y asigna un Cluster ID único.
#El archivo server.properties contiene toda la configuración necesaria para el broker, incluida la ubicación del almacenamiento de logs (log.dirs) y otros parámetros esenciales como:
#    log.dirs: Directorios donde Kafka almacenará los logs de datos y metadatos.
#    node.id: Identificador único del nodo en el clúster.
#    process.roles: Define si el nodo es controlador (controller), un broker o ambos.
#    controller.quorum.voters: Especifica los nodos que forman parte del quorum del controlador.
kafka-storage.sh format -t ID -c /kafka_2.13-3.9.0/config/kraft/server.properties
ID de mi Cluster = iifpkj4cTbeqy0BfBN22Wg

#Inicializar Kafka en daemon mode.
kafka-server-start.sh /kafka_2.13-3.9.0/config/kraft/server.properties

