# 🎉 Room Designer v3.1 - VERSIÓN COMPLETA FINAL

## 🚀 Cómo Ejecutar

```bash
python3 room_designer_gui.py
```

---

## ✅ TODAS LAS FUNCIONALIDADES

### 1. **Cocina Completa** ✅

```bash
# Heladera (0.7×0.7×1.8m)
h 0 0 heladera
agregar_heladera 0 0 mi_heladera

# Cocina/Estufa (0.6×0.6m)
co 1 0 cocina
agregar_cocina 1 0 estufa_principal

# Pileta/Fregadero (0.8×0.6m)
pi 2 0 pileta
agregar_pileta 2 0 lavaplatos

# Mesada (2.0×0.6m)
ms 0.5 0 mesada
agregar_mesada 0.5 0 mesada_principal

# Alacena/Gabinete
agregar_alacena 0 1 0 1.5 0.4 2.0 alacena_alta
```

### 2. **Muebles Personalizados** ✅

```bash
# Sintaxis completa:
mb <x> <y> <z> <ancho> <prof> <alto> <nombre> <tipo>

# Ejemplos:
mb 2 2 0 0.8 0.6 1.5 estante biblioteca
mb 3 1 0 0.5 0.5 0.8 mesita auxiliar
mb 1 3 0 1.2 0.8 0.75 escritorio mesa
mb 0.5 2 0 0.6 0.6 1.0 banqueta silla

# Tipos sugeridos:
# mesa, silla, estante, armario, escritorio,
# biblioteca, banqueta, auxiliar, consola, etc
```

### 3. **Export 3D con Visor Automático** ✅

#### Formatos Soportados:
- **STL**: Para impresión 3D, CAD
- **OBJ**: Universal, más compatible

#### Métodos:

**Botón en GUI:**
```
[Click en "🔲 Export 3D"]
✓ Exporta modelo.stl y modelo.obj
✓ Abre automáticamente en visor del sistema
```

**Comando:**
```bash
e3d mi_modelo
# Exporta: mi_modelo.stl y mi_modelo.obj
# Abre automáticamente
```

#### Visores Recomendados (Gratuitos):

**Windows:**
- Windows 3D Viewer (incluido)
- Blender (gratuito)
- MeshLab (gratuito)

**macOS:**
- Preview (incluido)
- Blender (gratuito)
- MeshLab (gratuito)

**Linux:**
```bash
# Instalar uno de estos:
sudo apt install meshlab       # Recomendado
sudo apt install blender       # Más pesado
sudo snap install f3d          # Ligero

# La GUI detecta automáticamente cual tienes
```

### 4. **Import STL** ✅

```bash
# Importar modelo STL existente
importar_stl silla.stl silla_1 1 2 0
importar_stl lampara.stl lampara 0.5 0.5 1.5

# Sintaxis:
importar_stl <archivo> [nombre] [x] [y] [z]
```

### 5. **Dimensiones Personalizadas** ✅

Todos los comandos aceptan dimensiones opcionales:

```bash
# Con dimensiones por defecto
c 1 1 cama_queen

# Con dimensiones personalizadas
# (se requiere usar nombres completos)
agregar_cama 1 1 0 1.6 2.0 cama_king

agregar_ropero 0 3 0 2.0 0.6 2.2 ropero_grande

agregar_mesa_luz 2 1 0 0.6 0.5 mesa_amplia
```

---

## 📖 Ejemplos Completos

### Cocina Completa

```bash
>>> n 4 5
✓ Espacio: 4×5×2.8m

>>> h 0 0
✓ Heladera agregada

>>> co 0.8 0
✓ Cocina agregada

>>> pi 1.5 0
✓ Pileta agregada

>>> ms 0 0.7
✓ Mesada agregada

>>> agregar_alacena 0 0 1.9 2.5 0.35 0.8 alacenas
✓ Alacena agregada

>>> p 2 0
✓ Puerta agregada

>>> [F2] Vista planta
[Se ve todo con colores distintos]

>>> e3d cocina
✓ Exportado: cocina.stl y cocina.obj
[Se abre en visor 3D]
```

### Sala de Estar con Muebles Custom

```bash
>>> n 6 6
>>> mb 1 1 0 2.5 1.0 0.8 sofa sofá
✓ Sofá agregado

>>> mb 3.5 2 0 0.6 0.6 0.5 mesa_centro mesa
✓ Mesa agregada

>>> mb 0.2 4 0 1.5 0.4 2.0 biblioteca estante
✓ Estante agregado

>>> mb 5 0.5 0 1.2 0.8 0.75 escritorio mesa
✓ Mesa agregada

>>> p 3 0 0.9 horizontal derecha norte entrada
✓ Puerta agregada

>>> v 0 3 1.2 1.5 1.0 ventana
✓ Ventana agregada

>>> g sala.json
✓ Guardado

>>> e3d sala
[Se abre visor 3D]
```

### Dormitorio + Cocina Integrado

```bash
>>> n 8 5
>>> c 0.5 1 cama
>>> agregar_ropero 3 0.5 ropero
>>> agregar_mesa_luz 2.5 1 mesa_izq
>>> agregar_mesa_luz 2.5 2.7 mesa_der

# Zona cocina
>>> h 6 0 heladera
>>> co 7 0 cocina
>>> ms 6 0.8 mesada

# Puerta divisoria
>>> p 5 2.5 0.8 vertical abajo oeste division

>>> agrupar dormitorio cama ropero mesa_izq mesa_der
✓ Grupo creado

>>> agrupar cocina heladera cocina mesada
✓ Grupo creado

>>> l
[Lista completa de objetos]

>>> g casa_completa.json
>>> e3d casa
[Visor 3D abierto]
```

---

## 🎨 Colores en Vista Planta

| Tipo | Color | Hex |
|------|-------|-----|
| Cama | Rosa claro | #FFB6C1 |
| Ropero | Marrón | #8B4513 |
| Mesa | Beige | #DEB887 |
| Heladera | Azul claro | #B0C4DE |
| Cocina | Rojo tomate | #FF6347 |
| Pileta | Azul acero | #4682B4 |
| Mesada | Trigo | #F5DEB3 |
| Alacena | Marrón medio | #A0522D |
| Puerta | Tan | #D2B48C |
| Ventana | Celeste | #87CEEB |
| Custom | Orquídea | #DDA0DD |

---

## 🔧 Atajos y Comandos

### Teclado
- **F1**: Ayuda
- **F2**: Planta
- **F3-F6**: Laterales (N/S/E/O)
- **Ctrl+G**: Guardar
- **Ctrl+L**: Limpiar
- **↑/↓**: Historial
- **TAB**: Autocompletar

### Abreviaturas
```
n=nuevo    c=cama      p=puerta
h=heladera co=cocina   pi=pileta
ms=mesada  mb=mueble   m=mover
r=rotar    d=eliminar  l=listar
g=guardar  s=select    e3d=export
```

---

## 🎯 Flujo de Trabajo Típico

1. **Crear espacio**: `n 5 5`
2. **Agregar muebles**: `c 1 1; h 0 0; co 1 0`
3. **Ajustar**: `m cama 0.5 0 0`
4. **Ver diferentes ángulos**: F2-F6
5. **Guardar**: `g mi_diseño.json`
6. **Ver en 3D**: Click "🔲 Export 3D" o `e3d`
7. **Editar en visor** (opcional): Meshlab, Blender, etc.

---

## 📦 Archivos Generados

```
mi_proyecto/
├── design.json          # Diseño guardado
├── modelo.stl          # Export 3D (binario)
├── modelo.obj          # Export 3D (texto, más compatible)
└── planta.png          # Vista 2D (si se genera)
```

---

## 💡 Tips

1. **Dimensiones realistas**:
   - Cama individual: 1.0×2.0m
   - Cama doble: 1.4×1.9m
   - Cama king: 1.8×2.0m
   - Heladera estándar: 0.7×0.7×1.8m
   - Cocina: 0.6×0.6×0.9m

2. **Orden lógico**:
   - Estructura → Paredes → Puertas/Ventanas → Muebles grandes → Detalles

3. **Grupos**:
   - Agrupa por zonas: dormitorio, cocina, baño
   - Más fácil de mover todo junto

4. **Export 3D**:
   - OBJ más universal que STL
   - STL mejor para impresión 3D
   - Ambos se generan automáticamente

---

## 🐛 Solución de Problemas

**P: No se abre el visor 3D**
```bash
# Linux - instalar visor:
sudo apt install meshlab

# Luego abrir manualmente:
meshlab modelo.obj
```

**P: Quiero cambiar colores**
R: Abre el .obj en Blender/Meshlab y aplica materiales

**P: El modelo 3D se ve raro**
R: Verifica que las dimensiones sean realistas (metros, no cm)

**P: Falta comando de cocina**
R: Actualiza a v3.1: `python3 room_designer_gui.py`

---

## ✅ Checklist de Funcionalidades

- [x] Crear espacios (rectangular e irregular)
- [x] Dormitorio completo (cama, ropero, mesas)
- [x] Cocina completa (heladera, cocina, pileta, mesada, alacena)
- [x] Muebles personalizados (cualquier dimensión)
- [x] Puertas con arcos visibles
- [x] Ventanas
- [x] 4 vistas laterales
- [x] Historial de comandos
- [x] Atajos de teclado
- [x] Comandos abreviados
- [x] Mover relativo
- [x] Selección de objetos
- [x] Grupos
- [x] Import STL
- [x] Export STL + OBJ
- [x] Visor 3D automático
- [x] Guardar/Cargar JSON

---

**Room Designer v3.1 - Diseño Completo**

Todo implementado y funcionando. ¡A diseñar! 🏠✨
