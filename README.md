# FCEN Aulas • Internal Dataserver

Acá está el código del servidor de datos internos de la app web [fcen-aulas](https://github.com/joangq/fcen-aulas).
En resumen el servidor interno se encarga de tener en caché los datos preprocesados para que el servidor que hace de [endpoint](https://github.com/joangq/fcen-aulas-endpoint) pueda fetchear los datos.
Se actualiza cada 1 minuto.

> [!NOTE]
> Esta versión, aunque funcional, es una versión de prueba.
> El código está muy desprolijo y tiene problemas de tight-coupling.

En una versión futura la idea es no usar un timer de un minuto, sino que se actualice cada más cantidad de tiempo, pero que reaccione ante pedidos del usuario (y se actualice acordemente).

