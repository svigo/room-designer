# 🔷 GUÍA DE FORMAS IRREGULARES - Room Designer

## Nueva Funcionalidad: Diseños No Rectangulares

Ahora puedes crear **habitaciones y muebles con formas irregulares** usando vértices personalizados. Perfecto para espacios en L, U, o cualquier forma con ángulos rectos.

---

## 📐 Conceptos Básicos

### ¿Qué son los vértices?

Los vértices son puntos (x, y) que definen las esquinas de tu forma. El programa conecta estos puntos en orden para crear el contorno.

**Formato:** `x,y` (sin espacios)

**Ejemplo de forma en L:**
```
(0,0) -------- (4,0)
  |               |
  |               | (4,3)
  |        (2,3) -+
  |          |
  |          | (2,5)
  +----------+
(0,5)
```

Vértices: `0,0` `4,0` `4,3` `2,3` `2,5` `0,5`

---

## 🏠 Crear Habitaciones Irregulares

### Comando: `new_custom`

```bash
new_custom <altura> <x1,y1> <x2,y2> <x3,y3> ...
```

**Parámetros:**
- `altura`: Altura del techo en metros
- `x1,y1 x2,y2 ...`: Vértices de la planta (mínimo 3)

### Ejemplo 1: Habitación en L

```bash
>>> new_custom 2.8 0,0 4,0 4,3 2,3 2,5 0,5
```

Esto crea:
- Brazo horizontal: 4m × 3m
- Brazo vertical: 2m × 5m
- Altura: 2.8m

### Ejemplo 2: Habitación en T

```bash
>>> new_custom 2.8 0,2 4,2 4,3 2,3 2,5 1,5 1,3 0,3
```

### Ejemplo 3: Habitación en U

```bash
>>> new_custom 2.8 0,0 3,0 3,1 2,1 2,3 1,3 1,1 0,1
```

---

## 🪑 Crear Muebles Irregulares

### Método 1: Comando `add_custom`

Crea **cualquier mueble** con forma personalizada.

```bash
add_custom <nombre> <z> <altura> <x1,y1> <x2,y2> ...
```

**Parámetros:**
- `nombre`: Identificador del mueble
- `z`: Altura desde el piso (usualmente 0 o 0.9)
- `altura`: Altura del mueble
- `x1,y1 ...`: Vértices de la base

### Ejemplos:

#### Escritorio en U
```bash
>>> add_custom escritorio_U 0 0.75 0.5,0.5 3.5,0.5 3.5,1.1 2.9,1.1 2.9,3.0 1.1,3.0 1.1,1.1 0.5,1.1
```

#### Isla de cocina
```bash
>>> add_custom isla 0 0.9 1.0,1.5 2.5,1.5 2.5,2.5 1.0,2.5
```

#### Mesada en Z
```bash
>>> add_custom mesada_Z 0 0.9 0,0 2,0 2,0.6 1,0.6 1,1.5 2,1.5 2,2.1 0,2.1 0,1.5 1,1.5 1,0.6 0,0.6
```

### Método 2: Comando `add_L_counter`

Atajo para **mesadas en forma de L**.

```bash
add_L_counter <x> <y> [z] [ancho1] [ancho2] [prof] [nombre]
```

**Parámetros:**
- `x, y`: Posición de la esquina interna de la L
- `ancho1`: Largo del brazo horizontal
- `ancho2`: Largo del brazo vertical
- `prof`: Profundidad de la mesada (default: 0.6m)

### Ejemplo:

```bash
>>> add_L_counter 0.8 0 0 2.5 2.0 0.6 mesada_cocina
```

Crea una mesada en L de:
- Brazo horizontal: 2.5m
- Brazo vertical: 2.0m
- Profundidad: 0.6m

---

## 🎯 Reglas Importantes

### ✅ Hacer:
1. **Definir vértices en orden** (sentido horario o antihorario)
2. **Usar solo ángulos rectos** (90°)
3. **Mínimo 3 vértices** para cualquier forma
4. **Cerrar la forma** (el último vértice conecta con el primero automáticamente)

### ❌ Evitar:
1. ~~Vértices desordenados~~ → Formas raras
2. ~~Ángulos no rectos~~ → El programa no los soporta aún
3. ~~Formas que se cruzan a sí mismas~~ → Problemas en renderizado
4. ~~Muy pocos vértices~~ → Se necesitan al menos 3

---

## 💡 Casos de Uso Reales

### 1. Cocina con Península

```bash
>>> new 4 5 2.8
>>> add_fridge 0 0 0 0.7 0.7 1.8 heladera

# Mesada en L con península
>>> add_custom mesada_peninsula 0 0.9 0.8,0 3.5,0 3.5,0.6 1.8,0.6 1.8,2.5 1.2,2.5 1.2,0.6 0.8,0.6

>>> add_stove 0.8 0 0.9 0.6 0.6 cocina
>>> add_sink 2.5 0 0.9 0.8 0.6 pileta
```

### 2. Dormitorio con Walking Closet

```bash
# Habitación principal en L (con espacio para closet)
>>> new_custom 2.8 0,0 5,0 5,4 3,4 3,5 0,5

>>> add_bed 0.5 0.5 0 1.6 2.0 cama_queen
>>> add_wardrobe 3.2 4.2 0 1.6 0.6 2.2 closet
```

### 3. Oficina en Casa con Escritorio Integrado

```bash
>>> new 4 3.5 2.8

# Escritorio empotrado en forma de L
>>> add_custom escritorio_empotrado 0 0.75 0,0.5 2.5,0.5 2.5,1.1 0.6,1.1 0.6,2.5 0,2.5

>>> add_wardrobe 2.7 0.5 0 1.2 0.6 2.0 biblioteca
```

### 4. Baño con Mueble de Vanitory en L

```bash
>>> new 2.5 3 2.8

# Vanitory en L
>>> add_custom vanitory 0 0.9 0,0 1.8,0 1.8,0.6 0.6,0.6 0.6,1.2 0,1.2

>>> add_sink 0.8 0.1 0.9 0.5 0.4 pileta_bano
```

---

## 🔧 Modo Programático

### Python API

```python
from room_designer import RoomDesigner

# Habitación irregular
vertices_habitacion = [
    (0, 0),
    (4, 0),
    (4, 3),
    (2, 3),
    (2, 5),
    (0, 5)
]

cuarto = RoomDesigner(vertices=vertices_habitacion, height=2.8)

# Mueble irregular
vertices_escritorio = [
    (0.5, 0.5),
    (3.5, 0.5),
    (3.5, 1.1),
    (2.9, 1.1),
    (2.9, 3.0),
    (1.1, 3.0),
    (1.1, 1.1),
    (0.5, 1.1)
]

cuarto.add_custom_furniture(
    vertices=vertices_escritorio,
    z=0,
    height=0.75,
    name='escritorio_U',
    obj_type='custom'
)

# Atajo para mesada en L
cuarto.add_L_counter(x=0, y=0, z=0, width1=2.5, width2=2.0, depth=0.6, name='mesada_L')

# Generar visualizaciones
cuarto.generate_plan_view('mi_cuarto.png')
cuarto.generate_3d_view('mi_cuarto_3d.png')
cuarto.export_stl('mi_cuarto.stl')
```

---

## 📊 Visualización

Las formas irregulares se renderizan correctamente en:

✅ **Vista en Planta** - Polígonos con bordes definidos
✅ **Vista 3D Isométrica** - Extrusión vertical del polígono
✅ **Exportación STL** - Mallas trianguladas correctamente

---

## 🎨 Tips de Diseño

### 1. Planifica en papel primero

Dibuja tu forma en papel cuadriculado y anota las coordenadas (x, y) de cada vértice.

### 2. Empieza simple

Comienza con formas simples (L, T, U) antes de intentar formas más complejas.

### 3. Verifica con plan_view

Genera la vista en planta frecuentemente para verificar que la forma quedó como esperabas:

```bash
>>> plan_view temp.png
```

### 4. Usa el atajo para L

Si solo necesitas una forma en L, `add_L_counter` es más rápido que `add_custom`.

### 5. Combina formas

Puedes crear formas complejas usando varios muebles rectangulares y personalizados juntos.

---

## 🐛 Solución de Problemas

### Problema: "Se necesitan al menos 3 vértices"

**Solución:** Agrega más puntos. Mínimo 3 vértices para formar una figura.

```bash
# ❌ Mal (solo 2 puntos)
>>> add_custom mesa 0 0.75 0,0 1,1

# ✅ Bien (4 puntos para rectángulo)
>>> add_custom mesa 0 0.75 0,0 1,0 1,1 0,1
```

### Problema: La forma se ve rara en la visualización

**Solución:** Los vértices deben estar en orden (horario o antihorario). Verifica el orden.

```bash
# ❌ Mal (vértices desordenados)
>>> add_custom mesa 0 0.75 0,0 1,1 1,0 0,1

# ✅ Bien (orden correcto)
>>> add_custom mesa 0 0.75 0,0 1,0 1,1 0,1
```

### Problema: El mueble no aparece en la vista 3D

**Solución:** Asegúrate de que los vértices estén dentro de los límites de la habitación.

---

## 📝 Ejemplos Paso a Paso

### Crear una Cocina Completa en L

```bash
# 1. Crear espacio rectangular estándar
>>> new 3.5 4 2.8

# 2. Agregar heladera en esquina
>>> add_fridge 0 0 0 0.7 0.7 1.8 heladera

# 3. Crear mesada en L
>>> add_L_counter 0.8 0 0 2.5 2.0 0.6 mesada_principal

# 4. Agregar electrodomésticos sobre la mesada
>>> add_stove 0.8 0 0.9 0.6 0.6 cocina
>>> add_sink 2.0 0 0.9 0.8 0.6 pileta

# 5. Agregar alacenas superiores (también en L si quieres)
>>> add_L_counter 0.8 0 1.9 2.5 2.0 0.35 alacenas_sup

# 6. Visualizar
>>> plan_view cocina_L.png
>>> view_3d cocina_L_3d.png
>>> export_stl cocina_L.stl
```

---

## 🎓 Ejercicios

### Ejercicio 1: Habitación Básica en L

Crea una habitación en L de:
- Brazo largo: 5m × 3m
- Brazo corto: 2m × 2m

<details>
<summary>Ver solución</summary>

```bash
>>> new_custom 2.8 0,0 5,0 5,3 2,3 2,5 0,5
```
</details>

### Ejercicio 2: Isla de Cocina Rectangular

Crea una isla rectangular de 1.5m × 1.0m en el centro de una cocina de 4m × 4m.

<details>
<summary>Ver solución</summary>

```bash
>>> new 4 4 2.8
>>> add_custom isla 0 0.9 1.25,1.5 2.75,1.5 2.75,2.5 1.25,2.5
```
</details>

### Ejercicio 3: Escritorio Esquinero

Crea un escritorio en L en la esquina de un cuarto de 3m × 3m.

<details>
<summary>Ver solución</summary>

```bash
>>> new 3 3 2.8
>>> add_L_counter 0 0 0 1.5 1.5 0.6 escritorio_esquinero
```
</details>

---

## 🚀 ¡Próximos Pasos!

Ahora que dominas las formas irregulares, puedes:

1. **Diseñar espacios reales** con formas no estándar
2. **Crear muebles personalizados** que se ajusten perfectamente
3. **Experimentar** con diferentes configuraciones
4. **Compartir** tus diseños exportando a STL o PNG

**¡Feliz diseño!** 🏠✨
