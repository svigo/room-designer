# 🔍 Vistas Laterales con Muebles - ACTUALIZADO

## ✅ Mejora Implementada

**Antes**: Las vistas laterales (F3-F6) solo mostraban las paredes
**Ahora**: Las vistas laterales muestran **paredes Y muebles**

---

## 📐 Cómo Funcionan las Vistas

### Vista Norte (F3) - Frente
Muestra lo que verías mirando desde el norte hacia el sur
- **Eje horizontal**: X (izquierda a derecha)
- **Eje vertical**: Z (altura)
- **Muebles visibles**: Los que están cerca del frente (Y < 1.5m)

```
     Techo
    ┌────────┐
    │        │  ← Paredes
    │  🛏️📦  │  ← Muebles del frente
    └────────┘
     Piso
```

### Vista Sur (F4) - Fondo
Muestra lo que verías mirando desde el sur hacia el norte
- **Muebles visibles**: Los que están cerca del fondo (Y > length-1.5m)

### Vista Este (F5) - Derecha
Muestra lo que verías mirando desde el este hacia el oeste
- **Eje horizontal**: Y (frente a fondo)
- **Eje vertical**: Z (altura)
- **Muebles visibles**: Los que están a la derecha (X > width-1.5m)

### Vista Oeste (F6) - Izquierda
Muestra lo que verías mirando desde el oeste hacia el este
- **Muebles visibles**: Los que están a la izquierda (X < 1.5m)

---

## 🎨 Características

### Muebles Incluyen:
- ✅ **Forma**: Rectángulo proporcional al tamaño real
- ✅ **Color**: El mismo que en la vista de planta
- ✅ **Nombre**: Etiqueta con el nombre del mueble
- ✅ **Posición**: Ubicación correcta en la pared

### Información Visual:
- **Altura correcta**: Los muebles se dibujan a su altura real (Z)
- **Ancho real**: Se respetan las dimensiones
- **Colores personalizados**: Si cambiaste el color, se refleja

---

## 📖 Ejemplo de Uso

```bash
python3 room_designer_gui.py

>>> n 5 5
>>> c 1 1 cama
>>> h 0 0 heladera

# Vista Planta (F2)
[Ves todo desde arriba]

# Vista Norte (F3)
[Ves la heladera porque está en Y=0, cerca del frente]

# Vista Sur (F4)
[No ves nada porque no hay muebles en el fondo]

# Vista Oeste (F6)
[Ves tanto la cama como la heladera porque ambas están en X < 1.5]

# Vista Este (F5)
[No ves nada porque no hay muebles a la derecha]
```

---

## 🎯 Uso Práctico

### Para Ver un Mueble en Vista Lateral:

**Ejemplo 1: Heladera en esquina**
```bash
>>> n 4 3.5
>>> h 0 0 0 0.7 0.7 1.8 heladera

# F3 (Norte): ✅ Se ve (Y=0, frente)
# F6 (Oeste): ✅ Se ve (X=0, izquierda)
# F4 (Sur): ❌ No se ve (está en el frente, no en el fondo)
# F5 (Este): ❌ No se ve (está a la izquierda, no a la derecha)
```

**Ejemplo 2: Cama en el centro**
```bash
>>> n 5 5
>>> c 2 2 cama

# F3 (Norte): ❌ No se ve (Y=2, no está lo suficientemente al frente)
# F4 (Sur): ❌ No se ve (Y=2, no está lo suficientemente al fondo)
# F5 (Este): ❌ No se ve (X=2, no está lo suficientemente a la derecha)
# F6 (Oeste): ❌ No se ve (X=2, no está lo suficientemente a la izquierda)
```

### Reglas de Visibilidad:

| Vista | Condición para Ver Mueble |
|-------|---------------------------|
| Norte (F3) | Y < 1.5m |
| Sur (F4) | Y > (length - 1.5m) |
| Este (F5) | X > (width - 1.5m) |
| Oeste (F6) | X < 1.5m |

**Nota**: Si quieres ver un mueble que está en el centro, colócalo más cerca de una pared o usa la vista de planta.

---

## 💡 Tips

### Ver Altura de Muebles
Las vistas laterales son perfectas para:
- Verificar que una heladera no toca el techo
- Ver si una ventana está a la altura correcta
- Comprobar que una puerta tiene espacio suficiente
- Visualizar estantes a diferentes alturas

### Ejemplo: Verificar Alturas
```bash
>>> n 3.5 3.5 2.67
>>> h 0 0 0 0.7 0.7 1.8 heladera
>>> agregar_ventana 1 0 1.2 1.3 0.9 ventana

# F3 (Vista Norte)
[Ves la heladera (1.8m alto) y la ventana (en Z=1.2m)]
[Puedes verificar que no se solapan]
```

---

## 🔧 Mejoras Técnicas

### Proyección Correcta
Cada vista proyecta los muebles en el plano correcto:

**Norte/Sur**: Proyección en plano XZ (ancho × altura)
```python
# Se dibuja: (obj_x, obj_z, obj_width, obj_height)
rect = Rectangle((obj_x, obj_z), obj_w, obj_h, ...)
```

**Este/Oeste**: Proyección en plano YZ (profundidad × altura)
```python
# Se dibuja: (obj_y, obj_z, obj_depth, obj_height)
rect = Rectangle((obj_y, obj_z), obj_d, obj_h, ...)
```

### Colores Consistentes
Los colores personalizados y por defecto se mantienen en todas las vistas:
```python
color = self.colores_personalizados.get(obj['name'], 
        colors_default.get(obj['type'], '#CCC'))
```

---

## 📊 Comparación

### Antes:
```
Vista Norte (F3):
┌────────────┐
│            │  ← Solo paredes vacías
│            │
└────────────┘
```

### Ahora:
```
Vista Norte (F3):
┌────────────┐
│            │  ← Paredes
│ 🚪  🪟 🛏️ │  ← ¡Muebles visibles!
└────────────┘
  puerta ventana cama
```

---

## ✅ Checklist

Para que las vistas laterales funcionen correctamente:

- [ ] Archivos actualizados (`room_designer_gui.py` v3.2)
- [ ] Muebles colocados cerca de las paredes (no en el centro)
- [ ] Altura de muebles configurada correctamente
- [ ] Presionar F3/F4/F5/F6 para cambiar vista

---

## 🎨 Ejemplo Visual Completo

```bash
# Crear cocina con elementos en todas las paredes
>>> n 3.5 3.5 2.67

# Pared norte (Y=0)
>>> h 0 0 0 0.7 0.7 1.8 heladera
>>> co 0.8 0 0 0.6 0.6 cocina

# Pared este (X=3.5)
>>> agregar_mueble 2.8 1 0 0.6 0.5 2.0 alacena estante

# Ahora prueba las vistas:
>>> [F3] → Ves heladera y cocina (pared norte)
>>> [F5] → Ves alacena (pared este)
>>> [F2] → Ves todo desde arriba
```

---

**¡Ahora puedes ver tus muebles desde todos los ángulos!** 👁️
