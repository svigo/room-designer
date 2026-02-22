# 🎉 Room Designer v3.2 - TODAS LAS MEJORAS

## ✅ Cambios Implementados

### 1. **STL con Altura Correcta** ✅
- Ahora exporta **PAREDES** con la altura real del cuarto
- Antes: solo piso y muebles
- Ahora: piso + 4 paredes + muebles
- La altura se respeta: si creas `nuevo 5 5 2.8`, el STL tendrá 2.8m de alto

### 2. **Ayuda Contextual Automática** ✅
```bash
# Escribe SOLO el comando sin parámetros:
>>> agregar_heladera

# Respuesta automática:
ℹ️  agregar_heladera <x> <y> [z] [w] [d] [h] [nombre]
  Ej: agregar_heladera 0 0 0 0.7 0.7 1.8 heladera

# Otro ejemplo:
>>> agregar_puerta

# Respuesta:
ℹ️  agregar_puerta <x> <y> [z] [ancho] [orient] [bisagra] [swing] [nombre]
  orient: horizontal|vertical
  bisagra h: izquierda|derecha
  bisagra v: arriba|abajo
  swing h: norte|sur, swing v: este|oeste
  Ej: agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada
```

### 3. **Cambiar Nombre y Color** ✅
```bash
# Renombrar objeto
>>> renombrar cama cama_principal
✓ 'cama' → 'cama_principal'

# Cambiar color (abre selector)
>>> color cama
[Se abre diálogo de color]
✓ Color aplicado a 'cama'

# O especificar color directo
>>> color mesa rojo
✓ Color 'rojo' para 'mesa'

# Colores válidos: rojo, azul, verde, amarillo, 
# naranja, morado, rosa, negro, blanco, gris
# O código hex: #FF5733
```

### 4. **Coordenadas Visibles** ✅
Ahora TODOS los objetos muestran:
```
nombre_objeto
(x, y)
```
Directamente en la visualización de planta.

Ejemplo visual:
```
┌─────────────────────┐
│  heladera           │
│  (0.00, 0.00)       │
├─────────────────────┤
│  cama_principal     │
│  (1.50, 2.00)       │
└─────────────────────┘
```

### 5. **Dimensiones Personalizables Cocina** ✅

**Antes (dimensiones fijas):**
```bash
agregar_heladera 0 0  # Siempre 0.7×0.7×1.8m
```

**Ahora (dimensiones opcionales):**
```bash
# Con dimensiones por defecto
h 0 0
✓ Heladera 0.7×0.7×1.8m

# Con dimensiones personalizadas
h 0 0 0 0.9 0.8 2.0
✓ Heladera 0.9×0.8×2.0m (más grande)

h 2 0 0 0.6 0.6 1.6 heladera_pequeña
✓ Heladera 0.6×0.6×1.6m (más pequeña)
```

**Sintaxis completa:**
```bash
agregar_heladera <x> <y> [z] [ancho] [prof] [alto] [nombre]
agregar_cocina <x> <y> [z] [ancho] [prof] [nombre]
agregar_pileta <x> <y> [z] [ancho> [prof] [nombre]
agregar_mesada <x> <y> [z] [ancho] [prof] [nombre]
```

### 6. **Grid Cada 0.1m** ✅

**Vista de Planta:**
- Grid principal (líneas gruesas): cada 1.0m
- Grid secundario (líneas punteadas): cada 0.1m
- Etiquetas en ejes: cada 0.5m
- Alpha 0.5 para principal, 0.2 para secundario

Mucho más preciso para posicionamiento exacto.

---

## 🚀 Cómo Ejecutar

```bash
python3 room_designer_gui.py
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Cocina con Dimensiones Custom

```bash
>>> n 4 5
✓ 4×5×2.8m

# Heladera más grande
>>> h 0 0 0 0.9 0.8 2.0 heladera_grande
✓ Heladera agregada

# Cocina más pequeña
>>> co 1 0 0 0.5 0.5 cocina_compacta
✓ Cocina agregada

# Mesada extra larga
>>> ms 1.6 0 0 2.5 0.6 mesada_larga
✓ Mesada agregada

# Pileta profunda
>>> pi 3.5 0 0 1.0 0.7 pileta_doble
✓ Pileta agregada

# Cambiar color de heladera
>>> color heladera_grande
[Selector de color → elegir color]
✓ Color aplicado

# Ver coordenadas en pantalla
[F2 - Vista Planta]
[Se ven todos con coordenadas visibles]
```

### Ejemplo 2: Dormitorio con Renombrado

```bash
>>> n 5 5
>>> c 1 1 cama
✓ Cama agregada

# Renombrar
>>> renombrar cama cama_king
✓ 'cama' → 'cama_king'

# Cambiar color
>>> color cama_king azul
✓ Color 'azul' para 'cama_king'

# Verificar coordenadas
[F2 - Vista Planta]
[Se ve: "cama_king" y "(1.00, 1.00)" en el objeto]

# Mover con precisión usando grid 0.1m
>>> m cama_king 0.3 0.2 0
✓ Movido
[Ahora se ve: "(1.30, 1.20)"]
```

### Ejemplo 3: Export STL con Altura Correcta

```bash
>>> n 5 5 3.5
✓ 5×5×3.5m

>>> c 1 1
>>> h 0 0 0 0.7 0.7 1.8
>>> co 1 0

# Exportar
>>> e3d mi_casa

# O desde terminal:
>>> export_stl mi_casa.stl
✓ Diseño exportado: mi_casa.stl (XXX triángulos, altura=3.5m)

# Abrir en visor
[El STL ahora tiene paredes de 3.5m de alto]
[Antes: paredes muy bajas o inexistentes]
[Ahora: paredes con altura correcta + techo]
```

### Ejemplo 4: Ayuda Contextual

```bash
# Olvidaste sintaxis
>>> agregar_mesada
ℹ️  agregar_mesada <x> <y> [z] [ancho] [prof] [nombre]
  Ej: agregar_mesada 0.5 0 0 2.0 0.6 mesada

# Ahora sabes qué parámetros necesitas
>>> agregar_mesada 0.5 0 0 3.0 0.7 mesada_extra_larga
✓ Mesada agregada

# Otro comando
>>> mover
ℹ️  mover <nombre> <dx> <dy> <dz>
  Mueve RELATIVO (no absoluto)
  Ej: mover cama 0.5 0 0  (mueve +0.5m en X)

>>> mover mesada_extra_larga 0 0.1 0
✓ Movido
```

---

## 🎯 Mejoras Visuales

### Grid Mejorado
```
Antes:
┌─────────┬─────────┐  (grid cada 1m)
│         │         │
│    ?    │    ?    │
│         │         │
└─────────┴─────────┘

Ahora:
┌─:─:─:─┬─:─:─:─┐  (grid cada 0.1m)
│ · · · │ · · · │
│·······│·······│
│ · · · │ · · · │
└─:─:─:─┴─:─:─:─┘
```

### Coordenadas Visibles
```
Antes:
┌─────────┐
│  cama   │  ← Solo nombre
└─────────┘

Ahora:
┌──────────┐
│  cama    │  ← Nombre
│ (1.5,2.0)│  ← Coordenadas
└──────────┘
```

---

## 🛠️ Comandos Nuevos

```bash
renombrar <viejo> <nuevo>  # Renombrar objeto
color <nombre> [color]     # Cambiar color
```

---

## 🎨 Colores Disponibles

**Texto:**
- rojo, azul, verde, amarillo
- naranja, morado, rosa, cyan
- negro, blanco, gris

**Hex:**
- #FF0000 (rojo)
- #00FF00 (verde)
- #0000FF (azul)
- Cualquier código hex válido

**Selector Visual:**
```bash
>>> color cama
[Se abre ventana con selector de color]
[Click en color → OK]
✓ Color aplicado
```

---

## 📦 Archivos

1. **room_designer.py** - Motor con STL mejorado
2. **room_designer_gui.py** - v3.2 completa
3. **GUIA_v3.2.md** - Este documento

---

## ✅ Checklist Completo

- [x] STL con altura correcta (paredes incluidas)
- [x] Ayuda contextual (comando solo → ayuda)
- [x] Renombrar objetos
- [x] Cambiar color de objetos
- [x] Coordenadas visibles en pantalla
- [x] Dimensiones custom para cocina
- [x] Grid cada 0.1m (principal + secundario)
- [x] Historial de comandos (↑/↓)
- [x] 4 vistas laterales (N/S/E/O)
- [x] Mover relativo
- [x] Selección de objetos
- [x] Comandos abreviados
- [x] Import/Export STL
- [x] Grupos de objetos

---

## 🐛 Solución de Problemas

**P: STL sigue sin altura correcta**
```bash
# Verifica la versión:
>>> import room_designer
>>> room_designer.__file__

# Debe ser la v3.2
# Si no, actualiza los archivos
```

**P: No veo las coordenadas**
```bash
# Asegúrate de estar en vista Planta (F2)
# Las coordenadas solo aparecen en planta
```

**P: El grid está muy denso**
```bash
# Es normal, hay un grid cada 0.1m
# Grid principal (1m): líneas sólidas
# Grid secundario (0.1m): líneas punteadas
```

**P: Color no cambia**
```bash
# Después de cambiar color:
>>> [Presiona F2 para refrescar]
# O ejecuta cualquier comando
```

---

## 💡 Tips

1. **Precisión con Grid**:
   - Usa el grid 0.1m para posicionamiento exacto
   - Las coordenadas se ven en tiempo real

2. **Dimensiones Cocina**:
   - Todas las dimensiones son opcionales
   - Sin especificar = valores por defecto razonables

3. **Colores**:
   - Colores personalizados se guardan en la sesión
   - Se pierden al cerrar (guarda en JSON si implementas)

4. **Ayuda**:
   - Escribe solo el comando para ver sintaxis
   - Muy útil cuando olvidas parámetros

5. **STL**:
   - Ahora exporta paredes completas
   - Listo para imprimir 3D o ver en visor

---

**Room Designer v3.2 - COMPLETO**
Todas las mejoras solicitadas implementadas ✅
