# 🚪 Sistema Completo de Puertas - Room Designer v2.2

## ✅ Sistema Final con Bisagras

Ahora las puertas tienen **3 parámetros** que definen completamente su comportamiento:

1. **Orientación**: ¿La puerta es horizontal o vertical?
2. **Bisagras**: ¿De qué lado están las bisagras?
3. **Swing**: ¿Hacia dónde abre la puerta?

---

## 📋 Sintaxis Completa

```bash
agregar_puerta <x> <y> [z] [ancho] [orientación] [bisagra] [swing] [nombre]
```

### Parámetros

| Parámetro | Opciones | Descripción |
|-----------|----------|-------------|
| **orientación** | `horizontal` \| `vertical` | Dirección del ancho de la puerta |
| **bisagra** (horizontal) | `izquierda` \| `derecha` | Dónde están las bisagras |
| **bisagra** (vertical) | `arriba` \| `abajo` | Dónde están las bisagras |
| **swing** (horizontal) | `norte` \| `sur` | Hacia dónde abre |
| **swing** (vertical) | `este` \| `oeste` | Hacia dónde abre |

---

## 🎯 Puertas Horizontales (Ancho en X)

### En Pared Inferior (y=0)

```
         NORTE (↑)
            │
    ┌───────┼───────┐
    │               │
    │               │
════╧═══════════════╧════ (pared y=0)
 bisagra         bisagra
izquierda       derecha
```

#### Ejemplos:

```bash
# Bisagras a la DERECHA, abre NORTE (hacia arriba)
>>> agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada1

# Bisagras a la IZQUIERDA, abre NORTE (hacia arriba)  
>>> agregar_puerta 4 0 0 0.9 horizontal izquierda norte entrada2

# Bisagras a la DERECHA, abre SUR (hacia abajo - raro pero posible)
>>> agregar_puerta 6 0 0 0.9 horizontal derecha sur sótano
```

### En Pared Superior (y=max)

```bash
# Bisagras a la DERECHA, abre SUR (hacia abajo)
>>> agregar_puerta 2 6.9 0 0.9 horizontal derecha sur salida_jardín

# Bisagras a la IZQUIERDA, abre SUR (hacia abajo)
>>> agregar_puerta 4 6.9 0 0.9 horizontal izquierda sur terraza
```

---

## 🎯 Puertas Verticales (Ancho en Y)

### En Pared Izquierda (x=0)

```
        │ bisagra
        │ arriba
        ╧
    ════╪════ OESTE (→)
        ╤
        │ bisagra  
        │ abajo
```

#### Ejemplos:

```bash
# Bisagras ABAJO, abre OESTE (hacia derecha)
>>> agregar_puerta 0 2 0 0.9 vertical abajo oeste cocina

# Bisagras ARRIBA, abre OESTE (hacia derecha)
>>> agregar_puerta 0 4 0 0.9 vertical arriba oeste baño

# Bisagras ABAJO, abre ESTE (hacia izquierda - raro pero posible)
>>> agregar_puerta 0 6 0 0.9 vertical abajo este armario
```

### En Pared Derecha (x=max)

```bash
# Bisagras ABAJO, abre ESTE (hacia izquierda)
>>> agregar_puerta 6.9 2 0 0.9 vertical abajo este balcón

# Bisagras ARRIBA, abre ESTE (hacia izquierda)
>>> agregar_puerta 6.9 4 0 0.9 vertical arriba este estudio
```

---

## 💡 Guía Rápida de Decisión

### Paso 1: ¿Horizontal o Vertical?
- ¿La puerta está en una pared horizontal (arriba/abajo)? → `horizontal`
- ¿La puerta está en una pared vertical (izquierda/derecha)? → `vertical`

### Paso 2: ¿Dónde están las bisagras?
**Para horizontal:**
- ¿Las bisagras están del lado izquierdo de la puerta? → `izquierda`
- ¿Las bisagras están del lado derecho de la puerta? → `derecha`

**Para vertical:**
- ¿Las bisagras están en la parte de arriba? → `arriba`
- ¿Las bisagras están en la parte de abajo? → `abajo`

### Paso 3: ¿Hacia dónde abre?
**Para horizontal:**
- ¿Abre hacia el interior de la habitación (norte, +Y)? → `norte`
- ¿Abre hacia afuera (sur, -Y)? → `sur`

**Para vertical:**
- ¿Abre hacia la derecha (oeste, +X)? → `oeste`
- ¿Abre hacia la izquierda (este, -X)? → `este`

---

## 🏠 Casos de Uso Comunes

### Dormitorio Estándar

```bash
>>> nuevo 4 5 2.8

# Puerta principal: horizontal en pared inferior
# Bisagras a la izquierda para que no choque con el ropero
# Abre hacia dentro (norte)
>>> agregar_puerta 1.5 0 0 0.9 horizontal izquierda norte entrada

# Placard: vertical en pared izquierda
# Bisagras abajo, abre hacia la derecha
>>> agregar_puerta 0 2 0 0.7 vertical abajo oeste placard

>>> agregar_cama 0.5 1.5 0 1.4 1.9 cama
>>> agregar_ropero 2.5 3.5 0 1.5 0.6 2.2 ropero
```

### Cocina con Dos Accesos

```bash
>>> nuevo 3.5 4.5 2.8

# Entrada desde pasillo: horizontal, bisagras derecha
>>> agregar_puerta 1.5 0 0 0.8 horizontal derecha norte entrada_pasillo

# Salida al patio: horizontal en pared superior, bisagras izquierda
>>> agregar_puerta 1 4.4 0 0.9 horizontal izquierda sur puerta_patio

>>> agregar_heladera 0 0 0 0.7 0.7 1.8 heladera
>>> agregar_mesada_L 0.8 0 0 2.5 2.5 0.6 mesada
```

### Baño con Puerta Corrediza Simulada

```bash
>>> nuevo 2 3 2.8

# Puerta: vertical, bisagras abajo, abre hacia adentro
>>> agregar_puerta 0 1 0 0.8 vertical abajo oeste puerta_baño

# (Para puerta corrediza real, usar un objeto personalizado)
```

---

## 📊 Matriz de Combinaciones

### Puertas Horizontales

| Bisagras | Swing | Resultado Visual |
|----------|-------|------------------|
| derecha | norte | Abre hacia arriba, pivote derecho |
| derecha | sur | Abre hacia abajo, pivote derecho |
| izquierda | norte | Abre hacia arriba, pivote izquierdo |
| izquierda | sur | Abre hacia abajo, pivote izquierdo |

### Puertas Verticales

| Bisagras | Swing | Resultado Visual |
|----------|-------|------------------|
| abajo | oeste | Abre hacia derecha, pivote abajo |
| abajo | este | Abre hacia izquierda, pivote abajo |
| arriba | oeste | Abre hacia derecha, pivote arriba |
| arriba | este | Abre hacia izquierda, pivote arriba |

**Total: 8 configuraciones posibles**

---

## 🎨 Diferencias Visuales

En la vista de planta verás claramente:

1. **Marco de la puerta**: Rectángulo que muestra la ubicación
2. **Punto de pivote**: Donde están las bisagras (marcado como inicio del arco)
3. **Arco punteado**: Muestra el rango completo de apertura (90°)
4. **Línea sólida**: Muestra la puerta en posición completamente abierta

### Ejemplo Visual:

```
Puerta horizontal, bisagras derecha, abre norte:

        ╱ (línea = puerta abierta)
      ╱ 
    ╱  ¨¨¨ (arco punteado = rango)
   ╱¨¨
  ╱¨
══════╧══════ (marco, ╧ = bisagra)
      pivote→
```

---

## ⚠️ Configuraciones Raras (Pero Válidas)

Algunas combinaciones son técnicamente posibles pero poco comunes:

```bash
# Puerta que abre "hacia afuera" de una pared inferior (sur)
>>> agregar_puerta 2 0 0 0.9 horizontal derecha sur salida_emergencia

# Puerta que abre "hacia atrás" en pared izquierda (este)
>>> agregar_puerta 0 2 0 0.9 vertical abajo este armario_empotrado
```

Estas configuraciones funcionan pero son inusuales en diseño real.

---

## 🔄 Migración desde Versión 2.1

### Antes (v2.1):
```bash
agregar_puerta 2 0 0 0.9 horizontal norte entrada
# Asumía bisagras a la derecha
```

### Ahora (v2.2):
```bash
# Debes especificar las bisagras explícitamente
agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada
```

Los valores por defecto son:
- Orientación: `horizontal`
- Bisagra: `derecha` (horizontal) o `abajo` (vertical)
- Swing: `norte` (horizontal) o `oeste` (vertical)

---

## ✅ Verificación del Sistema

Para probar todas las combinaciones:

```bash
./room_designer.py

>>> nuevo 10 10 2.8

# Horizontal - 4 combinaciones
>>> agregar_puerta 1 0 0 0.9 horizontal derecha norte h_der_n
>>> agregar_puerta 3 0 0 0.9 horizontal izquierda norte h_izq_n
>>> agregar_puerta 5 0 0 0.9 horizontal derecha sur h_der_s
>>> agregar_puerta 7 0 0 0.9 horizontal izquierda sur h_izq_s

# Vertical - 4 combinaciones
>>> agregar_puerta 0 1 0 0.9 vertical abajo oeste v_aba_o
>>> agregar_puerta 0 3 0 0.9 vertical arriba oeste v_arr_o
>>> agregar_puerta 0 5 0 0.9 vertical abajo este v_aba_e
>>> agregar_puerta 0 7 0 0.9 vertical arriba este v_arr_e

>>> vista_planta test_puertas.png
```

---

## 🎓 Resumen

**3 parámetros = Control Total:**

1. **Orientación** (horizontal/vertical) → Define en qué tipo de pared está
2. **Bisagra** (izq/der o arriba/abajo) → Define de qué lado pivotea
3. **Swing** (norte/sur o este/oeste) → Define hacia dónde se abre

Esto te permite representar **cualquier puerta real** con precisión arquitectónica.

---

**Room Designer v2.2** - Sistema Completo de Puertas  
Febrero 2026

¡Ahora sí todas las puertas posibles! 🚪✨
