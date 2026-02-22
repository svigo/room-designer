# 🚀 GUÍA RÁPIDA - Room Designer (Español)

## ⚡ Visualización en Tiempo Real

### Activar Visualización Automática

```bash
# Ver cambios en vista de planta automáticamente
>>> activar_viz_planta

# Ver cambios en vista lateral automáticamente  
>>> activar_viz_lateral

# Ver cambios en vista 3D automáticamente
>>> activar_viz_3d

# Desactivar visualización
>>> desactivar_viz
```

**¿Cómo funciona?**
Cuando activas la visualización, cada vez que agregues, muevas o modifiques algo, se actualizará la vista automáticamente en una ventana de matplotlib.

---

## 🏠 Crear Espacios

### Espacio Rectangular
```bash
>>> nuevo 4 5 2.8
# 4m de ancho × 5m de largo × 2.8m de alto
```

### Espacio Irregular (L, T, U, etc.)
```bash
>>> nuevo_irregular 2.8 0,0 4,0 4,3 2,3 2,5 0,5
# Altura 2.8m, vértices en formato x,y
```

---

## 🚪 Puertas y Ventanas

### Agregar Puerta

```bash
>>> agregar_puerta <x> <y> [z] [ancho] [dirección] [swing] [nombre]
```

**Direcciones:** `izquierda`, `derecha`, `arriba`, `abajo`  
**Swing:** `adentro`, `afuera`

**Ejemplos:**
```bash
# Puerta que abre hacia la derecha, hacia adentro
>>> agregar_puerta 2 0 0 0.9 derecha adentro entrada

# Puerta que abre hacia la izquierda, hacia afuera
>>> agregar_puerta 0 2.5 0 0.8 izquierda afuera cocina

# Puerta doble
>>> agregar_puerta 1.5 0 0 1.8 derecha adentro principal
```

### Agregar Ventana

```bash
>>> agregar_ventana <x> <y> [z] [ancho] [alto] [nombre]
```

**Ejemplos:**
```bash
# Ventana estándar
>>> agregar_ventana 1 0 1.2 1.5 1.0 ventana_frente

# Ventanal grande
>>> agregar_ventana 0 2 0.5 2.5 2.0 ventanal

# Ventana de baño pequeña
>>> agregar_ventana 1 0 1.8 0.6 0.4 ventana_baño
```

---

## 🛏️ Muebles de Dormitorio

```bash
# Cama
>>> agregar_cama 0.5 1.0 0 1.4 1.9 cama_matrimonial

# Cucheta (litera)
>>> agregar_cucheta 0.5 1.0 0 1.0 2.0 cucheta_chicos

# Ropero
>>> agregar_ropero 0 3.5 0 2.0 0.6 2.2 ropero_principal

# Mesa de luz
>>> agregar_mesa_luz 2.0 0.5 0 0.5 0.4 mesa_izq

# Mesa/Escritorio
>>> agregar_mesa 2.5 1.0 0 1.2 0.8 escritorio
```

---

## 🍳 Elementos de Cocina

```bash
# Heladera
>>> agregar_heladera 0 0 0 0.7 0.7 1.8 heladera

# Cocina/Hornalla
>>> agregar_cocina 0.8 0 0.9 0.6 0.6 cocina

# Pileta
>>> agregar_pileta 2.0 0 0.9 0.8 0.6 pileta

# Alacena/Mueble
>>> agregar_alacena 0.8 0 1.9 2.7 0.35 0.7 alacenas_sup

# Mesada simple
>>> agregar_mesada 0.8 0 0 2.5 0.6 mesada_principal

# Mesada en forma de L
>>> agregar_mesada_L 0.8 0 0 2.5 2.0 0.6 mesada_L
```

---

## 🔷 Muebles Personalizados

### Cualquier Forma
```bash
>>> agregar_personalizado <nombre> <z> <altura> <x1,y1> <x2,y2> ...
```

**Ejemplos:**
```bash
# Isla de cocina rectangular
>>> agregar_personalizado isla 0 0.9 1,1.5 2.5,1.5 2.5,2.5 1,2.5

# Escritorio en U
>>> agregar_personalizado escritorio_U 0 0.75 0.5,0.5 3.5,0.5 3.5,1.1 2.9,1.1 2.9,3.0 1.1,3.0 1.1,1.1 0.5,1.1

# Barra de bar
>>> agregar_personalizado barra 0 1.1 0.5,2.0 3.5,2.0 3.5,2.4 0.5,2.4
```

---

## 🎮 Manipular Objetos

```bash
# Mover un objeto
>>> mover cama 1.0 1.5 0

# Rotar 90 grados
>>> rotar ropero

# Eliminar
>>> eliminar mesa_vieja

# Ver lista de todos los objetos
>>> listar
```

---

## 💾 Guardar y Exportar

```bash
# Guardar diseño (JSON editable)
>>> guardar mi_dormitorio.json

# Cargar diseño
>>> cargar mi_dormitorio.json

# Exportar a 3D (STL)
>>> exportar_stl mi_dormitorio.stl

# Generar vistas PNG (sin visualización en tiempo real)
>>> vista_planta dormitorio_planta.png
>>> vista_lateral dormitorio_elevacion.png
>>> vista_3d dormitorio_3d.png
```

---

## 📋 Flujo de Trabajo Recomendado

### Opción 1: Con Visualización en Tiempo Real

```bash
# 1. Activar visualización
>>> activar_viz_planta

# 2. Crear espacio
>>> nuevo 4 5 2.8

# 3. Agregar elementos (se visualizan automáticamente)
>>> agregar_puerta 2 0 0 0.9 derecha adentro entrada
>>> agregar_cama 0.5 1.0 0 1.4 1.9 cama
>>> agregar_ropero 0 3.5 0 2.0 0.6 2.2 ropero
>>> agregar_ventana 1 0 1.2 1.5 1.0 ventana

# 4. Ajustar si es necesario
>>> mover cama 0.7 1.2 0

# 5. Ver en 3D (cambia la vista)
>>> activar_viz_3d

# 6. Guardar
>>> guardar mi_diseño.json
>>> exportar_stl mi_diseño.stl

# 7. Desactivar visualización
>>> desactivar_viz
```

### Opción 2: Sin Visualización en Tiempo Real

```bash
# 1. Crear espacio
>>> nuevo 4 5 2.8

# 2. Agregar todo
>>> agregar_puerta 2 0 0 0.9 derecha adentro entrada
>>> agregar_cama 0.5 1.0 0 1.4 1.9 cama
>>> agregar_ropero 0 3.5 0 2.0 0.6 2.2 ropero

# 3. Generar vistas cuando quieras
>>> vista_planta planta.png
>>> vista_3d vista3d.png

# 4. Guardar
>>> guardar mi_diseño.json
```

---

## 🎯 Ejemplos Completos

### Dormitorio con Puerta y Ventana

```bash
>>> activar_viz_planta
>>> nuevo 3.5 4 2.8
>>> agregar_puerta 1.5 0 0 0.9 arriba adentro puerta_entrada
>>> agregar_ventana 0 2 1.2 1.5 1.0 ventana_lateral
>>> agregar_cama 0.5 0.5 0 1.4 1.9 cama
>>> agregar_ropero 0 3.0 0 2.0 0.6 2.2 ropero
>>> agregar_mesa_luz 2.0 0.5 0 0.5 0.4 mesa_der
>>> guardar dormitorio.json
>>> exportar_stl dormitorio.stl
```

### Cocina en L con Puerta y Ventanas

```bash
>>> activar_viz_planta
>>> nuevo 3.5 4 2.8
>>> agregar_puerta 0 2 0 0.8 derecha afuera puerta_patio
>>> agregar_ventana 2 0 1.2 1.2 1.0 ventana_frente
>>> agregar_heladera 0 0 0 0.7 0.7 1.8 heladera
>>> agregar_mesada_L 0.8 0 0 2.5 2.0 0.6 mesada_principal
>>> agregar_cocina 0.8 0 0.9 0.6 0.6 cocina
>>> agregar_pileta 2.0 0 0.9 0.8 0.6 pileta
>>> agregar_alacena 0.8 0 1.9 2.5 0.35 0.7 alacenas
>>> guardar cocina.json
```

### Oficina con Escritorio Personalizado

```bash
>>> nuevo 4 4 2.8
>>> agregar_puerta 1.5 0 0 0.9 derecha adentro entrada
>>> agregar_ventana 0 2 1.0 1.8 1.5 ventanal
>>> agregar_personalizado escritorio_L 0 0.75 0.5,0.5 2.5,0.5 2.5,1.1 1.1,1.1 1.1,2.5 0.5,2.5
>>> agregar_ropero 2.7 0.5 0 1.2 0.6 2.0 biblioteca
>>> vista_planta oficina.png
>>> vista_3d oficina_3d.png
```

---

## 💡 Tips para Visualización en Tiempo Real

1. **Usa vista de planta para diseñar** - Es la más clara para ubicar muebles
2. **Cambia a 3D para verificar** - Ver el resultado final en perspectiva
3. **Desactiva la visualización para comandos masivos** - Si vas a agregar muchos objetos seguidos
4. **La ventana se actualiza automáticamente** - No hace falta cerrarla y abrirla

---

## 🚪 Configuraciones Comunes de Puertas

### Puerta de Entrada Principal
```bash
>>> agregar_puerta 2 0 0 0.9 derecha adentro entrada_principal
```

### Puerta al Patio (abre hacia afuera)
```bash
>>> agregar_puerta 1.5 5 0 0.8 arriba afuera puerta_patio
```

### Puerta de Placard
```bash
>>> agregar_puerta 1 0 0 0.7 izquierda adentro placard
```

### Puerta Doble
```bash
>>> agregar_puerta 1 0 0 1.6 derecha adentro puerta_doble
```

---

## ❓ Solución de Problemas

**La visualización no se actualiza**
```bash
>>> desactivar_viz
>>> activar_viz_planta
```

**Comando no reconocido**
- Verifica que esté en español (usa `ayuda` para ver la lista)
- Los parámetros numéricos deben usar punto, no coma: `1.5` no `1,5`
- Los vértices usan coma: `0,0` `1,0` `1,1` `0,1`

**La puerta no aparece o se ve rara**
- Verifica la dirección: `izquierda`, `derecha`, `arriba`, `abajo`
- Verifica el swing: `adentro`, `afuera`
- Asegúrate de que esté contra una pared

---

## 🎨 Código de Colores

- 🛏️ **Cama**: Rosa claro
- 🛏️ **Cucheta**: Rosa oscuro
- 🚪 **Ropero**: Marrón
- 🪑 **Mesa de luz**: Marrón claro
- ❄️ **Heladera**: Azul claro
- 🔥 **Cocina**: Rojo
- 💧 **Pileta**: Azul
- 📦 **Alacena**: Marrón medio
- 🔲 **Mesada**: Trigo/beige
- 🚪 **Puerta**: Tan/marrón claro
- 🪟 **Ventana**: Celeste

---

**¡Feliz diseño!** 🏠✨

Para más detalles, escribe `ayuda` en el programa.
