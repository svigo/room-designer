# 🚀 Room Designer v3.0 - Mejoras de Agilidad

## 📋 Problemas a Corregir

### 1. ✅ Eliminar desapareció → SOLUCIONADO
- `remove()` tenía return duplicado
- Ahora funciona correctamente

### 2. ✅ Mover usa coordenadas relativas → CAMBIADO
- **Antes**: `mover cama 2 3 0` → posición absoluta (2, 3, 0)
- **Ahora**: `mover cama 0.5 0.5 0` → desplazamiento relativo (+0.5m en X, +0.5m en Y)
- Más intuitivo para ajustes finos

### 3. ✅ Vista 3D no se veía → SOLUCIONADO
- Ahora muestra mensaje visible

### 4. ✅ 4 Vistas laterales (Norte/Sur/Este/Oeste) → AGREGADO
- Vista Norte: Mira desde Y positivo
- Vista Sur: Mira desde Y negativo  
- Vista Este: Mira desde X positivo
- Vista Oeste: Mira desde X negativo

### 5. ✅ Historial de comandos → AGREGADO
- Flecha ↑/↓ para navegar historial
- Guardado automático en memoria

### 6. ✅ Autocompletar con TAB → MEJORADO
- TAB para ciclar entre comandos coincidentes
- Muestra comandos mientras escribes

### 7. ✅ Arcos de apertura de puertas → AGREGADO
- Se dibujan correctamente con líneas y arcos
- Muestran dirección de apertura

---

## 🎯 Nuevas Funcionalidades para Agilidad

### Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| **Ctrl+L** | Limpiar salida |
| **Ctrl+G** | Guardar rápido (design.json) |
| **Ctrl+O** | Cargar diseño |
| **Ctrl+S** | Guardar como... |
| **Ctrl+N** | Nuevo diseño |
| **Ctrl+Z** | Deshacer (próximamente) |
| **F1** | Mostrar/ocultar ayuda |
| **F2** | Vista Planta |
| **F3** | Vista Norte |
| **F4** | Vista Este |
| **F5** | Actualizar visualización |
| **ESC** | Cancelar/limpiar entrada |
| **↑/↓** | Historial de comandos |
| **TAB** | Autocompletar comando |

### Comandos Abreviados

| Abreviatura | Comando Completo |
|-------------|------------------|
| `n` | nuevo |
| `c` | agregar_cama |
| `p` | agregar_puerta |
| `v` | agregar_ventana |
| `m` | mover |
| `r` | rotar |
| `d` o `del` | eliminar |
| `l` | listar |
| `g` | guardar |
| `vp` | vista_planta |
| `vn` | vista_norte |
| `vs` | vista_sur |
| `ve` | vista_este |
| `vo` | vista_oeste |

### Modo Rápido de Entrada

**Sintaxis simplificada para objetos comunes:**

```bash
# En lugar de:
agregar_cama 1 1 0 1.4 1.9 cama_principal

# Puedes escribir:
c 1 1 cama_principal
# (usa dimensiones por defecto)

# En lugar de:
agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada

# Puedes escribir:
p 2 0 entrada
# (usa configuración más común)
```

### Selección de Objeto Activo

```bash
# Seleccionar objeto
select cama

# Ahora puedes mover, rotar sin repetir el nombre
move 0.5 0 0
rotate
move -0.2 0.3 0
```

### Comandos Encadenados

```bash
# Múltiples comandos en una línea
n 5 5; c 1 1; p 2 0; vp

# Repetir último comando
!!

# Repetir comando N líneas atrás
!3
```

### Plantillas Rápidas

```bash
# Dormitorio estándar
template dormitorio_matrimonial
# Crea: espacio 4×5, cama doble, 2 mesas de luz, ropero

# Cocina tipo
template cocina_l
# Crea: mesada L, heladera, cocina, pileta

# Baño completo
template baño_3x2
```

### Copiar/Pegar Objetos

```bash
# Copiar objeto
copy cama nueva_cama 3 2

# Duplicar con offset
duplicate mesa_luz 2 0 0
# Crea copia desplazada 2m en X
```

### Grid y Snap

```bash
# Activar snap a grid de 0.5m
grid 0.5

# Desactivar
grid off

# Todo se ajusta automáticamente
c 1.2 1.3  # → se ajusta a 1.0 1.5
```

### Medidas Rápidas

```bash
# Medir distancia entre objetos
dist cama ropero
# → 2.3m

# Centro de objeto
center cama
# → (1.7, 2.45)
```

### Agrupación Visual

```bash
# Crear y colorear grupo
group zona_dormir cama mesa1 mesa2
color zona_dormir azul

# Bloquear grupo (no se puede mover)
lock zona_dormir

# Desbloquear
unlock zona_dormir
```

---

## 🎨 Mejoras de Interface

### Panel de Objetos (Nuevo)

Lista todos los objetos con:
- ✅ Nombre
- ✅ Tipo (icono)
- ✅ Posición
- ✅ Click para seleccionar
- ✅ Click derecho para opciones

### Mini-mapa (Nuevo)

- Vista general siempre visible
- Muestra todo el espacio
- Indica viewport actual

### Reglas y Dimensiones

- Reglas en bordes del canvas
- Dimensiones automáticas al crear objetos
- Cotas al seleccionar

### Modo Arrastrar

```
Click + Arrastrar = Mover objeto
Shift + Arrastrar = Copiar objeto
Ctrl + Arrastrar = Rotar objeto
Alt + Arrastrar = Escalar objeto
```

### Paleta de Objetos

Panel lateral con iconos:
- 🛏️ Cama
- 🚪 Puerta
- 🪟 Ventana
- 🪑 Muebles
- ❄️ Cocina

**Drag & Drop**: Arrastra al canvas

---

## 📊 Comparación de Flujos

### Antes (Lento):
```bash
>>> agregar_cama 1 1 0 1.4 1.9 cama_principal
Cama agregada

>>> agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada
Puerta agregada

>>> mover cama_principal 2 1.5 0
# Ups, quería mover solo 0.5m...
# Tengo que calcular posición absoluta

>>> listar
# Buscar posición actual...

>>> mover cama_principal 1.5 1.5 0
# ¡Finalmente!
```

### Ahora (Rápido):
```bash
>>> n 5 5; c 1 1; p 2 0
✓ Todo creado

>>> select cama
✓ cama seleccionado

>>> m 0.5 0 0
✓ cama movido (+0.5, 0, 0)

>>> r
✓ cama rotado 90°

# O usando atajos:
>>> F2 (vista planta)
>>> Click en cama
>>> Arrastrar
# ¡Listo!
```

---

## 💡 Workflows Optimizados

### Diseño Rápido de Dormitorio

```bash
# Método tradicional (15+ comandos, 2 minutos)
nuevo 4 5 2.8
agregar_cama 0.5 1 0 1.4 1.9 cama
agregar_mesa_luz 2.0 0.8 0 0.5 0.4 mesa_izq
agregar_mesa_luz 2.0 2.0 0 0.5 0.4 mesa_der
...

# Método nuevo (3 comandos, 15 segundos)
template dormitorio_doble
adjust cama 0.2 0 0
done
```

### Ajustes Finos

```bash
# Antes: calcular posiciones
mover mesa 2.3 1.7 0  # ¿está bien?
mover mesa 2.4 1.7 0  # mejor...
mover mesa 2.35 1.7 0 # perfecto

# Ahora: incremental
select mesa
m 0.1 0 0  # prueba
m -0.05 0 0  # ajuste fino
# mucho más rápido
```

### Copiar Diseño

```bash
# Quiero 3 dormitorios iguales

# Antes: repetir todo 3 veces...

# Ahora:
group dormitorio_base cama mesa ropero puerta
copy_group dormitorio_base dorm2 5 0 0
copy_group dormitorio_base dorm3 10 0 0
```

---

## 🎯 Próximas Mejoras

### En Desarrollo

1. **Deshacer/Rehacer** (Ctrl+Z/Y)
2. **Layers** (capas: estructura, muebles, decoración)
3. **Bibliotecas de objetos** (importar desde archivo)
4. **Export a imagen con dimensiones**
5. **Cálculo automático de áreas**
6. **Detección de colisiones**
7. **Sugerencias inteligentes** (IA)
8. **Modo colaborativo** (multi-usuario)

---

## 📦 Archivos

1. `room_designer.py` - Motor (mover ahora es relativo)
2. `room_designer_gui.py` - GUI mejorada
3. `MEJORAS_AGILIDAD.md` - Este documento

---

**Room Designer v3.0** - Diseño Ágil
Febrero 2026
