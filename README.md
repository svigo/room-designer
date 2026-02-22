\# Room Designer



Diseñador de habitaciones 3D con visualización interactiva web.



\## Características



\- Diseño de habitaciones rectangulares e irregulares

\- Muebles personalizables (camas, mesas, cocinas, etc.)

\- Exportación a múltiples formatos:

&nbsp; - \*\*STL\*\* (impresión 3D)

&nbsp; - \*\*OBJ+MTL\*\* (con colores)

&nbsp; - \*\*GLTF\*\* (formato moderno)

&nbsp; - \*\*Visor Web 3D\*\* (recorrido WASD en navegador)

\- Paredes con grosor realista (10cm)

\- Vistas: Planta, Norte, Sur, Este, Oeste

\- Redimensionar objetos con flechas del teclado

\- Etiquetas inteligentes con coordenadas



\##  Uso

```bash

python room\_designer\_gui.py

```



\## Comandos Principales

```bash

n 5 5              # Nueva habitación 5×5m

c 1 1 cama         # Agregar cama

h 0 0 heladera     # Agregar heladera

web cocina         # Exportar visor web 3D

F1                 # Ayuda completa

```



\##  Requisitos



\- Python 3.8+

\- matplotlib

\- numpy

```bash

pip install -r requirements.txt

```



\## Documentación



Ver archivos `.md` para guías detalladas de cada funcionalidad.



\##  Visor Web



El comando `web` genera un archivo HTML que puedes abrir en cualquier navegador para recorrer tu diseño en 3D con controles WASD.



\## Autor



Santiago Vigo

