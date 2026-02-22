# 🎮 Mejoras de Interfaz - Flechas y Guardar al Salir

## ✅ Cambios Implementados

### 1. **Flechas ↑↓ Inteligentes** 🎯
Las flechas arriba/abajo ahora tienen **dos modos**:
- **Modo Historial** (por defecto): Navegan comandos anteriores
- **Modo Redimensionar** (con objeto seleccionado): Cambian dimensiones

### 2. **Guardar al Salir** 💾
Al cerrar el programa (comando `salir` o botón X), pregunta si quieres guardar los cambios

---

## 🎯 Cambio 1: Flechas Inteligentes

### Problema Anterior
Las flechas ↑↓ estaban **siempre** atadas al historial de comandos, lo que impedía usarlas para redimensionar.

### Solución
Sistema de **bindings dinámicos** que cambia según el contexto:

#### **Sin objeto seleccionado** (modo por defecto)
```bash
↑  # Comando anterior
↓  # Comando siguiente
←→ # No hacen nada
```

#### **Con objeto seleccionado** (modo redimensionar)
```bash
>>> select mesa
✓ 'mesa' seleccionado
  Flechas: redimensionar (↑↓ deshabilitadas para historial)
  Usar 'unselect' para restaurar historial

# Ahora las 4 flechas controlan dimensiones
↑↓←→  # Redimensionan según la vista activa
```

---

## 📖 Uso de Flechas

### Activar Modo Redimensionar
```bash
>>> select cama
✓ 'cama' seleccionado
  Flechas: redimensionar (↑↓ deshabilitadas para historial)
  
# Ahora usa flechas para cambiar tamaño
>>> [F2]  # Vista planta
>>> [→→→]  # +0.03m ancho
>>> [↓↓]    # +0.02m profundidad
```

### Desactivar Modo Redimensionar
```bash
>>> unselect
✓ 'cama' deseleccionado
  Flechas ↑↓ restauradas para historial de comandos

# O abreviado:
>>> us
```

### Resumen de Comandos

| Comando | Abrev | Efecto |
|---------|-------|--------|
| `select <nombre>` | `s` | Selecciona objeto, activa modo redimensionar |
| `unselect` | `us` | Deselecciona objeto, restaura historial |

---

## 🎮 Tabla de Flechas por Modo

### Modo Historial (sin objeto seleccionado)
```
↑  = Comando anterior
↓  = Comando siguiente
←  = (sin uso)
→  = (sin uso)
```

### Modo Redimensionar (con objeto seleccionado)

#### Vista Planta (F2)
```
↑  = -0.01m depth
↓  = +0.01m depth
←  = -0.01m width
→  = +0.01m width
```

#### Vistas Norte/Sur (F3/F4)
```
↑  = +0.01m height
↓  = -0.01m height
←  = -0.01m width
→  = +0.01m width
```

#### Vistas Este/Oeste (F5/F6)
```
↑  = +0.01m height
↓  = -0.01m height
←  = -0.01m depth
→  = +0.01m depth
```

---

## 💾 Cambio 2: Guardar al Salir

### Comportamiento

#### Caso 1: Espacio vacío o sin diseño
```bash
>>> salir
[Diálogo: "¿Salir del programa?"]
[Sí] → Cierra
[No] → Cancela
```

#### Caso 2: Hay objetos en el diseño
```bash
>>> salir
[Diálogo: "¿Desea guardar los cambios antes de salir?"]

[Sí] → [Pide nombre archivo] → Guarda → Cierra
[No] → Cierra sin guardar
[Cancelar] → No cierra
```

### Ejemplo de Flujo Completo

```bash
# 1. Trabajar en el diseño
>>> n 5 5
>>> c 1 1
>>> h 0 0

# 2. Intentar salir
>>> salir

# 3. Diálogo aparece:
┌─────────────────────────────────┐
│  Guardar cambios                │
│                                 │
│  ¿Desea guardar los cambios     │
│  antes de salir?                │
│                                 │
│  [Sí]  [No]  [Cancelar]        │
└─────────────────────────────────┘

# 4. Si presionas [Sí]:
┌─────────────────────────────────┐
│  Guardar diseño                 │
│                                 │
│  Nombre: [mi_cocina.json____]   │
│                                 │
│  [Guardar]  [Cancelar]         │
└─────────────────────────────────┘

# 5. Después de guardar:
✓ Diseño guardado en: /ruta/mi_cocina.json
[Programa se cierra]
```

### Cerrar con Botón X

También funciona cuando cierras la ventana con la X:

```
[Click en X de la ventana]
↓
[Mismo diálogo de "¿Guardar cambios?"]
↓
[Mismas opciones: Sí/No/Cancelar]
```

---

## 🔄 Workflow Típico

### Sesión Normal con Guardado

```bash
# 1. Crear diseño
>>> n 4 4
>>> h 0 0 heladera
>>> c 2 2 cama

# 2. Ajustar con flechas
>>> s heladera
>>> [F3]  # Vista norte
>>> [↑↑↑↑↑]  # Hacer más alta
>>> us  # Restaurar historial

# 3. Más comandos
>>> ↑  # Ahora funciona el historial
>>> [Enter]  # Repite último comando

# 4. Salir
>>> salir
[¿Guardar? Sí]
[Nombre: cocina.json]
✓ Guardado y cerrado
```

### Sesión de Prueba sin Guardar

```bash
# 1. Probar algo rápido
>>> n 3 3
>>> c 1 1

# 2. No me gusta, salir sin guardar
>>> salir
[¿Guardar? No]
[Cierra sin guardar]
```

---

## 💡 Ventajas

### Flechas Inteligentes
- ✅ **Historial accesible**: Por defecto funcionan para comandos
- ✅ **Redimensionar cuando necesitas**: Select para activar modo
- ✅ **Fácil cambio**: `unselect` o `us` para volver
- ✅ **Intuitivo**: El mensaje te dice qué está activo

### Guardar al Salir
- ✅ **No pierdes trabajo**: Siempre pregunta si hay cambios
- ✅ **Rápido**: Solo 2 clicks para guardar y salir
- ✅ **Flexible**: Puedes cancelar si te arrepientes
- ✅ **Seguro**: Funciona con comando `salir` Y con botón X

---

## 🎯 Comparación Antes/Después

### Flechas

| Situación | Antes | Ahora |
|-----------|-------|-------|
| Sin objeto seleccionado | ↑↓ = historial | ↑↓ = historial ✓ |
| Con objeto seleccionado | ↑↓ = historial (NO podías redimensionar) | ↑↓ = redimensionar ✓ |
| Volver a historial | N/A | `unselect` ✓ |

### Salir

| Acción | Antes | Ahora |
|--------|-------|-------|
| Comando `salir` | Solo pregunta "¿Salir?" | Pregunta "¿Guardar cambios?" ✓ |
| Botón X | Cierra sin preguntar | Pregunta "¿Guardar cambios?" ✓ |
| Guardar al salir | Manual (antes de salir) | Automático (te ofrece) ✓ |

---

## ⚠️ Notas Importantes

### Flechas
1. **Indicador visual**: Cuando seleccionas un objeto, el mensaje dice "↑↓ deshabilitadas para historial"
2. **Restaurar**: Siempre puedes hacer `unselect` para volver al modo historial
3. **Persistente**: El modo redimensionar se mantiene hasta que hagas `unselect`

### Guardar
1. **Solo pregunta si hay objetos**: Si el espacio está vacío, sale directamente
2. **Tres opciones**: Sí (guarda y sale), No (sale sin guardar), Cancelar (no sale)
3. **Elige nombre**: Si guardas, te deja elegir el nombre del archivo
4. **Confirmación**: Te muestra un mensaje de éxito después de guardar

---

## 🐛 Solución de Problemas

### "Las flechas ↑↓ no funcionan para redimensionar"
**Causa**: No hay objeto seleccionado
**Solución**:
```bash
>>> s nombre_objeto
>>> [ahora usa flechas]
```

### "Las flechas ↑↓ no funcionan para historial"
**Causa**: Hay un objeto seleccionado
**Solución**:
```bash
>>> us
>>> [ahora funciona historial]
```

### "No me pregunta si guardar al salir"
**Causa**: El espacio está vacío (sin objetos)
**Solución**: Es normal, solo pregunta si hay algo que guardar

### "Cancelé el guardar pero el programa se cerró"
**Causa**: Presionaste "No" en lugar de "Cancelar"
**Solución**: 
- "Sí" = guardar y salir
- "No" = salir SIN guardar
- "Cancelar" = NO salir

---

## 📋 Resumen Rápido

```bash
# FLECHAS
select <obj>  # Activa modo redimensionar (↑↓ para dimensiones)
unselect      # Activa modo historial (↑↓ para comandos)

# SALIR
salir         # Pregunta si guardar antes de salir
[X]           # Mismo comportamiento al cerrar ventana

# ABREVIATURAS
s = select
us = unselect
```

---

**¡Interfaz mejorada para mejor experiencia!** 🎉
