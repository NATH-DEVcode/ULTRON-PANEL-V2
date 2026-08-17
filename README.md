╔══════════════════════════════════════════════════════╗
║             ULTRON PANEL — UHD CORE V2             ║
╚══════════════════════════════════════════════════════╝


║ DESCRIPCIÓN ║

ULTRON PANEL — UHD CORE V2 es un proyecto de código abierto
desarrollado principalmente en Python para Linux.

El proyecto busca crear un panel de control personal inspirado en
interfaces futuristas, sistemas HUD y asistentes de inteligencia
artificial.

el sistema incluye una interfaz gráfica futurista personalizable

ULTRON PANEL continúa en desarrollo y puede recibir nuevas funciones
y cambios en futuras versiones.


║ IMÁGENES ║

A continuación se muestran capturas de la interfaz y módulos de ULTRON:

![Ultron - Core y menú principal](images/ultron-1.jpg)
*Figura 1 — Ultron: prompt y nombre del proyecto.*

![Ultron - Menú lateral con módulos](images/ultron-2.jpg)
*Figura 2 — Lista de módulos disponibles.*

![Ultron - Listado de módulos (detalle)](images/ultron-3.jpg)
*Figura 3 — Módulos: Conciencia, Sistema, Preferencias, etc.*

![Ultron - HUD central y métricas del sistema](images/ultron-4.jpg)
*Figura 4 — Núcleo ULTRON con anillos y panel de métricas.*


║ CARACTERÍSTICAS PRINCIPALES ║

• Interfaz gráfica HUD inspirada en sistemas futuristas.

• ULTRON CORE (IA) animado con anillos y efectos visuales.

• Animación en el núcleo central.

• Sistema de módulos.

• Panel de información sobre el sistema.

• Inicio de sesión mediante usuario y contraseña.

• Cambio de usuario desde la interfaz.

• Protección contra nombres de usuario duplicados.

• Sistema de almacenado de contraseñas en su dispositivo.

• Visualización progresiva del texto durante las respuestas.

• Micrófono bloqueado por defecto por privacidad.

• El micrófono únicamente puede activarse mediante interacción
  explícita del usuario con el ULTRON-CORE.

• Sistema de herramientas locales.

• Información de memoria, almacenamiento y batería.

• Posibilidad de abrir aplicaciones y páginas web.

• Temas y colores personalizables.

• Arquitectura preparada para añadir nuevos módulos y funciones.

• Código abierto


║ PRIVACIDAD ║

ULTRON PANEL V2 incluye medidas diseñadas para evitar que el micrófono
permanezca activo sin conocimiento del usuario.

Al iniciar ULTRON:

El micrófono está desactivado por defecto 

La función de CONCIENCIA solamente puede habilitarse mediante una
acción explícita sobre ULTRON CORE.

Al desactivar CONCIENCIA, ULTRON revoca la autorización del micrófono
y detiene los procesos de captura relacionados.

El sistema de usuarios tampoco almacena las contraseñas directamente
en texto plano.

IMPORTANTE:

ULTRON es un proyecto experimental.

Antes de utilizarlo en entornos donde exista información sensible,
configure el sistema de acuerdo con sus necesidades.


║ REQUISITOS ║

ULTRON PANEL V2 está desarrollado principalmente para Linux.

Requisitos generales:

• Python 3
• Git
• Tkinter
• FFmpeg
• PipeWire/PulseAudio compatible
• Conexión a Internet para determinadas funciones
• Dependencias de Python utilizadas por el proyecto

Algunas características pueden depender del hardware y de la
distribución Linux utilizada.


║ COMPATIBILIDAD ║

Sistema principal:

✓ Linux

ULTRON PANEL ha sido desarrollado y probado pensando principalmente
en entornos Linux.

Otros sistemas operativos pueden requerir modificaciones.

Windows:

La interfaz gráfica podría ejecutarse parcialmente, pero diferentes
herramientas utilizan comandos, dispositivos, rutas y sistemas de
audio propios de Linux.

Por este motivo, actualmente no se garantiza el funcionamiento
completo en Windows.


║ INSTALACIÓN ║

Clona ULTRON PANEL V2:

git clone https://github.com/NATH-DEVcode/ULTRON-PANEL-V2.git

Entra al proyecto:

cd ULTRON-PANEL-V2

║ ENTORNO VIRTUAL ║

Se recomienda utilizar un entorno virtual de Python.

Crear el entorno:

python3 -m venv venv

Activarlo:

source venv/bin/activate

Si python3-venv no está instalado:

sudo apt update
sudo apt install python3-venv


║ DEPENDENCIAS ║

Si el repositorio contiene requirements.txt:

pip install -r requirements.txt

Algunas funciones relacionadas con audio pueden necesitar FFmpeg:

sudo apt install ffmpeg

Dependiendo de la distribución utilizada, pueden ser necesarios
paquetes adicionales.



║ EJECUCIÓN ║

Con el entorno virtual activado, ejecuta la interfaz principal según
la estructura instalada del proyecto.

Por ejemplo:

python3 gui/ultron.py

Si se configura el launcher de ULTRON, también puede iniciarse con:

ultron


║ PRIMER INICIO ║

Durante el primer inicio:

1. ULTRON mostrará el sistema de autenticación.

2. Cree un usuario.

3. Configure una contraseña.

4. Opcionalmente active:

   "Recordarme en este equipo"

5. Después del inicio de sesión aparecerá ULTRON CORE.

La sesión recordada utiliza un token local para evitar almacenar
directamente la contraseña.


║ ULTRON CORE ║

ULTRON CORE es el elemento central de la interfaz.

Además de funcionar como elemento visual, permite controlar el estado
de CONCIENCIA.

Los estados visuales pueden cambiar dependiendo de si ULTRON está:

IDLE
LISTENING
THINKING
SPEAKING


║ CONCIENCIA ║

CONCIENCIA permite interactuar mediante voz con ULTRON.

Por razones de privacidad permanece desactivada inicialmente.

Para activarla:

Presione ULTRON CORE.

Para desactivarla:

Presione nuevamente ULTRON CORE.

Cuando está desactivada, el sistema bloquea la captura del micrófono.


║ USUARIOS ║

ULTRON PANEL V2 incluye administración local de usuarios.

Cada usuario dispone de autenticación propia.

El sistema permite:

• Crear usuarios.
• Iniciar sesión.
• Recordar una sesión.
• Cambiar de usuario.
• Evitar nombres duplicados.

Desde la interfaz principal puede utilizarse el icono de usuario para
cambiar de cuenta sin necesidad de cerrar completamente ULTRON.


║ MÓDULOS ║

La arquitectura modular permite incorporar herramientas independientes
dentro del panel.

Entre las categorías del proyecto pueden existir módulos relacionados
con:

• Conciencia
• Gestión
• Sistema
• Red
• Seguridad
• Diagnóstico
• Preferencias
• Estado
• Chat

La disponibilidad exacta puede cambiar conforme ULTRON continúe
desarrollándose.


║ PERSONALIZACIÓN ║

ULTRON PANEL está diseñado para poder modificarse.

Puedes personalizar:

• Colores.
• Temas.

Antes de realizar modificaciones importantes se recomienda crear una
copia de seguridad o utilizar Git para poder regresar a una versión
anterior.




ULTRON PANEL — UHD CORE V2



╔══════════════════════════════════════════════════════╗
║                  CREADO POR                         ║
║                 NATH-DEVcode                        ║
╚══════════════════════════════════════════════════════╝

Proyecto desarrollado principalmente con Python.

ULTRON PANEL V2 CORE-UI 
