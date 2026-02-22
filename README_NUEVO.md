# Room Designer 🏠

**Diseñador de espacios (cocinas y dormitorios) por línea de comandos con visualización en imágenes**

Un programa práctico y simple para diseñar habitaciones con medidas exactas, usando comandos de texto. Genera visualizaciones profesionales en PNG y exporta a 3D.

## ✨ Características

- 🎯 **Diseño por comandos**: Rápido y preciso, sin interfaces complicadas
- 📏 **Medidas exactas**: Todo en metros, con precisión decimal
- 🖼️ **Visualizaciones PNG**: Imágenes de alta calidad con código de colores
- 🎨 **Vista en planta**: Diseño desde arriba con etiquetas y medidas
- 📐 **Vista de elevación**: Vista lateral para ver alturas
- 🎲 **Vista 3D isométrica**: Perspectiva tridimensional realista
- 🛏️ **Elementos de dormitorio**: Camas, cuchetas, roperos, mesas de luz, mesas
- 🍳 **Elementos de cocina**: Heladeras, cocinas, piletas, alacenas, mesadas
- 📦 **Exportación STL**: Para visualizar en 3D o imprimir
- 📥 **Importación STL**: Agrega tus propios muebles personalizados
- 💾 **Guardar/Cargar**: Diseños en formato JSON

## 🚀 Inicio Rápido

### Instalación

```bash
# Requiere Python 3 con matplotlib
pip install matplotlib pillow

# Hacer ejecutable
chmod +x room_designer.py
```

### Uso Básico

```bash
# Modo interactivo
./room_designer.py

# En el programa:
>>> new 4 5 2.8              # Crear espacio de 4m x 5m x 2.8m
>>> add_bed 0.5 1.0          # Agregar cama en posición (0.5, 1.0)
>>> add_wardrobe 0 0         # Agregar ropero en esquina
>>> list                     # Ver todos los objetos
>>> plan_view                # Generar vista en planta (PNG)
>>> side_view                # Generar vista de elevación (PNG)
>>> view_3d                  # Generar vista isométrica 3D (PNG)
>>> export_stl mi_cuarto.stl # Exportar a 3D
>>> save mi_diseno.json      # Guardar diseño
>>> exit                     # Salir
```

## 🎨 Código de Colores

Cada tipo de mueble tiene un color distintivo en las visualizaciones:

| Elemento | Color | Uso |
|----------|-------|-----|
| 🛏️ Cama | Rosa claro | Camas individuales/matrimoniales |
| 🛏️ Cucheta | Rosa oscuro | Camas doble altura |
| 🚪 Ropero | Marrón | Armarios y roperos |
| 🪑 Mesa de luz | Marrón claro | Mesitas de noche |
| 🪑 Mesa | Beige | Escritorios, mesas |
| ❄️ Heladera | Azul claro | Refrigeradores |
| 🔥 Cocina | Rojo | Hornallas, anafes |
| 💧 Pileta | Azul | Lavaplatos |
| 📦 Alacena | Marrón medio | Muebles de guardado |
| 🔲 Mesada | Trigo | Superficies de trabajo |

## 📖 Documentación

### Archivos Incluidos

- **`room_designer.py`** - Programa principal con interfaz interactiva
- **`ejemplo_uso.py`** - Script con ejemplos completos de dormitorios y cocinas
- **`README.md`** - Este archivo
- **`MANUAL_DE_USO.md`** - Manual completo con todos los comandos y ejemplos
- **`INICIO_RAPIDO.md`** - Tutorial paso a paso para empezar
- **`REFERENCIA_RAPIDA.txt`** - Hoja de referencia de comandos
- **`comandos_ejemplo.txt`** - Comandos listos para copiar y pegar

### Comandos Principales

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `new` | Crear nuevo espacio | `new 4 5 2.8` |
| `add_bed` | Agregar cama | `add_bed 0.5 1.0` |
| `add_wardrobe` | Agregar ropero | `add_wardrobe 0 0` |
| `add_fridge` | Agregar heladera | `add_fridge 0 0` |
| `move` | Mover objeto | `move cama 1.5 2.0 0` |
| `rotate` | Rotar 90° | `rotate ropero` |
| `list` | Listar objetos | `list` |
| `plan_view` | Vista en planta PNG | `plan_view planta.png` |
| `side_view` | Vista lateral PNG | `side_view elevacion.png` |
| `view_3d` | Vista isométrica 3D PNG | `view_3d vista3d.png` |
| `export_stl` | Exportar a STL | `export_stl cuarto.stl` |
| `save` | Guardar diseño | `save diseno.json` |
| `help` | Ver ayuda | `help` |

Ver **MANUAL_DE_USO.md** para documentación completa.

## 🎓 Ejemplos

### Ejemplo 1: Dormitorio Simple

```bash
>>> new 3.5 4 2.8
>>> add_bed 0.5 0.5 0 1.4 1.9 cama
>>> add_wardrobe 0 3.0 0 2.0 0.6 2.0 ropero
>>> add_nightstand 2.0 0.5 0 0.5 0.4 mesa
>>> plan_view dormitorio_planta.png
>>> view_3d dormitorio_3d.png
>>> export_stl dormitorio.stl
```

### Ejemplo 2: Cocina en L

```bash
>>> new 3.5 4 2.8
>>> add_fridge 0 0 0 0.7 0.7 1.8 heladera
>>> add_counter 0.8 0 0 2.7 0.6 mesada1
>>> add_counter 0 0.8 0 0.6 2.0 mesada2
>>> add_sink 2.0 0 0.9 0.8 0.6 pileta
>>> add_stove 0.8 0 0.9 0.6 0.6 cocina
>>> plan_view cocina_planta.png
>>> view_3d cocina_3d.png
>>> export_stl cocina.stl
```

### Ejemplo 3: Cuarto con Cuchetas

```bash
>>> new 3.5 4.5 2.8
>>> add_bunk_bed 0.2 0.5 0 1.0 2.0 cucheta1
>>> add_bunk_bed 0.2 2.8 0 1.0 2.0 cucheta2
>>> add_wardrobe 1.5 0.5 0 1.8 0.6 2.0 ropero
>>> add_table 1.5 3.2 0 1.5 0.7 escritorio
>>> plan_view cuarto_planta.png
>>> view_3d cuarto_3d.png
>>> export_stl cuarto_ninos.stl
```

## 🖼️ Tipos de Visualización

### 1. Vista en Planta (`plan_view`)
- Vista desde arriba (como un plano arquitectónico)
- Muestra la distribución de todos los muebles
- Incluye nombres y dimensiones de cada objeto
- Grid de referencia en metros
- Leyenda de colores
- **Salida**: Archivo PNG de alta resolución (300 DPI)

### 2. Vista de Elevación (`side_view`)
- Vista lateral del espacio
- Muestra alturas de los muebles
- Útil para verificar que todo entre verticalmente
- **Salida**: Archivo PNG de alta resolución (300 DPI)

### 3. Vista 3D Isométrica (`view_3d`)
- Perspectiva tridimensional
- Muestra profundidad, ancho y altura simultáneamente
- Renderizado con caras sombreadas para mayor realismo
- **Salida**: Archivo PNG de alta resolución (300 DPI)

## 🛠️ Elementos Disponibles

### Dormitorio
- **Camas** (`add_bed`): Simples, individuales, matrimoniales
- **Cuchetas** (`add_bunk_bed`): Camas doble altura
- **Roperos** (`add_wardrobe`): Varios tamaños
- **Mesas de luz** (`add_nightstand`)
- **Mesas** (`add_table`): Escritorios, veladores

### Cocina
- **Heladeras** (`add_fridge`)
- **Cocinas** (`add_stove`): Hornallas, anafes
- **Piletas** (`add_sink`): Simples o dobles
- **Alacenas** (`add_cabinet`): Muebles de guardado
- **Mesadas** (`add_counter`): Superficies de trabajo

## 📐 Sistema de Coordenadas

```
        Y (largo/profundidad)
        ↑
        |
        |
        +-----→ X (ancho)
       /
      /
     ↓
    Z (altura)
```

- **Origen (0,0,0)**: Esquina inferior frontal izquierda
- **Unidades**: Metros
- **Posición**: Esquina inferior izquierda de cada objeto

## 📁 Formatos de Archivo

| Formato | Extensión | Uso |
|---------|-----------|-----|
| PNG | `.png` | Visualizaciones 2D y 3D |
| STL | `.stl` | Modelos 3D (MeshLab, Blender) |
| JSON | `.json` | Diseños editables |

## 🎨 Visualización de Archivos

### Imágenes PNG
Las imágenes generadas se pueden abrir con cualquier visor de imágenes:
- Windows: Fotos, Paint
- Mac: Vista Previa
- Linux: Eye of GNOME, gThumb
- Cualquier navegador web

### Archivos STL
Los archivos STL generados se pueden abrir con:
- **[MeshLab](https://www.meshlab.net/)** (gratuito, simple)
- **[Blender](https://www.blender.org/)** (gratuito, profesional)
- **[FreeCAD](https://www.freecad.org/)** (gratuito, CAD)
- Cualquier visor STL online

## 💡 Consejos

1. **Mide antes**: Ten las medidas exactas de tus muebles reales
2. **Empieza simple**: Usa primero los valores por defecto
3. **Genera vistas frecuentemente**: `plan_view`, `view_3d` para visualizar mientras diseñas
4. **Guarda versiones**: `save version_1.json`, `save version_2.json`
5. **Usa nombres descriptivos**: `cama_principal` mejor que `c1`
6. **Combina vistas**: Usa planta + 3D para entender mejor el espacio

## 🔧 Comandos Avanzados

### Rotación
```bash
>>> add_wardrobe 0 0 0 1.8 0.6 2.0 ropero
>>> rotate ropero  # Ahora mide 0.6m x 1.8m
```

### Importar STL Personalizado
```bash
>>> import_stl silla.stl silla_comedor 1.0 2.0 0
```

### Múltiples Visualizaciones
```bash
>>> plan_view planta.png
>>> side_view elevacion.png
>>> view_3d perspectiva.png
# ¡Tres vistas diferentes del mismo diseño!
```

## 📝 Ejemplos de Uso Programático

```python
from room_designer import RoomDesigner

# Crear espacio
cuarto = RoomDesigner(width=4.0, length=5.0, height=2.8)

# Agregar muebles
cuarto.add_bed(0.5, 1.0, 0, 1.4, 2.0, "cama_matrimonial")
cuarto.add_wardrobe(0, 0, 0, 1.5, 0.6, 2.0, "ropero")
cuarto.add_nightstand(2.0, 1.0, 0, 0.5, 0.4, "mesa_luz")

# Generar visualizaciones
cuarto.generate_plan_view("planta.png")
cuarto.generate_side_view("elevacion.png")
cuarto.generate_3d_view("vista3d.png")

# Exportar
cuarto.export_stl("dormitorio.stl")
cuarto.save_design("dormitorio.json")
```

Ver **`ejemplo_uso.py`** para ejemplos completos.

## ❓ Preguntas Frecuentes

**P: ¿Qué formato tienen las visualizaciones?**
R: PNG de alta resolución (300 DPI), perfectas para imprimir o compartir.

**P: ¿Puedo cambiar los colores?**
R: Sí, editando el diccionario `colors` en el código fuente.

**P: ¿Las imágenes incluyen medidas?**
R: Sí, la vista en planta muestra dimensiones de cada objeto y grid de referencia.

**P: ¿Puedo generar todas las vistas de una vez?**
R: Sí, ejecuta `plan_view`, `side_view` y `view_3d` en secuencia.

**P: ¿Necesito software especial para ver las imágenes?**
R: No, cualquier visor de imágenes o navegador funciona.

## 🐛 Solución de Problemas

**Error: "No module named 'matplotlib'"**
```bash
pip install matplotlib pillow
```

**Las imágenes se ven pequeñas**
- Son de alta resolución (300 DPI)
- Ábrelas con un visor de imágenes para ver el detalle completo

**Los objetos se superponen en la imagen**
```bash
>>> list  # Ver posiciones exactas
>>> move objeto 1 1 0  # Ajustar
```

## 🤝 Contribuciones

Ideas para mejoras:
- Más tipos de muebles
- Texturas personalizadas
- Exportación a otros formatos de imagen (SVG, PDF)
- Renderizado con sombras

## 📄 Licencia

Código libre para uso personal y educativo.

## 🙏 Créditos

Desarrollado para facilitar el diseño de espacios domésticos de forma práctica y visual.

---

**¿Necesitas ayuda?** Consulta el **MANUAL_DE_USO.md** completo o ejecuta `help` dentro del programa.

**¡Feliz diseño!** 🏠✨
