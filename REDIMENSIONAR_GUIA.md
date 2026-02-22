# 📏 Redimensionar Objetos - Guía Completa

## ✅ Nueva Funcionalidad Implementada

Ahora puedes cambiar las dimensiones de cualquier objeto de **dos formas**:

1. **Comando `redimensionar`** - Cambios precisos con valores numéricos
2. **Flechas del teclado** - Ajustes finos en tiempo real (0.01m por tecla)

---

## 🎯 Método 1: Comando `redimensionar`

### Sintaxis
```bash
redimensionar <nombre> <delta_width> <delta_depth> <delta_height>
# O abreviado:
rd <nombre> <dw> <dd> <dh>
```

### Características
- **Cambios RELATIVOS**: Se suman/restan a las dimensiones actuales
- **Posición fija**: La esquina del objeto (X, Y, Z) NO cambia
- **Límite mínimo**: 0.01m (1cm) - no se puede hacer más pequeño

### Ejemplos

#### Agrandar una mesa
```bash
>>> agregar_mueble 2 2 0 1.0 0.8 0.7 mesa comedor
✓ Mesa agregada: 1.0×0.8×0.7m

>>> redimensionar mesa 0.5 0.2 0
✓ 'mesa' redimensionado:
  1.00×0.80×0.70m → 1.50×1.00×0.70m
```

#### Hacer una heladera más alta
```bash
>>> h 0 0 heladera
✓ Heladera: 0.7×0.7×1.8m

>>> rd heladera 0 0 0.3
✓ 'heladera' redimensionado:
  0.70×0.70×1.80m → 0.70×0.70×2.10m
```

#### Reducir ancho de mesada
```bash
>>> ms 1 0 mesada
✓ Mesada: 2.0×0.6m

>>> rd mesada -0.5 0 0
✓ 'mesada' redimensionado:
  2.00×0.60×0.90m → 1.50×0.60×0.90m
```

#### Con objeto seleccionado
```bash
>>> s cama
✓ 'cama' seleccionado

>>> rd 0.2 0.1 0
✓ 'cama' redimensionado:
  1.40×1.90×0.60m → 1.60×2.00×0.60m
```

---

## 🎮 Método 2: Flechas del Teclado

### Requisito
```bash
# Primero seleccionar el objeto
>>> select mesa
✓ 'mesa' seleccionado
```

### Control según Vista Activa

#### 📐 Vista Planta (F2)
```
Eje X (ancho):
  ← Flecha Izquierda:  -0.01m width
  → Flecha Derecha:    +0.01m width

Eje Y (profundidad):
  ↑ Flecha Arriba:     -0.01m depth
  ↓ Flecha Abajo:      +0.01m depth
```

**Ejemplo**:
```bash
>>> s mesa
>>> [F2]  # Vista planta
>>> [→→→→→]  # 5 veces = +0.05m width
>>> [↓↓]      # 2 veces = +0.02m depth
```

#### 🔲 Vistas Norte/Sur (F3/F4)
```
Eje X (ancho):
  ← Flecha Izquierda:  -0.01m width
  → Flecha Derecha:    +0.01m width

Eje Z (altura):
  ↑ Flecha Arriba:     +0.01m height
  ↓ Flecha Abajo:      -0.01m height
```

**Ejemplo**:
```bash
>>> s heladera
>>> [F3]  # Vista norte
>>> [↑↑↑↑↑↑↑↑↑↑]  # 10 veces = +0.10m height
```

#### 🔲 Vistas Este/Oeste (F5/F6)
```
Eje Y (profundidad):
  ← Flecha Izquierda:  -0.01m depth
  → Flecha Derecha:    +0.01m depth

Eje Z (altura):
  ↑ Flecha Arriba:     +0.01m height
  ↓ Flecha Abajo:      -0.01m height
```

---

## 📊 Tabla Resumen de Flechas

| Vista | ← | → | ↑ | ↓ |
|-------|---|---|---|---|
| **Planta** (F2) | -W | +W | -D | +D |
| **Norte** (F3) | -W | +W | +H | -H |
| **Sur** (F4) | -W | +W | +H | -H |
| **Este** (F5) | -D | +D | +H | -H |
| **Oeste** (F6) | -D | +D | +H | -H |

Donde:
- **W** = Width (ancho, eje X)
- **D** = Depth (profundidad, eje Y)
- **H** = Height (altura, eje Z)

---

## 💡 Casos de Uso Prácticos

### Ajustar mesa al espacio disponible
```bash
>>> n 4 4
>>> agregar_mueble 1 1 0 1.5 1.0 0.7 mesa comedor

# La mesa es muy ancha
>>> s mesa
>>> [F2]  # Vista planta
>>> [←←←←←←←←←←]  # Reduce 0.1m el ancho
✓ Mesa ahora: 1.40m de ancho
```

### Hacer heladera más alta para alcanzar techo
```bash
>>> n 3.5 3.5 2.67
>>> h 0 0 0 0.7 0.7 1.8 heladera

# Queremos que llegue casi al techo (2.67m)
>>> s heladera
>>> [F3]  # Vista norte (se ve la altura)
>>> [↑↑↑...]  # Repetir hasta llegar a ~2.6m
✓ Heladera ahora: 2.60m de alto
```

### Afinar mesada para que encaje
```bash
>>> ms 0 0 0 3.0 0.6 mesada

# Necesita ser 2.85m para encajar entre paredes
>>> rd mesada -0.15 0 0
✓ 'mesada' redimensionado:
  3.00×0.60m → 2.85×0.60m
```

---

## 🔒 Límites y Restricciones

### Dimensión Mínima: 0.01m (1cm)
```bash
>>> agregar_mueble 2 2 0 0.1 0.1 0.1 cubo pequeño

>>> rd cubo -0.1 0 0
✓ 'cubo' redimensionado:
  0.10×0.10×0.10m → 0.01×0.10×0.10m
# Se aplicó el límite mínimo

>>> rd cubo -0.1 0 0
✓ 'cubo' redimensionado:
  0.01×0.10×0.10m → 0.01×0.10×0.10m
# Ya no puede ser más pequeño
```

### La Posición NO Cambia
```bash
>>> agregar_mueble 2 3 0 1 1 1 caja origen

# Posición original: (2, 3, 0)
>>> rd caja 0.5 0.5 0.5
✓ Redimensionado: 1.0×1.0×1.0m → 1.5×1.5×1.5m

# La posición SIGUE siendo: (2, 3, 0)
# Solo cambian las dimensiones
# La caja crece hacia la derecha/atrás/arriba
```

---

## 🎨 Workflow Completo

### Crear y Ajustar una Mesa

```bash
# 1. Crear habitación
>>> n 5 5

# 2. Agregar mesa en el centro
>>> agregar_mueble 2 2 0 1.2 0.8 0.7 mesa comedor

# 3. Ver en planta
>>> [F2]

# 4. Seleccionar para editar
>>> s mesa
✓ 'mesa' seleccionado

# 5. Ajustar ancho con flechas
>>> [→→→→→]  # +0.05m ancho
✓ 'mesa' redimensionado: 1.20×0.80×0.70m → 1.25×0.80×0.70m

# 6. Ver desde el norte para ajustar altura
>>> [F3]
>>> [↑↑]  # +0.02m altura
✓ 'mesa' redimensionado: 1.25×0.80×0.70m → 1.25×0.80×0.72m

# 7. Ajuste fino con comando
>>> rd 0.05 0 -0.02
✓ 'mesa' redimensionado: 1.25×0.80×0.72m → 1.30×0.80×0.70m

# 8. Perfecto!
```

---

## ⚡ Tips y Trucos

### 1. Ajuste Rápido vs. Fino
```bash
# Cambio grande: usar comando
>>> rd mesa 0.5 0 0

# Ajuste fino: usar flechas
>>> [→→→]  # +0.03m
```

### 2. Ver Cambios en Tiempo Real
```bash
>>> s objeto
>>> [F2]  # Vista apropiada
>>> [flechas]  # Los cambios se ven inmediatamente
```

### 3. Trabajar con Objetos Seleccionados
```bash
>>> s mesa
>>> rd 0.1 0.1 0.1  # No necesitas repetir el nombre
```

### 4. Resetear Dimensiones
```bash
# Si te equivocaste, puedes volver atrás
>>> rd mesa -0.5 -0.3 0
# O recrear el objeto
>>> d mesa
>>> agregar_mueble 2 2 0 1.0 0.8 0.7 mesa comedor
```

---

## 🐛 Solución de Problemas

### "Las flechas no funcionan"
**Solución**: Asegúrate de haber seleccionado un objeto:
```bash
>>> s nombre_objeto
>>> [luego usar flechas]
```

### "El objeto se mueve en lugar de cambiar tamaño"
**Problema**: Las flechas están configuradas para el historial de comandos
**Solución**: Haz click fuera del campo de comandos, en el área de visualización

### "No puedo hacer el objeto más pequeño"
**Causa**: Llegaste al límite mínimo de 0.01m
**Solución**: Ese es el límite, no se puede ir más abajo

---

## 📋 Resumen Rápido

```bash
# COMANDO
redimensionar <nombre> <dw> <dd> <dh>
rd <nombre> <dw> <dd> <dh>

# FLECHAS (objeto seleccionado)
Planta (F2): ←→ ancho, ↑↓ profundidad
Norte/Sur (F3/F4): ←→ ancho, ↑↓ altura
Este/Oeste (F5/F6): ←→ profundidad, ↑↓ altura

# LÍMITES
Mínimo: 0.01m
Incremento con flechas: 0.01m
Posición del objeto: NO cambia
```

---

**¡Ahora puedes ajustar cada mueble al milímetro!** 📏✨
