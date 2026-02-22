# 🚀 Room Designer v3.0 - Guía de Uso Rápido

## Cómo Ejecutar

```bash
# Con interfaz gráfica (RECOMENDADO)
python3 room_designer_gui.py

# Sin interfaz (solo terminal)
python3 room_designer.py
```

---

## ✅ TODAS LAS FUNCIONALIDADES IMPLEMENTADAS

### 1. **4 Vistas Laterales** ✅
- **F2**: Vista Planta
- **F3**: Vista Norte (desde +Y)
- **F4**: Vista Sur (desde -Y)
- **F5**: Vista Este (desde +X)
- **F6**: Vista Oeste (desde -X)

### 2. **Historial de Comandos** ✅
- **↑**: Comando anterior
- **↓**: Comando siguiente
- Guarda todos los comandos de la sesión

### 3. **Atajos de Teclado** ✅
- **F1**: Mostrar/ocultar ayuda
- **F2-F6**: Cambiar vistas
- **Ctrl+G**: Guardar rápido (design.json)
- **Ctrl+O**: Abrir archivo
- **Ctrl+L**: Limpiar salida
- **ESC**: Limpiar entrada

### 4. **Comandos Abreviados** ✅
```
n   = nuevo
c   = agregar_cama
p   = agregar_puerta
v   = agregar_ventana
m   = mover (ahora RELATIVO!)
r   = rotar
d   = eliminar
l   = listar
g   = guardar
s   = select
```

### 5. **Autocompletar con TAB** ✅
- Escribe parte del comando y presiona TAB
- Muestra opciones si hay múltiples coincidencias

### 6. **Arcos de Puertas Visibles** ✅
- Se dibujan en ROJO
- Muestran dirección de apertura
- Línea sólida + arco punteado

### 7. **Mover con Coordenadas RELATIVAS** ✅
```bash
# Antes (absoluto):
mover cama 2 3 0  # mueve A posición (2,3,0)

# Ahora (relativo):
m cama 0.5 0 0    # mueve +0.5m en X
```

### 8. **Selección de Objeto** ✅
```bash
select cama       # Selecciona cama
m 0.5 0 0        # Mueve cama 0.5m en X
r                # Rota cama
d                # Elimina cama
```

### 9. **Comandos Encadenados** ✅
```bash
n 5 5; c 1 1; p 2 0; l
# Ejecuta múltiples comandos en una línea
```

### 10. **Eliminar Funciona** ✅
```bash
d cama           # Elimina cama
eliminar puerta  # Elimina puerta
```

---

## 📖 Ejemplos de Uso

### Flujo Básico
```bash
# 1. Ejecutar
python3 room_designer_gui.py

# 2. Crear espacio (comando o abreviatura)
>>> n 5 5
✓ Espacio: 5×5×2.8m

# 3. Agregar muebles
>>> c 1 1 cama_principal
✓ Cama 'cama_principal' agregada

# 4. Agregar puerta (se ve el arco!)
>>> p 2 0 0.9 horizontal derecha norte entrada
✓ Puerta agregada
[Arco rojo visible en planta]

# 5. Mover con coordenadas relativas
>>> m cama_principal 0.5 0 0
✓ 'cama_principal' movido (Δx=0.5, Δy=0, Δz=0)

# 6. Cambiar vista con F3
[Presiona F3]
✓ Vista NORTE
[Ves la elevación lateral]

# 7. Guardar
>>> g mi_diseño.json
✓ Diseño guardado
```

### Flujo Ágil (con abreviaturas)
```bash
# Todo en comandos cortos
>>> n 5 5; c 1 1; c 3 1; p 2 0
✓ Todo creado en una línea

# Usar selección
>>> s cama
✓ cama seleccionado

>>> m 0.2 0.3 0
✓ movido

>>> r
✓ rotado 90°

# Cambiar vistas rápido
[F2] Planta
[F3] Norte
[F4] Sur
[F5] Este
[F6] Oeste
```

### Historial
```bash
>>> n 5 5
>>> c 1 1
>>> [Presiona ↑]
>>> c 1 1  # Aparece último comando
>>> [Presiona ↑ dos veces]
>>> n 5 5  # Aparece comando anterior
>>> [Edita y ejecuta]
```

### Autocompletar
```bash
>>> agr[TAB]
Opciones: agregar_cama, agregar_puerta, ...

>>> agregar_c[TAB]
>>> agregar_cama  # Se autocompleta
```

---

## 🎨 Interfaz Visual

```
┌────────────────────────────────────────────────────────┐
│ Visualización              │ Ayuda Rápida             │
│                            │ ATAJOS:                  │
│ [F2:Planta] [F3:Norte]    │ F1-F6, Ctrl+G           │
│ [F4:Sur] [F5:Este]        │ ↑/↓ historial           │
│ [F6:Oeste] [F1:Ocultar]   │ TAB autocompletar       │
│                            │                          │
│ ┌────────────────────┐    │ ABREVIATURAS:           │
│ │                    │    │ n, c, p, m, r, d        │
│ │  [PLANTA CON       │    │                          │
│ │   ARCOS ROJOS]     │    │ MOVER RELATIVO:         │
│ │                    │    │ m cama 0.5 0 0          │
│ └────────────────────┘    │ (mueve +0.5m en X)      │
├────────────────────────────────────────────────────────┤
│ Salida:                                               │
│ >>> n 5 5                                             │
│ ✓ Espacio creado                                      │
├────────────────────────────────────────────────────────┤
│ >>> [comando___________] [Ejecutar] [Limpiar]        │
└────────────────────────────────────────────────────────┘
```

---

## 🔧 Solución de Problemas

**P: No aparece ventana**
R: Ejecuta `python3 room_designer_gui.py` (con _gui)

**P: F1-F6 no funcionan**
R: Asegúrate de tener la v3.0 más reciente

**P: Los arcos de las puertas no se ven**
R: Están en ROJO. Si no los ves, verifica que la puerta esté creada correctamente

**P: Mover no funciona**
R: Recuerda que ahora es RELATIVO:
   - `m cama 0.5 0 0` mueve +0.5m
   - No es posición absoluta

**P: Eliminar no funciona**  
R: v3.0 corrige esto. Usa `d <nombre>` o `eliminar <nombre>`

---

## 📦 Archivos

1. **`room_designer.py`** - Motor (mover relativo, remove corregido)
2. **`room_designer_gui.py`** - GUI v3.0 con TODO implementado ⭐
3. **`GUIA_USO_v3.0.md`** - Este archivo
4. **`MEJORAS_AGILIDAD.md`** - Ideas futuras

---

## 🎯 Funcionalidades Principales

| Funcionalidad | Estado | Cómo Usar |
|--------------|--------|-----------|
| 4 Vistas laterales | ✅ | F3, F4, F5, F6 |
| Historial | ✅ | ↑/↓ |
| Atajos teclado | ✅ | F1-F6, Ctrl+G/O/L |
| Abreviaturas | ✅ | n, c, p, m, r, d, l, g |
| Autocompletar | ✅ | TAB |
| Arcos puertas | ✅ | Rojos en planta |
| Mover relativo | ✅ | m <obj> <dx> <dy> <dz> |
| Selección objeto | ✅ | select <nombre> |
| Comandos encadenados | ✅ | cmd1; cmd2; cmd3 |
| Eliminar | ✅ | d <nombre> |

---

**¡Todo implementado y funcionando!** 🎉

Para ejecutar: `python3 room_designer_gui.py`
