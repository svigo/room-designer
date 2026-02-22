# 🚀 Guía Rápida - Exportar OBJ con Colores

## ✅ Comandos Disponibles

### STL (sin colores)
```bash
exportar_stl cocina.stl
# O abreviado:
e cocina.stl
```

### OBJ con COLORES ⭐
```bash
exportar_obj cocina
# O abreviado:
obj cocina
```

**Nota**: No pongas la extensión en OBJ, el programa genera automáticamente:
- `cocina.obj` (geometría)
- `cocina.mtl` (colores)

---

## 📖 Ejemplo Completo

```bash
# Iniciar la GUI
python3 room_designer_gui.py

# En la consola de comandos:
>>> cargar cocina1.json
✓ Diseño cargado

>>> exportar_obj cocina
✓ Exportado OBJ con colores:
  cocina.obj
  cocina.mtl
  Materiales: 4
  Puertas: 1, Ventanas: 1, Muebles: 0

# Ahora tienes cocina.obj y cocina.mtl con colores
```

---

## 🎨 Qué Incluye el OBJ

✅ **Piso** (forma L completa) - Color beige
✅ **6 Paredes** verticales - Color gris  
✅ **Puerta** - Color marrón
✅ **Ventana** - Color azul
✅ **Espejo corregido** (norte en su lugar)

---

## 🔍 Verificar que Tienes la Versión Correcta

Si el comando `exportar_obj` no funciona:

1. **Copia los archivos actualizados**:
   - `room_designer.py` 
   - `room_designer_gui.py`
   
2. **Desde el directorio donde están los archivos**:
   ```bash
   python3 room_designer_gui.py
   ```

3. **Verifica la versión** - Al inicio debe decir:
   ```
   ============================================================
   ROOM DESIGNER v3.2 FINAL
   ============================================================
   ✓ Exportar STL: exportar_stl o e
   ✓ Exportar OBJ con colores: exportar_obj o obj
   ✓ Grid 0.1m + Coords visibles
   ```

---

## 📝 Todos los Comandos de Exportación

| Comando | Abrev | Descripción |
|---------|-------|-------------|
| `exportar_stl archivo.stl` | `e archivo.stl` | STL sin colores |
| `exportar_obj nombre` | `obj nombre` | OBJ+MTL con colores |

**Ejemplos**:
```bash
# STL
>>> exportar_stl mi_cocina.stl
>>> e modelo.stl

# OBJ (CON COLORES)
>>> exportar_obj mi_cocina
>>> obj cocina_completa
```

---

## 🎯 Ayuda Contextual

Si olvidas la sintaxis, escribe solo el comando:

```bash
>>> exportar_obj

ℹ️  exportar_obj [nombre_base]
  Exporta OBJ+MTL (CON COLORES)
  Ej: exportar_obj cocina
  Genera: cocina.obj y cocina.mtl
```

---

## 🖥️ Abrir los Archivos

### OBJ con colores:
- **MeshLab** (mejor para ver colores)
- **Blender** (edición completa)
- **Online**: https://3dviewer.net

### STL:
- **3D Viewer** (Windows)
- **Preview** (macOS)
- **MeshLab** (todos)

---

## ⚠️ Solución de Problemas

### "Comando desconocido: exportar_obj"

**Causa**: Estás usando archivos viejos

**Solución**:
1. Asegúrate de tener los archivos de `/mnt/user-data/outputs/`
2. Reinicia la GUI
3. Al inicio debe decir "v3.2 FINAL" y mencionar `exportar_obj`

### "No se ven las paredes en el OBJ"

**Causa**: Versión vieja del código

**Solución**: 
- Usa `room_designer.py` actualizado
- El OBJ debe reportar "Materiales: 4" (floor, wall, door, window)
- Si reporta "Materiales: 2", tienes la versión vieja

---

## ✅ Checklist

- [ ] Archivos actualizados de `/mnt/user-data/outputs/`
- [ ] Al iniciar dice "v3.2 FINAL"
- [ ] Menciona "exportar_obj o obj"
- [ ] Comando `obj cocina` funciona
- [ ] Genera 2 archivos: .obj y .mtl
- [ ] OBJ muestra paredes, piso, puerta y ventana
- [ ] Colores visibles en MeshLab/Blender

---

**¡Listo! Ahora puedes exportar tu cocina con colores** 🎨
