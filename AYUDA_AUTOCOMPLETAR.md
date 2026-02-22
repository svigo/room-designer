# 📚 Ayuda Completa y Autocompletado

## ✅ Mejoras Implementadas

### 1. **Panel de Ayuda Completo** 📖
- **Antes**: Solo mostraba comandos básicos
- **Ahora**: TODOS los comandos con sintaxis completa
- **Scrollable**: Se puede recorrer con scroll si no cabe todo

### 2. **Autocompletado de Comandos** ⚡
- **Tecla**: `Ctrl+Space`
- **Funciones**:
  - Completa comando si hay un solo match
  - Muestra opciones si hay múltiples matches
  - Completa hasta el prefijo común

---

## 📖 Panel de Ayuda

### Contenido Completo

```
═══════════════════════════════════════════════════════
              ROOM DESIGNER v3.2 - GUÍA COMPLETA
═══════════════════════════════════════════════════════

NAVEGACIÓN:
  F1         Panel ayuda (toggle)
  F2-F6      Vistas (Planta, Norte, Sur, Este, Oeste)
  Ctrl+E     Exportar STL (diálogo)

ESPACIO:
  nuevo [w] [l] [h]        Crear (n)
  cargar <archivo.json>    Cargar diseño
  guardar [archivo.json]   Guardar diseño (g)
  listar                   Lista objetos (l)
  salir / exit             Salir

MUEBLES BÁSICOS:
  agregar_cama <x> <y> [nombre]                    (c)
  agregar_puerta <x> <y> [z] [w] [o] [b] [s] [n] (p)
  agregar_ventana <x> <y> <z> <w> <h> [n]         (v)

COCINA:
  agregar_heladera <x> <y> [z] [w] [d] [h] [n]   (h)
  agregar_cocina <x> <y> [z] [w] [d] [n]         (co)
  agregar_pileta <x> <y> [z] [w] [d] [n]         (pi)
  agregar_mesada <x> <y> [z] [w] [d] [n]         (ms)

MUEBLE PERSONALIZADO:
  agregar_mueble <x> <y> <z> <w> <d> <h> <n> [tipo]  (mb)

EDICIÓN:
  select <nombre>          Seleccionar (s)
  unselect                 Deseleccionar (us)
  mover <obj> <dx> <dy> <dz>                 (m)
  rotar <obj>              90° (r)
  redimensionar <obj> <dw> <dd> <dh>         (rd)
  renombrar <viejo> <nuevo>
  color <nombre> [color]
  eliminar <nombre>        (d)

EXPORTAR:
  exportar_stl [archivo.stl]      Sin colores (e)
  exportar_obj [nombre]            CON COLORES (obj)

HABITACIONES IRREGULARES:
  Usar cargar con JSON que tenga:
    "is_irregular": true
    "vertices": [[x1,y1], [x2,y2], ...]

CARACTERÍSTICAS:
  • Grid: 0.1m (primario 1m)
  • Dimensiones mínimas: 0.01m
  • Coordenadas visibles en objetos
  • Colores personalizables
  • Espejo Y corregido en exportaciones
  • STL sin techo para ver interior
  • OBJ con materiales y colores

AYUDA CONTEXTUAL:
  Comando solo → muestra sintaxis
  Ejemplo: >>> redimensionar
           ℹ️  redimensionar <nombre> <dw> <dd> <dh>

AUTOCOMPLETAR:
  Ctrl+Space    Completa comando

HISTORIAL:
  ↑↓           Comandos anteriores (si NO hay objeto seleccionado)

MÚLTIPLES COMANDOS:
  cmd1; cmd2; cmd3    Ejecuta secuencia

═══════════════════════════════════════════════════════
Presiona F1 para ocultar esta ayuda
═══════════════════════════════════════════════════════
```

### Cómo Acceder

```bash
# Toggle ayuda (mostrar/ocultar)
[F1]

# O desde comando
>>> ayuda
```

### Características

- ✅ **Scrollable**: Si no cabe todo, puedes hacer scroll
- ✅ **Completo**: TODOS los comandos están documentados
- ✅ **Organizado**: Por categorías (Espacio, Muebles, Edición, etc.)
- ✅ **Con abreviaturas**: Muestra las teclas cortas entre paréntesis
- ✅ **Sintaxis clara**: Formato consistente para todos los comandos

---

## ⚡ Autocompletado

### Uso Básico

```bash
>>> ag[Ctrl+Space]
💡 Comandos disponibles con 'ag':
  agregar_cama
  agregar_cocina
  agregar_heladera
  agregar_mesada
  agregar_mueble
  agregar_pileta
  agregar_puerta
  agregar_ventana

# Completa hasta el prefijo común
Campo ahora: agregar_
```

### Casos de Uso

#### Caso 1: Un Solo Match

```bash
>>> exp[Ctrl+Space]
# Se completa automáticamente a:
>>> exportar_
```

#### Caso 2: Múltiples Matches

```bash
>>> e[Ctrl+Space]
💡 Comandos disponibles con 'e':
  e → exportar_stl
  eliminar
  exportar_obj
  exportar_stl

# Completa hasta donde puede
Campo ahora: e
```

#### Caso 3: Con Abreviaturas

```bash
>>> c[Ctrl+Space]
💡 Comandos disponibles con 'c':
  c → agregar_cama
  cargar
  co → agregar_cocina
  color

# Muestra qué es cada abreviatura
```

#### Caso 4: Completar Abreviatura

```bash
>>> co[Ctrl+Space]
# Se completa a:
>>> co 
# (listo para escribir parámetros)
```

#### Caso 5: No Hay Matches

```bash
>>> xyz[Ctrl+Space]
❌ No hay comandos que empiecen con 'xyz'
```

---

## 🎯 Ejemplos Prácticos

### Workflow con Autocompletado

```bash
# 1. Empezar a escribir
>>> ag[Ctrl+Space]
💡 Comandos disponibles con 'ag':
  agregar_cama
  agregar_cocina
  ...
Campo: agregar_

# 2. Continuar
>>> agregar_c[Ctrl+Space]
💡 Comandos disponibles con 'agregar_c':
  agregar_cama
  agregar_cocina
Campo: agregar_c

# 3. Más específico
>>> agregar_ca[Ctrl+Space]
# Se completa:
>>> agregar_cama 

# 4. Agregar parámetros
>>> agregar_cama 1 1 cama_principal
[Enter]
✓ Cama agregada
```

### Usando Abreviaturas

```bash
# Escribir abreviatura directamente
>>> h 0 0
✓ Heladera agregada

# O autocompletar para ver qué hace
>>> h[Ctrl+Space]
💡 Comandos disponibles con 'h':
  h → agregar_heladera
  
# Ahora sabes que 'h' = heladera
```

### Explorar Comandos

```bash
# Ver todos los comandos de exportar
>>> exportar[Ctrl+Space]
💡 Comandos disponibles con 'exportar':
  exportar_obj
  exportar_stl

# Ver comandos de edición
>>> r[Ctrl+Space]
💡 Comandos disponibles con 'r':
  r → rotar
  rd → redimensionar
  renombrar

# Ver comandos que empiezan con 'a'
>>> a[Ctrl+Space]
💡 Comandos disponibles con 'a':
  agregar_cama
  agregar_cocina
  agregar_heladera
  ...
```

---

## 💡 Tips

### 1. Usar Autocompletado para Aprender

```bash
# No recuerdas el comando exacto?
>>> agr[Ctrl+Space]
# Te muestra todas las opciones
```

### 2. Combinar con Ayuda Contextual

```bash
# Autocompletar
>>> redim[Ctrl+Space]
Campo: redimensionar 

# Luego ver sintaxis
>>> redimensionar
ℹ️  redimensionar <nombre> <dw> <dd> <dh>
  Cambio RELATIVO en dimensiones
```

### 3. Prefijo Común

```bash
>>> agregar_c[Ctrl+Space]
💡 Comandos disponibles:
  agregar_cama
  agregar_cocina

# Completa hasta 'agregar_c'
# Agrega una letra más:
>>> agregar_ca[Ctrl+Space]
# Ahora completa a 'agregar_cama'
```

---

## 🔍 Comparación Antes/Después

### Ayuda

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Comandos mostrados | ~10 | TODOS (~30+) |
| Sintaxis | Parcial | Completa |
| Scroll | No | ✓ Sí |
| Organización | Básica | Por categorías |
| Abreviaturas | Pocas | Todas |

### Autocompletado

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Tecla | Tab (conflicto) | Ctrl+Space |
| Función | No disponible | ✓ Funciona |
| Múltiples matches | N/A | Muestra opciones |
| Abreviaturas | N/A | Incluidas |

---

## ⌨️ Atajos de Teclado Completos

```
F1              Ayuda (toggle)
F2              Vista Planta
F3              Vista Norte
F4              Vista Sur
F5              Vista Este
F6              Vista Oeste
Ctrl+E          Exportar STL (diálogo)
Ctrl+Space      Autocompletar comando
↑↓              Historial (sin objeto seleccionado)
←→↑↓            Redimensionar (con objeto seleccionado)
Enter           Ejecutar comando
```

---

## 🎨 Formato del Panel de Ayuda

El panel usa:
- **Fuente**: Courier 8 (monoespaciada)
- **Wrap**: NONE (permite scroll horizontal)
- **Formato**: Alineado en columnas
- **Separadores**: Líneas dobles (═) para secciones
- **Abreviaturas**: Entre paréntesis después del comando

---

## 📋 Lista Completa de Comandos

### Espacio
- nuevo, cargar, guardar, listar, salir

### Muebles
- agregar_cama, agregar_puerta, agregar_ventana
- agregar_heladera, agregar_cocina, agregar_pileta, agregar_mesada
- agregar_mueble

### Edición
- select, unselect, mover, rotar, redimensionar
- renombrar, color, eliminar

### Exportar
- exportar_stl, exportar_obj

### Navegación
- F1-F6, Ctrl+E

### Total: ~25 comandos principales + abreviaturas

---

## 🐛 Solución de Problemas

### "Ctrl+Space no funciona"

**Prueba**:
1. Asegúrate de que el foco está en el campo de comandos
2. Presiona Ctrl y Space al mismo tiempo
3. Si no funciona, puede ser conflicto con tu sistema operativo

**Alternativa**: Escribe el comando completo o usa ayuda contextual

### "No veo toda la ayuda"

**Solución**:
- Usa la barra de scroll en el panel de ayuda
- El panel es scrollable vertical y horizontalmente
- Presiona F1 para maximizar el panel

### "Tab sigue moviéndose entre botones"

**Es correcto**: Tab se usa para navegación de interfaz
**Usa**: Ctrl+Space para autocompletar comandos

---

## ✅ Checklist de Mejoras

- [✓] Panel de ayuda con TODOS los comandos
- [✓] Ayuda scrollable (vertical y horizontal)
- [✓] Autocompletado con Ctrl+Space
- [✓] Muestra opciones si hay múltiples matches
- [✓] Incluye abreviaturas en autocompletado
- [✓] Completa hasta prefijo común
- [✓] No interfiere con Tab (navegación de interfaz)
- [✓] Mensaje de bienvenida actualizado

---

**¡Ayuda completa y autocompletado funcionando!** 📚⚡
