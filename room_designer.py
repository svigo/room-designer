#!/usr/bin/env python3
"""
Room Designer - Diseñador de cocinas y dormitorios por línea de comandos
Con visualización gráfica en imágenes PNG
"""

import json
import struct
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import os
import time

# Variable global para control de visualización en tiempo real
VISUALIZACION_ACTIVA = None  # None, 'planta', 'lateral', '3d'
VENTANA_VISUALIZACION = None

# Lista de todos los comandos disponibles
COMANDOS_DISPONIBLES = [
    'nuevo', 'nuevo_irregular',
    'agregar_cama', 'agregar_cucheta', 'agregar_ropero', 'agregar_mesa_luz', 'agregar_mesa',
    'agregar_heladera', 'agregar_cocina', 'agregar_pileta', 'agregar_alacena', 
    'agregar_mesada', 'agregar_mesada_L', 'agregar_personalizado',
    'agregar_puerta', 'agregar_ventana',
    'mover', 'rotar', 'eliminar', 'listar',
    'agrupar', 'desagrupar', 'mover_grupo', 'listar_grupos',
    'vista_planta', 'vista_lateral', 'vista_3d',
    'exportar_stl', 'importar_stl',
    'guardar', 'cargar',
    'activar_viz_planta', 'activar_viz_lateral', 'activar_viz_3d', 'desactivar_viz',
    'ayuda', 'salir'
]

# Ayuda rápida para cada comando
AYUDA_COMANDOS = {
    'nuevo': 'nuevo <ancho> <largo> [altura] - Ejemplo: nuevo 4 5 2.8',
    'nuevo_irregular': 'nuevo_irregular <altura> <x1,y1> <x2,y2> <x3,y3> ... - Ejemplo: nuevo_irregular 2.8 0,0 4,0 4,3 2,3 2,5 0,5',
    'agregar_cama': 'agregar_cama <x> <y> [z] [ancho] [largo] [nombre] - Ejemplo: agregar_cama 0.5 1.0 0 1.4 1.9 cama',
    'agregar_cucheta': 'agregar_cucheta <x> <y> [z] [ancho] [largo] [nombre] - Ejemplo: agregar_cucheta 0.5 1.0 0 1.0 2.0 cucheta',
    'agregar_ropero': 'agregar_ropero <x> <y> [z] [ancho] [prof] [alto] [nombre] - Ejemplo: agregar_ropero 0 3.5 0 2.0 0.6 2.2 ropero',
    'agregar_mesa_luz': 'agregar_mesa_luz <x> <y> [z] [ancho] [prof] [nombre] - Ejemplo: agregar_mesa_luz 2.0 0.5 0 0.5 0.4 mesa',
    'agregar_mesa': 'agregar_mesa <x> <y> [z] [ancho] [prof] [nombre] - Ejemplo: agregar_mesa 2.5 1.0 0 1.2 0.8 escritorio',
    'agregar_heladera': 'agregar_heladera <x> <y> [z] [ancho] [prof] [alto] [nombre] - Ejemplo: agregar_heladera 0 0 0 0.7 0.7 1.8 heladera',
    'agregar_cocina': 'agregar_cocina <x> <y> [z] [ancho] [prof] [nombre] - Ejemplo: agregar_cocina 0.8 0 0.9 0.6 0.6 cocina',
    'agregar_pileta': 'agregar_pileta <x> <y> [z] [ancho] [prof] [nombre] - Ejemplo: agregar_pileta 2.0 0 0.9 0.8 0.6 pileta',
    'agregar_alacena': 'agregar_alacena <x> <y> [z] [ancho] [prof] [alto] [nombre] - Ejemplo: agregar_alacena 0.8 0 1.9 2.7 0.35 0.7 alacenas',
    'agregar_mesada': 'agregar_mesada <x> <y> [z] [ancho] [prof] [nombre] - Ejemplo: agregar_mesada 0.8 0 0 2.5 0.6 mesada',
    'agregar_mesada_L': 'agregar_mesada_L <x> <y> [z] [ancho1] [ancho2] [prof] [nombre] - Ejemplo: agregar_mesada_L 0.8 0 0 2.5 2.0 0.6 mesada_L',
    'agregar_personalizado': 'agregar_personalizado <nombre> <z> <altura> <x1,y1> <x2,y2> ... - Ejemplo: agregar_personalizado isla 0 0.9 1,1 2,1 2,2 1,2',
    'agregar_puerta': 'agregar_puerta <x> <y> [z] [ancho] [orientación] [bisagra] [swing] [nombre] - Orientación: horizontal|vertical, Bisagra horizontal: izquierda|derecha, Bisagra vertical: arriba|abajo, Swing horizontal: norte|sur, Swing vertical: este|oeste - Ejemplo: agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada',
    'agregar_ventana': 'agregar_ventana <x> <y> [z] [ancho] [alto] [nombre] - Ejemplo: agregar_ventana 1 0 1.2 1.5 1.0 ventana',
    'mover': 'mover <nombre> <x> <y> <z> - Ejemplo: mover cama 1.0 1.5 0',
    'rotar': 'rotar <nombre> - Ejemplo: rotar ropero',
    'eliminar': 'eliminar <nombre> - Ejemplo: eliminar mesa_vieja',
    'listar': 'listar - Muestra todos los objetos en el espacio',
    'agrupar': 'agrupar <nombre_grupo> <obj1> <obj2> <obj3> ... - Ejemplo: agrupar zona_dormir cama mesa_izq mesa_der',
    'desagrupar': 'desagrupar <nombre_grupo> - Ejemplo: desagrupar zona_dormir',
    'mover_grupo': 'mover_grupo <nombre_grupo> <dx> <dy> <dz> - Ejemplo: mover_grupo zona_dormir 0.5 0 0',
    'listar_grupos': 'listar_grupos - Muestra todos los grupos creados',
    'vista_planta': 'vista_planta [archivo] - Ejemplo: vista_planta planta.png',
    'vista_lateral': 'vista_lateral [archivo] - Ejemplo: vista_lateral elevacion.png',
    'vista_3d': 'vista_3d [archivo] - Ejemplo: vista_3d perspectiva.png',
    'exportar_stl': 'exportar_stl [archivo] - Ejemplo: exportar_stl dormitorio.stl',
    'importar_stl': 'importar_stl <archivo> [nombre] [x] [y] [z] - Ejemplo: importar_stl silla.stl silla_1 1.0 2.0 0',
    'guardar': 'guardar [archivo] - Ejemplo: guardar mi_diseño.json',
    'cargar': 'cargar <archivo> - Ejemplo: cargar mi_diseño.json',
    'activar_viz_planta': 'activar_viz_planta - Activa visualización de planta en tiempo real',
    'activar_viz_lateral': 'activar_viz_lateral - Activa visualización lateral en tiempo real',
    'activar_viz_3d': 'activar_viz_3d - Activa visualización 3D en tiempo real',
    'desactivar_viz': 'desactivar_viz - Desactiva visualización en tiempo real',
    'ayuda': 'ayuda - Muestra todos los comandos disponibles',
    'salir': 'salir - Termina el programa'
}

class RoomDesignerCompleter:
    """Clase para autocompletado de comandos"""
    def __init__(self, commands):
        self.commands = commands
        self.matches = []
    
    def complete(self, text, state):
        if state == 0:
            # Primera vez que se llama para este texto
            if text:
                self.matches = [cmd for cmd in self.commands if cmd.startswith(text)]
            else:
                self.matches = self.commands[:]
        
        try:
            return self.matches[state]
        except IndexError:
            return None

class STLWriter:
    """Escritor de archivos STL en formato binario"""
    
    @staticmethod
    def write_binary_stl(filename, triangles):
        """
        Escribe un archivo STL binario
        triangles: lista de triángulos, cada uno con 3 vértices [[v1, v2, v3], ...]
        """
        with open(filename, 'wb') as f:
            # Header (80 bytes)
            header = b'Binary STL created by Room Designer' + b' ' * 45
            f.write(header)
            
            # Número de triángulos
            f.write(struct.pack('<I', len(triangles)))
            
            # Escribir cada triángulo
            for tri in triangles:
                # Normal (calculada automáticamente)
                v1, v2, v3 = tri
                normal = STLWriter.calculate_normal(v1, v2, v3)
                
                # Normal
                f.write(struct.pack('<fff', *normal))
                
                # Vértices
                for vertex in tri:
                    f.write(struct.pack('<fff', *vertex))
                
                # Attribute byte count (2 bytes, siempre 0)
                f.write(struct.pack('<H', 0))
    
    @staticmethod
    def calculate_normal(v1, v2, v3):
        """Calcula la normal de un triángulo"""
        # Vectores del triángulo
        u = [v2[i] - v1[i] for i in range(3)]
        v = [v3[i] - v1[i] for i in range(3)]
        
        # Producto cruz
        normal = [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        ]
        
        # Normalizar
        length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
        if length > 0:
            normal = [n / length for n in normal]
        
        return normal


class RoomDesigner:
    def __init__(self, width=4.0, length=5.0, height=2.8, vertices=None):
        """
        Inicializa un nuevo espacio
        
        Args:
            width: Ancho del cuarto en metros (si es rectangular)
            length: Largo del cuarto en metros (si es rectangular)
            height: Altura del cuarto en metros
            vertices: Lista de tuplas (x,y) para habitaciones irregulares
                     Ejemplo: [(0,0), (4,0), (4,3), (2,3), (2,5), (0,5)]
        """
        if vertices is not None:
            # Habitación irregular definida por vértices
            self.vertices = vertices
            self.is_irregular = True
            # Calcular bounding box
            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]
            self.width = max(xs) - min(xs)
            self.length = max(ys) - min(ys)
        else:
            # Habitación rectangular estándar
            self.width = width
            self.length = length
            self.is_irregular = False
            self.vertices = [(0, 0), (width, 0), (width, length), (0, length)]
        
        self.height = height
        self.objects = []
        self.groups = {}  # Diccionario de grupos: {nombre_grupo: [lista de nombres de objetos]}
    
    def _validar_nombre_unico(self, nombre):
        """Verifica que el nombre no esté en uso"""
        nombres_existentes = [obj['name'] for obj in self.objects]
        if nombre in nombres_existentes:
            # Generar nombre alternativo
            contador = 1
            nuevo_nombre = f"{nombre}_{contador}"
            while nuevo_nombre in nombres_existentes:
                contador += 1
                nuevo_nombre = f"{nombre}_{contador}"
            return nuevo_nombre
        return nombre
        
    def add_bed(self, x, y, z=0, width=1.0, length=2.0, name="cama"):
        """Agrega una cama simple"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'bed',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'length': length,
            'height': 0.6
        }
        self.objects.append(obj)
        self.actualizar_visualizacion()
        return f"Cama '{name}' agregada en ({x}, {y}, {z})"
    
    def add_bunk_bed(self, x, y, z=0, width=1.0, length=2.0, name="cucheta"):
        """Agrega una cama cucheta"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'bunk_bed',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'length': length,
            'height': 1.8
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Cucheta '{name}' agregada en ({x}, {y}, {z})"
    
    def add_wardrobe(self, x, y, z=0, width=1.5, depth=0.6, height=2.0, name="ropero"):
        """Agrega un ropero"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'wardrobe',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Ropero '{name}' agregado en ({x}, {y}, {z})"
    
    def add_nightstand(self, x, y, z=0, width=0.5, depth=0.4, name="mesa_luz"):
        """Agrega una mesa de luz"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'nightstand',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': 0.5
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Mesa de luz '{name}' agregada en ({x}, {y}, {z})"
    
    def add_fridge(self, x, y, z=0, width=0.7, depth=0.7, height=1.8, name="heladera"):
        """Agrega una heladera"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'fridge',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Heladera '{name}' agregada en ({x}, {y}, {z})"
    
    def add_stove(self, x, y, z=0, width=0.6, depth=0.6, name="cocina"):
        """Agrega una cocina/hornalla"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'stove',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': 0.9
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Cocina '{name}' agregada en ({x}, {y}, {z})"
    
    def add_sink(self, x, y, z=0, width=0.8, depth=0.6, name="pileta"):
        """Agrega una pileta"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'sink',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': 0.9
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Pileta '{name}' agregada en ({x}, {y}, {z})"
    
    def add_cabinet(self, x, y, z=0, width=1.0, depth=0.6, height=0.9, name="alacena"):
        """Agrega un mueble de guardado"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'cabinet',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Mueble '{name}' agregado en ({x}, {y}, {z})"
    
    def add_counter(self, x, y, z=0, width=2.0, depth=0.6, name="mesada"):
        """Agrega una mesada"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'counter',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': 0.9
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Mesada '{name}' agregada en ({x}, {y}, {z})"
    
    def add_generic_furniture(self, x, y, z=0, width=1.0, depth=0.6, height=1.0, name="mueble", furniture_type="generic"):
        """
        Agrega un mueble genérico (prisma rectangular)
        
        Args:
            x, y: Posición en planta
            z: Altura del PISO del mueble (punto de anclaje inferior)
            width: Ancho (X)
            depth: Profundidad (Y)
            height: Altura (Z) - el mueble crece hacia arriba desde z
            name: Nombre único
            furniture_type: Tipo para identificar visualmente
        
        Nota: z es la altura del PISO del mueble, no del centro
        """
        name = self._validar_nombre_unico(name)
        obj = {
            'type': furniture_type,
            'name': name,
            'x': x, 
            'y': y, 
            'z': z,  # Z es el piso del mueble (punto de anclaje inferior)
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        self.actualizar_visualizacion()
        return f"{furniture_type.capitalize()} '{name}' agregado: {width:.2f}×{depth:.2f}×{height:.2f}m en ({x:.2f}, {y:.2f}, {z:.2f})"
    
    def add_table(self, x, y, z=0, width=1.2, depth=0.8, name="mesa"):
        """Agrega una mesa"""
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'table',
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': 0.75
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Mesa '{name}' agregada en ({x}, {y}, {z})"
    
    def add_custom_furniture(self, vertices, z=0, height=1.0, name="mueble_custom", obj_type="custom"):
        """
        Agrega un mueble con forma irregular definida por vértices
        
        Args:
            vertices: Lista de tuplas (x,y) definiendo la planta del mueble
                     Ejemplo: [(0,0), (1,0), (1,0.5), (0.5,0.5), (0.5,1), (0,1)]
            z: Altura desde el piso
            height: Altura del mueble
            name: Nombre identificador
            obj_type: Tipo de mueble (custom, counter_l, etc)
        """
        obj = {
            'type': obj_type,
            'name': name,
            'x': min(v[0] for v in vertices),  # Para referencia
            'y': min(v[1] for v in vertices),
            'z': z,
            'height': height,
            'vertices': vertices,  # Polígono 2D de la base
            'is_custom': True
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Mueble personalizado '{name}' agregado con {len(vertices)} vértices"
    
    def add_L_counter(self, x, y, z=0, width1=2.0, width2=1.5, depth=0.6, name="mesada_L"):
        """
        Agrega una mesada en forma de L
        
        Args:
            x, y: Esquina del ángulo interno de la L
            width1: Largo del brazo horizontal
            width2: Largo del brazo vertical
            depth: Profundidad de la mesada
        """
        # Crear vértices para forma de L
        vertices = [
            (x, y),
            (x + width1, y),
            (x + width1, y + depth),
            (x + depth, y + depth),
            (x + depth, y + width2),
            (x, y + width2)
        ]
        return self.add_custom_furniture(vertices, z, 0.9, name, "counter_l")
    
    def add_door(self, x, y, z=0, width=0.9, orientation='horizontal', hinge='derecha', swing='norte', name="puerta"):
        """
        Agrega una puerta con apertura direccional
        
        Args:
            x, y: Posición de la esquina de la puerta
            z: Altura desde el piso (usualmente 0)
            width: Ancho de la puerta (default: 0.9m)
            orientation: 'horizontal' o 'vertical'
                - horizontal: puerta paralela al eje X (ancho en X)
                - vertical: puerta paralela al eje Y (ancho en Y)
            hinge: Posición de las bisagras
                - Para horizontal: 'izquierda' o 'derecha'
                - Para vertical: 'arriba' o 'abajo'
            swing: Dirección de apertura (punto cardinal real)
                - Para horizontal: 'norte' (abre hacia +Y, arriba) o 'sur' (abre hacia -Y, abajo)
                - Para vertical: 'este' (abre hacia +X, derecha) o 'oeste' (abre hacia -X, izquierda)
            name: Nombre identificador
            
        Ejemplos:
            # Puerta horizontal, bisagras a la derecha, abre hacia el norte (+Y, arriba)
            add_door(2, 0, 0, 0.9, 'horizontal', 'derecha', 'norte', 'entrada')
            
            # Puerta vertical, bisagras abajo, abre hacia el este (+X, derecha)
            add_door(0, 2, 0, 0.9, 'vertical', 'abajo', 'este', 'cocina')
        """
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'door',
            'name': name,
            'x': x,
            'y': y,
            'z': z,
            'width': width,
            'height': 2.1,
            'orientation': orientation,
            'hinge': hinge,
            'swing': swing,
            'thickness': 0.1
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Puerta '{name}' agregada en ({x}, {y}, {z}) - {orientation}, bisagras: {hinge}, abre: {swing}"
    
    def add_window(self, x, y, z=1.0, width=1.2, height=1.0, name="ventana"):
        """
        Agrega una ventana
        
        Args:
            x, y: Posición de la ventana
            z: Altura desde el piso (default: 1.0m)
            width: Ancho de la ventana
            height: Alto de la ventana
            name: Nombre identificador
        """
        name = self._validar_nombre_unico(name)
        obj = {
            'type': 'window',
            'name': name,
            'x': x,
            'y': y,
            'z': z,
            'width': width,
            'height': height,
            'depth': 0.05
        }
        self.objects.append(obj)
        
        self.actualizar_visualizacion()
        return f"Ventana '{name}' agregada en ({x}, {y}, {z})"

    
    def create_group(self, group_name, object_names):
        """
        Crea un grupo de objetos para manipularlos juntos
        
        Args:
            group_name: Nombre del grupo
            object_names: Lista de nombres de objetos a agrupar
        """
        # Verificar que todos los objetos existen
        existing_objects = [obj['name'] for obj in self.objects]
        for obj_name in object_names:
            if obj_name not in existing_objects:
                return f"Error: objeto '{obj_name}' no encontrado"
        
        self.groups[group_name] = object_names
        return f"Grupo '{group_name}' creado con {len(object_names)} objetos: {', '.join(object_names)}"
    
    def ungroup(self, group_name):
        """Desagrupa un grupo de objetos"""
        if group_name not in self.groups:
            return f"Error: grupo '{group_name}' no encontrado"
        
        objects = self.groups[group_name]
        del self.groups[group_name]
        return f"Grupo '{group_name}' desagrupado ({len(objects)} objetos liberados)"
    
    def move_group(self, group_name, dx, dy, dz):
        """
        Mueve todos los objetos de un grupo
        
        Args:
            group_name: Nombre del grupo
            dx, dy, dz: Desplazamiento relativo
        """
        if group_name not in self.groups:
            return f"Error: grupo '{group_name}' no encontrado"
        
        moved_count = 0
        for obj_name in self.groups[group_name]:
            for obj in self.objects:
                if obj['name'] == obj_name:
                    obj['x'] += dx
                    obj['y'] += dy
                    obj['z'] += dz
                    moved_count += 1
                    break
        
        return f"Grupo '{group_name}' movido ({moved_count} objetos desplazados en Δx={dx}, Δy={dy}, Δz={dz})"
    
    def list_groups(self):
        """Lista todos los grupos creados"""
        if not self.groups:
            return "No hay grupos creados"
        
        result = f"\n{'='*70}\nGRUPOS CREADOS\n{'='*70}\n"
        for group_name, objects in self.groups.items():
            result += f"\n{group_name}:\n"
            result += f"  Objetos ({len(objects)}): {', '.join(objects)}\n"
        return result
    
    def move(self, name, dx, dy, dz):
        """Mueve un objeto con desplazamiento relativo (dx, dy, dz)"""
        for obj in self.objects:
            if obj['name'] == name:
                obj['x'] += dx
                obj['y'] += dy
                obj['z'] += dz
                self.actualizar_visualizacion()
                return f"'{name}' movido (Δx={dx}, Δy={dy}, Δz={dz}) → nueva pos: ({obj['x']:.2f}, {obj['y']:.2f}, {obj['z']:.2f})"
        return f"Error: objeto '{name}' no encontrado"
    
    def rotate(self, name, angle=90):
        """Rota un objeto 90 grados (intercambia width y depth/length)"""
        for obj in self.objects:
            if obj['name'] == name:
                if 'width' in obj and 'depth' in obj:
                    obj['width'], obj['depth'] = obj['depth'], obj['width']
                elif 'width' in obj and 'length' in obj:
                    obj['width'], obj['length'] = obj['length'], obj['width']
                self.actualizar_visualizacion()
                return f"'{name}' rotado {angle}°"
        return f"Error: objeto '{name}' no encontrado"
    
    def resize(self, name, dwidth, ddepth, dheight):
        """
        Redimensiona un objeto con cambios relativos (delta)
        
        Args:
            name: Nombre del objeto
            dwidth: Cambio en ancho (puede ser negativo)
            ddepth: Cambio en profundidad/largo (puede ser negativo)
            dheight: Cambio en altura (puede ser negativo)
        
        Returns:
            Mensaje con el resultado
        """
        MIN_DIM = 0.01  # Dimensión mínima: 1cm
        
        for obj in self.objects:
            if obj['name'] == name:
                # Obtener dimensiones actuales
                old_w = obj.get('width', 1.0)
                old_d = obj.get('depth', obj.get('length', 1.0))
                old_h = obj.get('height', 1.0)
                
                # Calcular nuevas dimensiones
                new_w = old_w + dwidth
                new_d = old_d + ddepth
                new_h = old_h + dheight
                
                # Aplicar límite mínimo
                new_w = max(MIN_DIM, new_w)
                new_d = max(MIN_DIM, new_d)
                new_h = max(MIN_DIM, new_h)
                
                # Actualizar objeto
                obj['width'] = new_w
                if 'depth' in obj:
                    obj['depth'] = new_d
                elif 'length' in obj:
                    obj['length'] = new_d
                obj['height'] = new_h
                
                self.actualizar_visualizacion()
                return f"✓ '{name}' redimensionado:\n  {old_w:.2f}×{old_d:.2f}×{old_h:.2f}m → {new_w:.2f}×{new_d:.2f}×{new_h:.2f}m"
        
        return f"❌ Objeto '{name}' no encontrado"
    
    def remove(self, name):
        """Elimina un objeto"""
        for i, obj in enumerate(self.objects):
            if obj['name'] == name:
                self.objects.pop(i)
                self.actualizar_visualizacion()
                return f"'{name}' eliminado"
        return f"Error: objeto '{name}' no encontrado"
    
    def list_objects(self):
        """Lista todos los objetos en el espacio"""
        if not self.objects:
            return "No hay objetos en el espacio"
        
        result = f"\n{'='*70}\n"
        result += f"Espacio: {self.width}m x {self.length}m x {self.height}m\n"
        result += f"{'='*70}\n"
        for obj in self.objects:
            result += f"\n{obj['name']} ({obj['type']})\n"
            result += f"  Posición: ({obj['x']:.2f}, {obj['y']:.2f}, {obj['z']:.2f})\n"
            if 'width' in obj:
                result += f"  Dimensiones: {obj['width']:.2f}m x "
                result += f"{obj.get('depth', obj.get('length', 0)):.2f}m x "
                result += f"{obj['height']:.2f}m\n"
        return result
    
    def create_box_triangles(self, x, y, z, width, depth, height):
        """Crea triángulos para una caja con normales correctas"""
        # 8 vértices de la caja
        v = [
            [x, y, z],                    # 0: esquina inferior frontal izquierda
            [x + width, y, z],            # 1: esquina inferior frontal derecha
            [x + width, y + depth, z],    # 2: esquina inferior trasera derecha
            [x, y + depth, z],            # 3: esquina inferior trasera izquierda
            [x, y, z + height],           # 4: esquina superior frontal izquierda
            [x + width, y, z + height],   # 5: esquina superior frontal derecha
            [x + width, y + depth, z + height],  # 6: esquina superior trasera derecha
            [x, y + depth, z + height]    # 7: esquina superior trasera izquierda
        ]
        
        # 12 triángulos (2 por cada cara) con normales hacia AFUERA
        triangles = [
            # Bottom (normal hacia abajo: -Z)
            [v[0], v[1], v[2]], [v[0], v[2], v[3]],
            # Top (normal hacia arriba: +Z)
            [v[4], v[6], v[5]], [v[4], v[7], v[6]],
            # Front (normal hacia -Y)
            [v[0], v[4], v[5]], [v[0], v[5], v[1]],
            # Back (normal hacia +Y)
            [v[2], v[6], v[7]], [v[2], v[7], v[3]],
            # Left (normal hacia -X)
            [v[0], v[3], v[7]], [v[0], v[7], v[4]],
            # Right (normal hacia +X)
            [v[1], v[5], v[6]], [v[1], v[6], v[2]]
        ]
        
        return triangles
    
    def triangulate_polygon(self, vertices):
        """
        Triangula un polígono simple (incluso no convexo) usando ear clipping CORRECTO
        vertices: lista de tuplas (x, y)
        Retorna: lista de triángulos, cada uno con 3 índices de vértices
        """
        if len(vertices) < 3:
            return []
        if len(vertices) == 3:
            return [[0, 1, 2]]
        
        # Ear clipping mejorado que funciona con polígonos no convexos
        triangles = []
        remaining = list(range(len(vertices)))
        
        def is_ear(prev_idx, curr_idx, next_idx, remaining_indices):
            """Verifica si un vértice forma una oreja válida"""
            p1 = vertices[prev_idx]
            p2 = vertices[curr_idx]
            p3 = vertices[next_idx]
            
            # Calcular el área del triángulo (producto cruz)
            area = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
            
            # Si el área es negativa, no es una oreja válida (está "hacia adentro")
            if area <= 0:
                return False
            
            # Verificar que ningún otro vértice esté dentro del triángulo
            for idx in remaining_indices:
                if idx in [prev_idx, curr_idx, next_idx]:
                    continue
                
                p = vertices[idx]
                # Verificar si p está dentro del triángulo usando coordenadas baricéntricas
                if point_in_triangle(p, p1, p2, p3):
                    return False
            
            return True
        
        def point_in_triangle(p, a, b, c):
            """Verifica si punto p está dentro del triángulo abc"""
            def sign(p1, p2, p3):
                return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
            
            d1 = sign(p, a, b)
            d2 = sign(p, b, c)
            d3 = sign(p, c, a)
            
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            
            return not (has_neg and has_pos)
        
        max_iterations = len(vertices) * 2  # Prevenir bucles infinitos
        iterations = 0
        
        while len(remaining) > 3 and iterations < max_iterations:
            iterations += 1
            found_ear = False
            
            for i in range(len(remaining)):
                prev_idx = remaining[i - 1]
                curr_idx = remaining[i]
                next_idx = remaining[(i + 1) % len(remaining)]
                
                if is_ear(prev_idx, curr_idx, next_idx, remaining):
                    triangles.append([prev_idx, curr_idx, next_idx])
                    remaining.pop(i)
                    found_ear = True
                    break
            
            if not found_ear:
                # Fallback: si no encontramos orejas, usar triángulo simple
                if len(remaining) >= 3:
                    triangles.append([remaining[0], remaining[1], remaining[2]])
                    remaining.pop(1)
        
        # Agregar el último triángulo
        if len(remaining) == 3:
            triangles.append(remaining)
        
        return triangles
    
    def create_extruded_polygon_triangles(self, vertices_2d, z, height):
        """
        Crea triángulos para un polígono extruido verticalmente
        vertices_2d: lista de tuplas (x, y) definiendo la base
        z: altura base
        height: altura de extrusión
        """
        triangles = []
        n = len(vertices_2d)
        
        # Crear vértices 3D (base y tope)
        vertices_bottom = [[v[0], v[1], z] for v in vertices_2d]
        vertices_top = [[v[0], v[1], z + height] for v in vertices_2d]
        
        # Triangular la base (cara inferior)
        base_tris = self.triangulate_polygon(vertices_2d)
        for tri in base_tris:
            # Invertir orden para normal hacia abajo
            triangles.append([vertices_bottom[tri[2]], vertices_bottom[tri[1]], vertices_bottom[tri[0]]])
        
        # Triangular el tope (cara superior)
        for tri in base_tris:
            triangles.append([vertices_top[tri[0]], vertices_top[tri[1]], vertices_top[tri[2]]])
        
        # Crear paredes laterales
        for i in range(n):
            next_i = (i + 1) % n
            
            # Dos triángulos por cada pared lateral
            v0 = vertices_bottom[i]
            v1 = vertices_bottom[next_i]
            v2 = vertices_top[next_i]
            v3 = vertices_top[i]
            
            triangles.append([v0, v1, v2])
            triangles.append([v0, v2, v3])
        
        return triangles
    
    def export_stl(self, filename="room_design.stl", flip_y=True):
        """
        Exporta el diseño a STL - VERSIÓN CORREGIDA para habitaciones irregulares
        
        Args:
            filename: Nombre del archivo STL
            flip_y: Si True, invierte el eje Y (corrige espejo norte-sur)
        """
        all_triangles = []
        
        def flip_vertex(v):
            """Invierte el eje Y si es necesario"""
            if flip_y:
                return [v[0], -v[1], v[2]]
            return v
        
        def flip_triangle(tri):
            """Invierte triángulo y ajusta orden de vértices para mantener normales"""
            if flip_y:
                # Invertir Y y revertir orden para mantener normal correcta
                return [flip_vertex(tri[2]), flip_vertex(tri[1]), flip_vertex(tri[0])]
            return tri
        
        # ===== CREAR HABITACIÓN =====
        if not self.is_irregular:
            # Habitación rectangular estándar
            wall_t = 0.15
            
            # PISO
            piso = self.create_box_triangles(0, 0, -0.1, self.width, self.length, 0.1)
            all_triangles.extend(piso)
            
            # PAREDES (sin solapamiento)
            pared_frontal = self.create_box_triangles(0, 0, 0, self.width, wall_t, self.height)
            all_triangles.extend(pared_frontal)
            
            pared_trasera = self.create_box_triangles(0, self.length - wall_t, 0, 
                                                     self.width, wall_t, self.height)
            all_triangles.extend(pared_trasera)
            
            pared_izq = self.create_box_triangles(0, wall_t, 0, 
                                                  wall_t, self.length - 2*wall_t, self.height)
            all_triangles.extend(pared_izq)
            
            pared_der = self.create_box_triangles(self.width - wall_t, wall_t, 0, 
                                                  wall_t, self.length - 2*wall_t, self.height)
            all_triangles.extend(pared_der)
            
            # SIN TECHO
            
        else:
            # Habitación irregular (forma L, etc)
            # PISO usando triangulación mejorada
            floor_triangles = self.create_extruded_polygon_triangles(self.vertices, -0.1, 0.1)
            all_triangles.extend(floor_triangles)
            
            # PAREDES LATERALES (solo los bordes, sin techo ni piso interno)
            # Crear paredes como rectángulos verticales entre cada par de vértices
            n = len(self.vertices)
            for i in range(n):
                next_i = (i + 1) % n
                v0 = self.vertices[i]
                v1 = self.vertices[next_i]
                
                # Crear pared vertical entre v0 y v1
                # 4 vértices de la pared
                p0 = [v0[0], v0[1], 0]
                p1 = [v1[0], v1[1], 0]
                p2 = [v1[0], v1[1], self.height]
                p3 = [v0[0], v0[1], self.height]
                
                # 2 triángulos para esta pared (normal hacia afuera)
                all_triangles.append([p0, p1, p2])
                all_triangles.append([p0, p2, p3])
            
            # SIN TECHO para ver el interior
        
        # ===== AGREGAR PUERTAS Y VENTANAS =====
        for obj in self.objects:
            obj_type = obj['type']
            x, y, z = obj['x'], obj['y'], obj['z']
            
            if obj_type == 'door':
                # Exportar puerta como caja delgada
                w = obj.get('width', 0.9)
                h = obj.get('height', 2.1)
                t = obj.get('thickness', 0.1)
                o = obj.get('orientation', 'horizontal')
                
                if o == 'horizontal':
                    door_tri = self.create_box_triangles(x, y, z, w, t, h)
                else:
                    door_tri = self.create_box_triangles(x, y, z, t, w, h)
                
                all_triangles.extend(door_tri)
            
            elif obj_type == 'window':
                # Exportar ventana como marco
                w = obj.get('width', 1.0)
                h = obj.get('height', 1.0)
                d = obj.get('depth', 0.05)
                
                # Ventana como caja delgada
                window_tri = self.create_box_triangles(x, y, z, w, d, h)
                all_triangles.extend(window_tri)
        
        # ===== AGREGAR MUEBLES =====
        for obj in self.objects:
            obj_type = obj['type']
            
            # Saltar puertas y ventanas (ya procesadas)
            if obj_type in ['door', 'window']:
                continue
            
            z = obj['z']
            height = obj.get('height', 1.0)
            
            # Objetos con forma personalizada
            if obj.get('is_custom') and 'vertices' in obj:
                vertices_2d = obj['vertices']
                obj_triangles = self.create_extruded_polygon_triangles(vertices_2d, z, height)
                all_triangles.extend(obj_triangles)
            else:
                # Objetos rectangulares estándar
                x = obj['x']
                y = obj['y']
                
                if obj_type in ['bed', 'bunk_bed', 'wardrobe', 'nightstand', 
                               'fridge', 'stove', 'sink', 'cabinet', 'counter', 'table',
                               'generic']:
                    width = obj.get('width', 1.0)
                    depth = obj.get('depth', obj.get('length', 1.0))
                    
                    triangles = self.create_box_triangles(x, y, z, width, depth, height)
                    all_triangles.extend(triangles)
                    
                    # Cuchetas - segunda cama
                    if obj_type == 'bunk_bed':
                        triangles2 = self.create_box_triangles(x, y, z + 0.9, width, depth, 0.6)
                        all_triangles.extend(triangles2)
        
        if all_triangles:
            # Aplicar inversión de Y si es necesario (corregir espejo)
            if flip_y:
                flipped_triangles = []
                for tri in all_triangles:
                    # Invertir Y en cada vértice y revertir orden
                    v0 = [tri[0][0], -tri[0][1], tri[0][2]]
                    v1 = [tri[1][0], -tri[1][1], tri[1][2]]
                    v2 = [tri[2][0], -tri[2][1], tri[2][2]]
                    # Revertir orden para mantener normal correcta
                    flipped_triangles.append([v2, v1, v0])
                all_triangles = flipped_triangles
            
            STLWriter.write_binary_stl(filename, all_triangles)
            
            # Contar objetos exportados
            muebles = sum(1 for o in self.objects if o['type'] not in ['door', 'window'])
            puertas = sum(1 for o in self.objects if o['type'] == 'door')
            ventanas = sum(1 for o in self.objects if o['type'] == 'window')
            
            tipo = "irregular" if self.is_irregular else "rectangular"
            flip_msg = " (eje Y corregido)" if flip_y else ""
            
            return f"✓ Exportado: {filename}{flip_msg}\n  Triángulos: {len(all_triangles)}\n  Habitación {tipo}: {self.width:.2f}×{self.length:.2f}×{self.height:.2f}m\n  Piso + paredes (sin techo)\n  Puertas: {puertas}, Ventanas: {ventanas}, Muebles: {muebles}"
        else:
            return "No hay objetos para exportar"
    
    def export_obj_with_colors(self, filename_base):
        """
        Exporta a OBJ con colores (archivo .obj + .mtl)
        
        Args:
            filename_base: Nombre base sin extensión (ej: "cocina")
            Genera: cocina.obj y cocina.mtl
        
        Returns:
            Mensaje de éxito
        """
        obj_file = filename_base + ".obj"
        mtl_file = filename_base + ".mtl"
        mtl_name = mtl_file.split('/')[-1]
        
        # Colores por tipo
        colors = {
            'wall': (0.9, 0.9, 0.9),
            'floor': (0.8, 0.75, 0.7),
            'door': (0.82, 0.71, 0.55),
            'window': (0.53, 0.81, 0.92),
            'bed': (1.0, 0.71, 0.76),
            'wardrobe': (0.55, 0.27, 0.07),
            'table': (0.87, 0.72, 0.53),
            'fridge': (0.69, 0.77, 0.87),
            'stove': (1.0, 0.36, 0.27),
            'sink': (0.28, 0.51, 0.71),
            'counter': (0.96, 0.87, 0.70),
            'generic': (0.87, 0.63, 0.87),
        }
        
        vertices = []
        faces_by_material = {}
        vertex_index = 1
        
        def add_box_obj(x, y, z, w, d, h, material):
            nonlocal vertex_index
            
            # 8 vértices (con Y invertido para corregir espejo)
            v = [
                [x, -y, z],
                [x + w, -y, z],
                [x + w, -(y + d), z],
                [x, -(y + d), z],
                [x, -y, z + h],
                [x + w, -y, z + h],
                [x + w, -(y + d), z + h],
                [x, -(y + d), z + h]
            ]
            
            vertices.extend(v)
            idx = list(range(vertex_index, vertex_index + 8))
            vertex_index += 8
            
            # Caras (orden ajustado para Y invertido)
            faces = [
                [idx[0], idx[3], idx[2], idx[1]],  # Bottom
                [idx[4], idx[5], idx[6], idx[7]],  # Top
                [idx[0], idx[1], idx[5], idx[4]],  # Front
                [idx[2], idx[3], idx[7], idx[6]],  # Back
                [idx[0], idx[4], idx[7], idx[3]],  # Left
                [idx[1], idx[2], idx[6], idx[5]],  # Right
            ]
            
            if material not in faces_by_material:
                faces_by_material[material] = []
            faces_by_material[material].extend(faces)
        
        # Exportar habitación
        if not self.is_irregular:
            add_box_obj(0, 0, -0.1, self.width, self.length, 0.1, 'floor')
            
            wall_t = 0.15
            add_box_obj(0, 0, 0, self.width, wall_t, self.height, 'wall')
            add_box_obj(0, self.length - wall_t, 0, self.width, wall_t, self.height, 'wall')
            add_box_obj(0, wall_t, 0, wall_t, self.length - 2*wall_t, self.height, 'wall')
            add_box_obj(self.width - wall_t, wall_t, 0, wall_t, self.length - 2*wall_t, self.height, 'wall')
        else:
            # Habitación irregular - EXPORTAR PISO Y PAREDES
            base_tris = self.triangulate_polygon(self.vertices)
            vertices_bottom = [[v[0], -v[1], -0.1] for v in self.vertices]
            vertices_top = [[v[0], -v[1], 0] for v in self.vertices]
            
            floor_start = vertex_index
            for v in vertices_bottom + vertices_top:
                vertices.append(v)
                vertex_index += 1
            
            if 'floor' not in faces_by_material:
                faces_by_material['floor'] = []
            
            n = len(self.vertices)
            for tri in base_tris:
                faces_by_material['floor'].append([floor_start + tri[2], floor_start + tri[1], floor_start + tri[0]])
                faces_by_material['floor'].append([floor_start + n + tri[0], floor_start + n + tri[1], floor_start + n + tri[2]])
            
            # Paredes
            if 'wall' not in faces_by_material:
                faces_by_material['wall'] = []
            
            for i in range(n):
                next_i = (i + 1) % n
                v0, v1 = self.vertices[i], self.vertices[next_i]
                
                wall_start = vertex_index
                for wv in [[v0[0], -v0[1], 0], [v1[0], -v1[1], 0], [v1[0], -v1[1], self.height], [v0[0], -v0[1], self.height]]:
                    vertices.append(wv)
                    vertex_index += 1
                
                faces_by_material['wall'].append([wall_start, wall_start+1, wall_start+2, wall_start+3])
        
        # Exportar objetos
        for obj in self.objects:
            obj_type = obj['type']
            x, y, z = obj['x'], obj['y'], obj['z']
            
            if obj_type == 'door':
                w = obj.get('width', 0.9)
                h = obj.get('height', 2.1)
                t = obj.get('thickness', 0.1)
                o = obj.get('orientation', 'horizontal')
                
                if o == 'horizontal':
                    add_box_obj(x, y, z, w, t, h, 'door')
                else:
                    add_box_obj(x, y, z, t, w, h, 'door')
            
            elif obj_type == 'window':
                w = obj.get('width', 1.0)
                h = obj.get('height', 1.0)
                d = obj.get('depth', 0.05)
                add_box_obj(x, y, z, w, d, h, 'window')
            
            elif obj_type in ['bed', 'wardrobe', 'table', 'fridge', 'stove', 'sink', 'counter', 'generic']:
                w = obj.get('width', 1.0)
                d = obj.get('depth', obj.get('length', 1.0))
                h = obj.get('height', 1.0)
                add_box_obj(x, y, z, w, d, h, obj_type)
        
        # Escribir MTL
        with open(mtl_file, 'w') as f:
            f.write("# Room Designer Materials\n\n")
            for mat_name, color in colors.items():
                f.write(f"newmtl {mat_name}\n")
                f.write(f"Ka {color[0]:.3f} {color[1]:.3f} {color[2]:.3f}\n")
                f.write(f"Kd {color[0]:.3f} {color[1]:.3f} {color[2]:.3f}\n")
                f.write(f"Ks 0.5 0.5 0.5\n")
                f.write(f"Ns 50.0\n")
                f.write(f"d 1.0\n\n")
        
        # Escribir OBJ
        with open(obj_file, 'w') as f:
            f.write("# Room Designer Export\n")
            f.write(f"mtllib {mtl_name}\n\n")
            
            for v in vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
            f.write("\n")
            
            for material, faces in faces_by_material.items():
                f.write(f"usemtl {material}\n")
                for face in faces:
                    f.write(f"f {' '.join(map(str, face))}\n")
                f.write("\n")
        
        muebles = sum(1 for o in self.objects if o['type'] not in ['door', 'window'])
        puertas = sum(1 for o in self.objects if o['type'] == 'door')
        ventanas = sum(1 for o in self.objects if o['type'] == 'window')
        
        return f"✓ Exportado OBJ con colores:\n  {obj_file}\n  {mtl_file}\n  Materiales: {len(faces_by_material)}\n  Puertas: {puertas}, Ventanas: {ventanas}, Muebles: {muebles}"
    
    def import_stl(self, filename, name="imported", x=0, y=0, z=0):
        """
        Importa un STL simple como objeto personalizado
        NOTA: Esta es una implementación básica que crea un bounding box del STL
        """
        try:
            with open(filename, 'rb') as f:
                # Leer header
                header = f.read(80)
                
                # Leer número de triángulos
                num_triangles = struct.unpack('<I', f.read(4))[0]
                
                # Leer vértices para calcular bounding box
                min_x = min_y = min_z = float('inf')
                max_x = max_y = max_z = float('-inf')
                
                for _ in range(num_triangles):
                    # Leer normal (3 floats)
                    f.read(12)
                    
                    # Leer 3 vértices
                    for _ in range(3):
                        vx, vy, vz = struct.unpack('<fff', f.read(12))
                        min_x, max_x = min(min_x, vx), max(max_x, vx)
                        min_y, max_y = min(min_y, vy), max(max_y, vy)
                        min_z, max_z = min(min_z, vz), max(max_z, vz)
                    
                    # Leer attribute byte count
                    f.read(2)
                
                # Crear objeto con dimensiones del bounding box
                width = max_x - min_x
                depth = max_y - min_y
                height = max_z - min_z
                
                obj = {
                    'type': 'imported',
                    'name': name,
                    'x': x,
                    'y': y,
                    'z': z,
                    'width': width,
                    'depth': depth,
                    'height': height,
                    'stl_file': filename
                }
                self.objects.append(obj)
                
                return f"STL '{filename}' importado como '{name}' ({width:.2f}m x {depth:.2f}m x {height:.2f}m)"
        except Exception as e:
            return f"Error importando STL: {e}"
    
    def generate_plan_view(self, filename="plan_view.png"):
        """Genera una vista en planta como imagen PNG"""
        fig, ax = plt.subplots(figsize=(12, 12 * self.length / self.width))
        
        # Dibujar el cuarto (paredes) - puede ser irregular
        if self.is_irregular:
            # Dibujar polígono irregular
            xs = [v[0] for v in self.vertices] + [self.vertices[0][0]]
            ys = [v[1] for v in self.vertices] + [self.vertices[0][1]]
            ax.fill(xs, ys, facecolor='white', edgecolor='black', linewidth=3)
        else:
            # Dibujar rectángulo estándar
            room_rect = Rectangle((0, 0), self.width, self.length, 
                                  linewidth=3, edgecolor='black', facecolor='white')
            ax.add_patch(room_rect)
        
        # Colores por tipo de objeto
        colors = {
            'bed': '#FFB6C1',           # Rosa para camas
            'bunk_bed': '#FF69B4',      # Rosa oscuro para cuchetas
            'wardrobe': '#8B4513',      # Marrón para roperos
            'nightstand': '#D2691E',    # Marrón claro para mesas de luz
            'table': '#DEB887',         # Beige para mesas
            'fridge': '#B0C4DE',        # Azul claro para heladera
            'stove': '#CD5C5C',         # Rojo para cocina
            'sink': '#4682B4',          # Azul para pileta
            'cabinet': '#A0522D',       # Marrón medio para alacenas
            'counter': '#F5DEB3',       # Trigo para mesadas
            'counter_l': '#F5DEB3',     # Trigo para mesadas en L
            'custom': '#9370DB',        # Púrpura para personalizados
            'door': '#D2B48C',          # Tan para puertas
            'window': '#87CEEB',        # Celeste para ventanas
            'imported': '#808080'       # Gris para importados
        }
        
        labels_spanish = {
            'bed': 'Cama',
            'bunk_bed': 'Cucheta',
            'wardrobe': 'Ropero',
            'nightstand': 'Mesa de luz',
            'table': 'Mesa',
            'fridge': 'Heladera',
            'stove': 'Cocina',
            'sink': 'Pileta',
            'cabinet': 'Alacena',
            'counter': 'Mesada',
            'counter_l': 'Mesada L',
            'custom': 'Personalizado',
            'door': 'Puerta',
            'window': 'Ventana',
            'imported': 'Importado'
        }
        
        # Dibujar cada objeto
        for obj in self.objects:
            color = colors.get(obj['type'], '#CCCCCC')
            
            # Verificar si es una puerta
            if obj['type'] == 'door':
                x = obj['x']
                y = obj['y']
                width = obj.get('width', 0.9)
                orientation = obj.get('orientation', 'horizontal')
                hinge = obj.get('hinge', 'derecha')
                swing = obj.get('swing', 'norte')
                thickness = obj.get('thickness', 0.1)
                
                from matplotlib.patches import Arc
                import math
                
                if orientation == 'horizontal':
                    # Puerta horizontal: ancho en X, grosor en Y
                    rect = Rectangle((x, y), width, thickness,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    ax.add_patch(rect)
                    
                    # Determinar pivote según bisagras
                    if hinge == 'derecha':
                        pivot_x = x + width
                        if swing == 'norte':
                            # Norte = +Y (arriba en el plano)
                            pivot_y = y
                            theta1, theta2 = 90, 180
                            end_x = pivot_x - width
                            end_y = pivot_y + width
                        else:  # sur
                            # Sur = -Y (abajo en el plano, hacia afuera)
                            pivot_y = y + thickness
                            theta1, theta2 = 180, 270
                            end_x = pivot_x - width
                            end_y = pivot_y - width
                    else:  # izquierda
                        pivot_x = x
                        if swing == 'norte':
                            # Norte = +Y (arriba en el plano)
                            pivot_y = y
                            theta1, theta2 = 0, 90
                            end_x = pivot_x + width
                            end_y = pivot_y + width
                        else:  # sur
                            # Sur = -Y (abajo en el plano, hacia afuera)
                            pivot_y = y + thickness
                            theta1, theta2 = 270, 360
                            end_x = pivot_x + width
                            end_y = pivot_y - width
                    
                    # Dibujar arco y línea
                    arc = Arc((pivot_x, pivot_y), width*2, width*2, 
                             angle=0, theta1=theta1, theta2=theta2,
                             color='black', linewidth=1, linestyle='--', alpha=0.6)
                    ax.add_patch(arc)
                    ax.plot([pivot_x, end_x], [pivot_y, end_y], 
                           color='black', linewidth=1, linestyle='-', alpha=0.4)
                    
                    # Etiqueta
                    center_x = x + width / 2
                    center_y = y + thickness / 2
                    
                else:  # vertical
                    # Puerta vertical: ancho en Y, grosor en X
                    rect = Rectangle((x, y), thickness, width,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    ax.add_patch(rect)
                    
                    # Determinar pivote según bisagras
                    if hinge == 'abajo':
                        pivot_y = y
                        if swing == 'este':
                            # Este = +X (derecha en el plano)
                            pivot_x = x + thickness
                            theta1, theta2 = 0, 90
                            end_x = pivot_x + width
                            end_y = pivot_y + width
                        else:  # oeste
                            # Oeste = -X (izquierda en el plano)
                            pivot_x = x
                            theta1, theta2 = 90, 180
                            end_x = pivot_x - width
                            end_y = pivot_y + width
                    else:  # arriba
                        pivot_y = y + width
                        if swing == 'este':
                            # Este = +X (derecha en el plano)
                            pivot_x = x + thickness
                            theta1, theta2 = 270, 360
                            end_x = pivot_x + width
                            end_y = pivot_y - width
                        else:  # oeste
                            # Oeste = -X (izquierda en el plano)
                            pivot_x = x
                            theta1, theta2 = 180, 270
                            end_x = pivot_x - width
                            end_y = pivot_y - width
                    
                    # Dibujar arco y línea
                    arc = Arc((pivot_x, pivot_y), width*2, width*2, 
                             angle=0, theta1=theta1, theta2=theta2,
                             color='black', linewidth=1, linestyle='--', alpha=0.6)
                    ax.add_patch(arc)
                    ax.plot([pivot_x, end_x], [pivot_y, end_y], 
                           color='black', linewidth=1, linestyle='-', alpha=0.4)
                    
                    # Etiqueta
                    center_x = x + thickness / 2
                    center_y = y + width / 2
                
                ax.text(center_x, center_y, obj['name'],
                       ha='center', va='center', fontsize=6,
                       fontweight='bold', color='black',
                       bbox=dict(boxstyle='round,pad=0.2', 
                               facecolor='white', alpha=0.8, edgecolor='none'))
            
            # Verificar si es una ventana
            elif obj['type'] == 'window':
                x = obj['x']
                y = obj['y']
                width = obj.get('width', 1.2)
                depth = obj.get('depth', 0.05)
                
                # Dibujar ventana
                rect = Rectangle((x, y), width, depth,
                               linewidth=1.5, edgecolor='black', 
                               facecolor=color, alpha=0.5)
                ax.add_patch(rect)
                
                # Líneas cruzadas para indicar ventana
                ax.plot([x, x + width], [y, y + depth], 'k-', linewidth=0.5)
                ax.plot([x, x + width], [y + depth, y], 'k-', linewidth=0.5)
                
                # Etiqueta
                center_x = x + width / 2
                center_y = y + depth / 2
                ax.text(center_x, center_y + 0.1, obj['name'],
                       ha='center', va='center', fontsize=6,
                       style='italic', color='black')
            
            # Verificar si es un objeto con forma personalizada
            elif obj.get('is_custom') and 'vertices' in obj:
                # Dibujar polígono personalizado
                vertices = obj['vertices']
                xs = [v[0] for v in vertices] + [vertices[0][0]]
                ys = [v[1] for v in vertices] + [vertices[0][1]]
                
                ax.fill(xs, ys, facecolor=color, edgecolor='black', 
                       linewidth=1.5, alpha=0.7)
                
                # Calcular centroide para la etiqueta
                center_x = sum(v[0] for v in vertices) / len(vertices)
                center_y = sum(v[1] for v in vertices) / len(vertices)
                
                # Agregar etiqueta
                ax.text(center_x, center_y, obj['name'],
                       ha='center', va='center', fontsize=8,
                       fontweight='bold', color='black',
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='white', alpha=0.8, edgecolor='none'))
            else:
                # Objeto rectangular estándar
                x = obj['x']
                y = obj['y']
                width = obj.get('width', 1.0)
                depth = obj.get('depth', obj.get('length', 1.0))
                
                # Crear rectángulo para el objeto
                rect = Rectangle((x, y), width, depth,
                               linewidth=1.5, edgecolor='black', 
                               facecolor=color, alpha=0.7)
                ax.add_patch(rect)
                
                # Agregar etiqueta con el nombre
                center_x = x + width / 2
                center_y = y + depth / 2
                
                # Nombre del objeto
                ax.text(center_x, center_y, obj['name'],
                       ha='center', va='center', fontsize=8,
                       fontweight='bold', color='black',
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='white', alpha=0.8, edgecolor='none'))
                
                # Dimensiones en pequeño
                dim_text = f"{width:.1f}×{depth:.1f}m"
                ax.text(center_x, center_y - 0.15, dim_text,
                       ha='center', va='center', fontsize=6,
                       style='italic', color='black')
        
        # Configurar ejes
        ax.set_xlim(-0.5, self.width + 0.5)
        ax.set_ylim(-0.5, self.length + 0.5)
        ax.set_aspect('equal')
        ax.set_xlabel('Ancho (metros)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Largo (metros)', fontsize=12, fontweight='bold')
        
        # Título
        title = f'Vista en Planta - {self.width:.1f}m × {self.length:.1f}m'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Grid de referencia
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xticks(np.arange(0, self.width + 0.5, 0.5))
        ax.set_yticks(np.arange(0, self.length + 0.5, 0.5))
        
        # Invertir eje Y para que (0,0) esté abajo a la izquierda
        ax.invert_yaxis()
        
        # Agregar leyenda de colores
        from matplotlib.patches import Patch
        legend_elements = []
        seen_types = set()
        for obj in self.objects:
            obj_type = obj['type']
            if obj_type not in seen_types:
                seen_types.add(obj_type)
                legend_elements.append(
                    Patch(facecolor=colors.get(obj_type, '#CCCCCC'),
                         edgecolor='black', label=labels_spanish.get(obj_type, obj_type))
                )
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc='upper left', 
                     bbox_to_anchor=(1.02, 1), fontsize=9)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Vista en planta guardada en {filename}"
    
    def generate_side_view(self, filename="side_view.png"):
        """Genera una vista lateral (elevación) como imagen PNG"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Dibujar el piso
        floor = Rectangle((0, 0), self.width, 0.1, 
                         linewidth=2, edgecolor='black', facecolor='#654321')
        ax.add_patch(floor)
        
        # Dibujar las paredes laterales (líneas)
        ax.plot([0, 0], [0, self.height], 'k-', linewidth=3)  # Pared izquierda
        ax.plot([self.width, self.width], [0, self.height], 'k-', linewidth=3)  # Pared derecha
        ax.plot([0, self.width], [self.height, self.height], 'k-', linewidth=3)  # Techo
        
        # Colores por tipo de objeto
        colors = {
            'bed': '#FFB6C1',
            'bunk_bed': '#FF69B4',
            'wardrobe': '#8B4513',
            'nightstand': '#D2691E',
            'table': '#DEB887',
            'fridge': '#B0C4DE',
            'stove': '#CD5C5C',
            'sink': '#4682B4',
            'cabinet': '#A0522D',
            'counter': '#F5DEB3',
            'imported': '#808080'
        }
        
        # Dibujar cada objeto (vista lateral)
        for obj in self.objects:
            x = obj['x']
            z = obj['z']
            width = obj.get('width', 1.0)
            height = obj.get('height', 1.0)
            
            color = colors.get(obj['type'], '#CCCCCC')
            
            # Crear rectángulo para el objeto
            rect = Rectangle((x, z), width, height,
                           linewidth=1.5, edgecolor='black', 
                           facecolor=color, alpha=0.7)
            ax.add_patch(rect)
            
            # Agregar etiqueta
            center_x = x + width / 2
            center_z = z + height / 2
            
            ax.text(center_x, center_z, obj['name'],
                   ha='center', va='center', fontsize=7,
                   fontweight='bold', color='black', rotation=0,
                   bbox=dict(boxstyle='round,pad=0.2', 
                           facecolor='white', alpha=0.8, edgecolor='none'))
        
        # Configurar ejes
        ax.set_xlim(-0.3, self.width + 0.3)
        ax.set_ylim(-0.2, self.height + 0.3)
        ax.set_aspect('equal')
        ax.set_xlabel('Ancho (metros)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Altura (metros)', fontsize=12, fontweight='bold')
        
        # Título
        title = f'Vista Lateral (Elevación) - {self.width}m × {self.height}m'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Grid de referencia
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xticks(np.arange(0, self.width + 0.5, 0.5))
        ax.set_yticks(np.arange(0, self.height + 0.5, 0.5))
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Vista lateral guardada en {filename}"
    
    def generate_3d_view(self, filename="view_3d.png"):
        """Genera una vista isométrica 3D como imagen PNG"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Función para convertir coordenadas 3D a 2D isométricas
        def iso_transform(x, y, z):
            # Proyección isométrica estándar
            iso_x = (x - y) * np.cos(np.pi / 6)
            iso_y = (x + y) * np.sin(np.pi / 6) + z
            return iso_x, iso_y
        
        # Colores por tipo de objeto
        colors = {
            'bed': '#FFB6C1',
            'bunk_bed': '#FF69B4',
            'wardrobe': '#8B4513',
            'nightstand': '#D2691E',
            'table': '#DEB887',
            'fridge': '#B0C4DE',
            'stove': '#CD5C5C',
            'sink': '#4682B4',
            'cabinet': '#A0522D',
            'counter': '#F5DEB3',
            'counter_l': '#F5DEB3',
            'custom': '#9370DB',
            'imported': '#808080'
        }
        
        # Dibujar el piso del cuarto (puede ser irregular)
        floor_iso = [iso_transform(v[0], v[1], 0) for v in self.vertices]
        floor_xs, floor_ys = zip(*floor_iso)
        ax.fill(floor_xs, floor_ys, color='#F5F5DC', alpha=0.3, edgecolor='black', linewidth=2)
        
        # Dibujar cada objeto en isométrico
        objects_sorted = sorted(self.objects, key=lambda o: (o['y'], o['x']))
        
        for obj in objects_sorted:
            z = obj['z']
            height = obj.get('height', 1.0)
            color = colors.get(obj['type'], '#CCCCCC')
            
            # Verificar si es un objeto con forma personalizada
            if obj.get('is_custom') and 'vertices' in obj:
                # Dibujar polígono extruido
                vertices_2d = obj['vertices']
                n = len(vertices_2d)
                
                # Vértices superiores e inferiores en 3D
                bottom_verts_3d = [(v[0], v[1], z) for v in vertices_2d]
                top_verts_3d = [(v[0], v[1], z + height) for v in vertices_2d]
                
                # Convertir a isométrico
                bottom_iso = [iso_transform(*v) for v in bottom_verts_3d]
                top_iso = [iso_transform(*v) for v in top_verts_3d]
                
                # Dibujar cara superior
                top_xs, top_ys = zip(*top_iso)
                ax.fill(top_xs, top_ys, color=color, alpha=0.8, edgecolor='black', linewidth=1)
                
                # Dibujar caras laterales visibles
                # Simplificación: dibujar todas las caras laterales
                for i in range(n):
                    next_i = (i + 1) % n
                    
                    # Crear polígono de la cara lateral
                    face_iso = [
                        bottom_iso[i],
                        bottom_iso[next_i],
                        top_iso[next_i],
                        top_iso[i]
                    ]
                    
                    face_xs, face_ys = zip(*face_iso)
                    ax.fill(face_xs, face_ys, color=color, alpha=0.6, 
                           edgecolor='black', linewidth=1)
                
                # Calcular centroide para etiqueta
                center_x = sum(v[0] for v in vertices_2d) / len(vertices_2d)
                center_y = sum(v[1] for v in vertices_2d) / len(vertices_2d)
                label_x, label_y = iso_transform(center_x, center_y, z + height)
                
            else:
                # Objeto rectangular estándar (código existente)
                x = obj['x']
                y = obj['y']
                width = obj.get('width', 1.0)
                depth = obj.get('depth', obj.get('length', 1.0))
                
                # Vértices del cubo
                vertices_3d = [
                    (x, y, z),
                    (x + width, y, z),
                    (x + width, y + depth, z),
                    (x, y + depth, z),
                    (x, y, z + height),
                    (x + width, y, z + height),
                    (x + width, y + depth, z + height),
                    (x, y + depth, z + height)
                ]
                
                vertices_iso = [iso_transform(vx, vy, vz) for vx, vy, vz in vertices_3d]
                
                # Dibujar cara superior
                top_face = [vertices_iso[4], vertices_iso[5], vertices_iso[6], vertices_iso[7]]
                top_xs, top_ys = zip(*top_face)
                ax.fill(top_xs, top_ys, color=color, alpha=0.8, edgecolor='black', linewidth=1)
                
                # Dibujar cara frontal
                front_face = [vertices_iso[0], vertices_iso[1], vertices_iso[5], vertices_iso[4]]
                front_xs, front_ys = zip(*front_face)
                ax.fill(front_xs, front_ys, color=color, alpha=0.6, edgecolor='black', linewidth=1)
                
                # Dibujar cara lateral derecha
                right_face = [vertices_iso[1], vertices_iso[2], vertices_iso[6], vertices_iso[5]]
                right_xs, right_ys = zip(*right_face)
                ax.fill(right_xs, right_ys, color=color, alpha=0.5, edgecolor='black', linewidth=1)
                
                label_x, label_y = iso_transform(x + width/2, y + depth/2, z + height)
            
            # Agregar etiqueta
            ax.text(label_x, label_y + 0.1, obj['name'],
                   ha='center', va='center', fontsize=7,
                   fontweight='bold', color='black',
                   bbox=dict(boxstyle='round,pad=0.2', 
                           facecolor='white', alpha=0.9, edgecolor='gray'))
        
        # Configurar ejes
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Título
        title = f'Vista Isométrica 3D - {self.width:.1f}m × {self.length:.1f}m × {self.height:.1f}m'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Ajustar límites para centrar el dibujo
        all_x = []
        all_y = []
        
        # Incluir el piso
        for v in self.vertices:
            ix, iy = iso_transform(v[0], v[1], 0)
            all_x.append(ix)
            all_y.append(iy)
        
        # Incluir todos los objetos
        for obj in self.objects:
            if obj.get('is_custom') and 'vertices' in obj:
                for v in obj['vertices']:
                    for dz in [0, obj.get('height', 1.0)]:
                        ix, iy = iso_transform(v[0], v[1], obj['z'] + dz)
                        all_x.append(ix)
                        all_y.append(iy)
            else:
                for dx in [0, obj.get('width', 1.0)]:
                    for dy in [0, obj.get('depth', obj.get('length', 1.0))]:
                        for dz in [0, obj.get('height', 1.0)]:
                            ix, iy = iso_transform(obj['x'] + dx, obj['y'] + dy, obj['z'] + dz)
                            all_x.append(ix)
                            all_y.append(iy)
        
        if all_x and all_y:
            margin = 1.0
            ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
            ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Vista 3D isométrica guardada en {filename}"
    
    def save_design(self, filename="design.json"):
        """Guarda el diseño en JSON"""
        data = {
            'room': {
                'width': self.width,
                'length': self.length,
                'height': self.height,
                'is_irregular': self.is_irregular,
                'vertices': self.vertices if self.is_irregular else None
            },
            'objects': self.objects
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return f"Diseño guardado en {filename}"
    
    def load_design(self, filename="design.json"):
        """Carga un diseño desde JSON"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        room_data = data['room']
        if room_data.get('is_irregular') and room_data.get('vertices'):
            self.__init__(vertices=room_data['vertices'], height=room_data['height'])
        else:
            self.__init__(room_data['width'], room_data['length'], room_data['height'])
        
        self.objects = data['objects']
        return f"Diseño cargado desde {filename}"
    
    def actualizar_visualizacion(self):
        """Actualiza la visualización en tiempo real si está activa"""
        global VISUALIZACION_ACTIVA, VENTANA_VISUALIZACION
        
        if VISUALIZACION_ACTIVA is None:
            return
        
        # Configurar matplotlib para modo interactivo
        plt.ion()
        
        # Si no hay figura activa, crear una
        if VENTANA_VISUALIZACION is None or not plt.fignum_exists(VENTANA_VISUALIZACION):
            fig = plt.figure(figsize=(10, 10))
            VENTANA_VISUALIZACION = fig.number
            plt.show(block=False)
        else:
            # Usar la figura existente
            plt.figure(VENTANA_VISUALIZACION)
            plt.clf()  # Limpiar el contenido actual
        
        # Generar el contenido según el tipo de visualización
        if VISUALIZACION_ACTIVA == 'planta':
            self._dibujar_planta_en_figura()
        elif VISUALIZACION_ACTIVA == 'lateral':
            self._dibujar_lateral_en_figura()
        elif VISUALIZACION_ACTIVA == '3d':
            self._dibujar_3d_en_figura()
        
        # Actualizar la ventana
        plt.draw()
        plt.pause(0.001)  # Pausa mínima para que se actualice
    
    def _dibujar_planta_en_figura(self):
        """Dibuja la vista de planta en la figura actual"""
        ax = plt.gca()
        
        # Dibujar el cuarto
        if self.is_irregular:
            xs = [v[0] for v in self.vertices] + [self.vertices[0][0]]
            ys = [v[1] for v in self.vertices] + [self.vertices[0][1]]
            ax.fill(xs, ys, facecolor='white', edgecolor='black', linewidth=3)
        else:
            from matplotlib.patches import Rectangle
            room_rect = Rectangle((0, 0), self.width, self.length, 
                                  linewidth=3, edgecolor='black', facecolor='white')
            ax.add_patch(room_rect)
        
        # Colores (versión simplificada para la visualización en tiempo real)
        colors = {
            'bed': '#FFB6C1', 'bunk_bed': '#FF69B4', 'wardrobe': '#8B4513',
            'nightstand': '#D2691E', 'table': '#DEB887', 'fridge': '#B0C4DE',
            'stove': '#CD5C5C', 'sink': '#4682B4', 'cabinet': '#A0522D',
            'counter': '#F5DEB3', 'counter_l': '#F5DEB3', 'custom': '#9370DB',
            'door': '#D2B48C', 'window': '#87CEEB', 'imported': '#808080'
        }
        
        # Dibujar objetos (versión simplificada)
        for obj in self.objects:
            color = colors.get(obj['type'], '#CCCCCC')
            
            if obj.get('is_custom') and 'vertices' in obj:
                vertices = obj['vertices']
                xs = [v[0] for v in vertices] + [vertices[0][0]]
                ys = [v[1] for v in vertices] + [vertices[0][1]]
                ax.fill(xs, ys, facecolor=color, edgecolor='black', linewidth=1, alpha=0.7)
            else:
                x, y = obj['x'], obj['y']
                w = obj.get('width', 1.0)
                d = obj.get('depth', obj.get('length', 1.0))
                
                from matplotlib.patches import Rectangle
                rect = Rectangle((x, y), w, d, linewidth=1, edgecolor='black',
                               facecolor=color, alpha=0.7)
                ax.add_patch(rect)
        
        ax.set_xlim(-0.5, self.width + 0.5)
        ax.set_ylim(-0.5, self.length + 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_title(f'Vista en Planta - {self.width:.1f}m × {self.length:.1f}m', 
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _dibujar_lateral_en_figura(self):
        """Dibuja la vista lateral en la figura actual"""
        ax = plt.gca()
        ax.plot([0, self.width], [0, 0], 'k-', linewidth=2)  # Piso
        ax.set_xlim(-0.3, self.width + 0.3)
        ax.set_ylim(-0.2, self.height + 0.3)
        ax.set_aspect('equal')
        ax.set_title(f'Vista Lateral - {self.width:.1f}m × {self.height:.1f}m',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _dibujar_3d_en_figura(self):
        """Dibuja la vista 3D isométrica en la figura actual"""
        ax = plt.gca()
        ax.axis('off')
        ax.set_title(f'Vista 3D - {self.width:.1f}m × {self.length:.1f}m × {self.height:.1f}m',
                    fontsize=12, fontweight='bold')
        # Aquí iría la lógica completa de 3D, simplificada por ahora


def interactive_mode():
    """Modo interactivo por línea de comandos con visualización en tiempo real"""
    global VISUALIZACION_ACTIVA
    
    # Configurar readline para autocompletado e historial
    try:
        import readline
        
        # Configurar historial
        histfile = os.path.expanduser("~/.room_designer_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        
        # Configurar autocompletado
        completer = RoomDesignerCompleter(COMANDOS_DISPONIBLES)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        
        # Guardar historial al salir
        import atexit
        atexit.register(readline.write_history_file, histfile)
        
        readline_available = True
    except ImportError:
        readline_available = False
    
    print("="*70)
    print("ROOM DESIGNER - Diseñador de Espacios")
    print("="*70)
    
    if readline_available:
        print("\n💡 TIPS:")
        print("  - Usa TAB para autocompletar comandos")
        print("  - Usa ↑ y ↓ para navegar por el historial")
    
    print("\nEscribe 'ayuda' para ver los comandos disponibles")
    print("Escribe 'salir' para terminar\n")
    
    designer = None
    
    # Diccionario de traducciones de comandos
    comandos_es_en = {
        'nuevo': 'new',
        'nuevo_irregular': 'new_custom',
        'agregar_cama': 'add_bed',
        'agregar_cucheta': 'add_bunk_bed',
        'agregar_ropero': 'add_wardrobe',
        'agregar_mesa_luz': 'add_nightstand',
        'agregar_mesa': 'add_table',
        'agregar_heladera': 'add_fridge',
        'agregar_cocina': 'add_stove',
        'agregar_pileta': 'add_sink',
        'agregar_alacena': 'add_cabinet',
        'agregar_mesada': 'add_counter',
        'agregar_mesada_L': 'add_l_counter',
        'agregar_personalizado': 'add_custom',
        'agregar_puerta': 'add_door',
        'agregar_ventana': 'add_window',
        'mover': 'move',
        'rotar': 'rotate',
        'eliminar': 'remove',
        'listar': 'list',
        'vista_planta': 'plan_view',
        'vista_lateral': 'side_view',
        'vista_3d': 'view_3d',
        'exportar_stl': 'export_stl',
        'importar_stl': 'import_stl',
        'guardar': 'save',
        'cargar': 'load',
        'agrupar': 'agrupar',
        'desagrupar': 'desagrupar',
        'mover_grupo': 'mover_grupo',
        'listar_grupos': 'listar_grupos',
        'ayuda': 'help',
        'salir': 'exit',
        'activar_viz_planta': 'viz_on_plan',
        'activar_viz_lateral': 'viz_on_side',
        'activar_viz_3d': 'viz_on_3d',
        'desactivar_viz': 'viz_off'
    }
    
    while True:
        try:
            cmd = input(">>> ").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split()
            comando_original = parts[0].lower()
            
            # Traducir comando si está en español
            command = comandos_es_en.get(comando_original, comando_original)
            
            # Si solo se escribió el comando sin parámetros, mostrar ayuda rápida
            if len(parts) == 1:
                # Intentar con el comando original en español
                ayuda_texto = AYUDA_COMANDOS.get(comando_original)
                
                # Si no existe ayuda para el comando en español, buscar la traducción
                if not ayuda_texto:
                    # Buscar el comando en español que traduce a este comando inglés
                    for cmd_es, cmd_en in comandos_es_en.items():
                        if cmd_en == command and cmd_es in AYUDA_COMANDOS:
                            ayuda_texto = AYUDA_COMANDOS[cmd_es]
                            break
                
                if ayuda_texto:
                    # Excepciones: comandos que no necesitan parámetros
                    comandos_sin_parametros = ['listar', 'listar_grupos', 'ayuda', 'salir', 
                                               'activar_viz_planta', 'activar_viz_lateral', 
                                               'activar_viz_3d', 'desactivar_viz',
                                               'list', 'help', 'exit', 'viz_on_plan',
                                               'viz_on_side', 'viz_on_3d', 'viz_off']
                    
                    if command not in comandos_sin_parametros and comando_original not in comandos_sin_parametros:
                        print(f"ℹ️  Uso: {ayuda_texto}")
                        continue
            
            if command == 'exit':
                print("¡Hasta luego!")
                plt.close('all')
                break
            
            # Comandos de visualización en tiempo real
            if command == 'viz_on_plan':
                VISUALIZACION_ACTIVA = 'planta'
                print("✓ Visualización de planta ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_on_side':
                VISUALIZACION_ACTIVA = 'lateral'
                print("✓ Visualización lateral ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_on_3d':
                VISUALIZACION_ACTIVA = '3d'
                print("✓ Visualización 3D ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_off':
                VISUALIZACION_ACTIVA = None
                plt.close('all')
                print("✓ Visualización en tiempo real DESACTIVADA")
                continue
            
            
            if command == 'help':
                print("""
COMANDOS DISPONIBLES (en español):

VISUALIZACIÓN EN TIEMPO REAL:
  activar_viz_planta        - Activa visualización de planta automática
  activar_viz_lateral       - Activa visualización lateral automática  
  activar_viz_3d            - Activa visualización 3D automática
  desactivar_viz            - Desactiva visualización automática

CREAR ESPACIO:
  nuevo <ancho> <largo> [altura]  - Crea espacio rectangular
  nuevo_irregular <altura> <x1,y1> <x2,y2> ... - Crea espacio irregular
    Ejemplo: nuevo_irregular 2.8 0,0 4,0 4,3 2,3 2,5 0,5

MUEBLES DE DORMITORIO:
  agregar_cama <x> <y> [z] [ancho] [largo] [nombre]
  agregar_cucheta <x> <y> [z] [ancho] [largo] [nombre]
  agregar_ropero <x> <y> [z] [ancho] [prof] [alto] [nombre]
  agregar_mesa_luz <x> <y> [z] [ancho] [prof] [nombre]
  agregar_mesa <x> <y> [z] [ancho] [prof] [nombre]

ELEMENTOS DE COCINA:
  agregar_heladera <x> <y> [z] [ancho] [prof] [alto] [nombre]
  agregar_cocina <x> <y> [z] [ancho] [prof] [nombre]
  agregar_pileta <x> <y> [z] [ancho] [prof] [nombre]
  agregar_alacena <x> <y> [z] [ancho] [prof] [alto] [nombre]
  agregar_mesada <x> <y> [z] [ancho] [prof] [nombre]
  agregar_mesada_L <x> <y> [z] [ancho1] [ancho2] [prof] [nombre]

PUERTAS Y VENTANAS:
  agregar_puerta <x> <y> [z] [ancho] [orientación] [bisagra] [swing] [nombre]
    Orientación: horizontal (ancho en X) o vertical (ancho en Y)
    Bisagra: Para horizontal: izquierda|derecha, Para vertical: arriba|abajo
    Swing: Para horizontal: norte|sur, Para vertical: este|oeste
    
    Ejemplos:
    - Horizontal, bisagras derecha, abre norte: agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada
    - Horizontal, bisagras izquierda, abre norte: agregar_puerta 2 0 0 0.9 horizontal izquierda norte cocina
    - Vertical, bisagras abajo, abre oeste: agregar_puerta 0 2 0 0.9 vertical abajo oeste baño
  
  agregar_ventana <x> <y> [z] [ancho] [alto] [nombre]
    Ejemplo: agregar_ventana 1 0 1.2 1.5 1.0 ventana_frente

MUEBLES PERSONALIZADOS:
  agregar_personalizado <nombre> <z> <altura> <x1,y1> <x2,y2> ...
    Ejemplo: agregar_personalizado isla 0 0.9 1,1 2,1 2,2 1,2

MANIPULAR OBJETOS:

AGRUPAR OBJETOS:
  agrupar <nombre_grupo> <obj1> <obj2> ...  - Crea grupo de objetos
    Ejemplo: agrupar dormitorio_principal cama mesa_luz_1 mesa_luz_2
  
  desagrupar <nombre_grupo>      - Desagrupa objetos
    Ejemplo: desagrupar dormitorio_principal
  
  mover_grupo <grupo> <dx> <dy> <dz>  - Mueve todo el grupo
    Ejemplo: mover_grupo dormitorio_principal 0.5 0 0
  
  listar_grupos                  - Lista todos los grupos creados

  mover <nombre> <x> <y> <z>     - Mueve un objeto
  rotar <nombre>                 - Rota un objeto 90°
  eliminar <nombre>              - Elimina un objeto
  listar                         - Lista todos los objetos

EXPORTAR Y GUARDAR:
  exportar_stl [archivo]         - Exporta a STL
  importar_stl <archivo> [nombre] [x] [y] [z]
  vista_planta [archivo]         - Genera vista en planta PNG
  vista_lateral [archivo]        - Genera vista lateral PNG
  vista_3d [archivo]             - Genera vista 3D PNG
  guardar [archivo]              - Guarda diseño en JSON
  cargar <archivo>               - Carga diseño desde JSON

EJEMPLOS:
  # Activar visualización en tiempo real
  >>> activar_viz_planta
  
  # Crear habitación y ver cambios en tiempo real
  >>> nuevo 4 5 2.8
  >>> agregar_cama 0.5 1.0 0 1.4 1.9 cama
  >>> agregar_puerta 2 0 0 0.9 derecha adentro entrada
  
  # Habitación irregular
  >>> nuevo_irregular 2.8 0,0 4,0 4,3 2,3 2,5 0,5
  
  # Mueble personalizado  
  >>> agregar_personalizado isla_cocina 0 0.9 1,1 2,1 2,2 1,2
""")
                continue
            
            # Comandos de visualización en tiempo real
            if command == 'viz_on_plan':
                VISUALIZACION_ACTIVA = 'planta'
                print("✓ Visualización de planta ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_on_side':
                VISUALIZACION_ACTIVA = 'lateral'
                print("✓ Visualización lateral ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_on_3d':
                VISUALIZACION_ACTIVA = '3d'
                print("✓ Visualización 3D ACTIVADA - Los cambios se mostrarán automáticamente")
                print("  (Se abrirá una ventana de matplotlib)")
                if designer:
                    designer.actualizar_visualizacion()
                continue
            
            elif command == 'viz_off':
                VISUALIZACION_ACTIVA = None
                plt.close('all')
                print("✓ Visualización en tiempo real DESACTIVADA")
                continue
            
            if command == 'new':
                w = float(parts[1]) if len(parts) > 1 else 4.0
                l = float(parts[2]) if len(parts) > 2 else 5.0
                h = float(parts[3]) if len(parts) > 3 else 2.8
                designer = RoomDesigner(w, l, h)
                print(f"Nuevo espacio creado: {w}m x {l}m x {h}m")
            
            elif command == 'new_custom':
                # new_custom 2.8 0,0 4,0 4,3 2,3 2,5 0,5
                h = float(parts[1]) if len(parts) > 1 else 2.8
                vertices = []
                for i in range(2, len(parts)):
                    coords = parts[i].split(',')
                    if len(coords) == 2:
                        vertices.append((float(coords[0]), float(coords[1])))
                if len(vertices) >= 3:
                    designer = RoomDesigner(vertices=vertices, height=h)
                    print(f"Espacio irregular creado con {len(vertices)} vértices, altura {h}m")
                else:
                    print("Error: Se necesitan al menos 3 vértices para crear un espacio irregular")
                    
            elif designer is None:
                print("Error: Primero crea un espacio con 'new' o 'new_custom'")
                
            elif command == 'add_bed':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 1.0
                l = float(parts[5]) if len(parts) > 5 else 2.0
                name = parts[6] if len(parts) > 6 else f"cama_{len(designer.objects)+1}"
                print(designer.add_bed(x, y, z, w, l, name))
                
            elif command == 'add_bunk_bed':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 1.0
                l = float(parts[5]) if len(parts) > 5 else 2.0
                name = parts[6] if len(parts) > 6 else f"cucheta_{len(designer.objects)+1}"
                print(designer.add_bunk_bed(x, y, z, w, l, name))
                
            elif command == 'add_wardrobe':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 1.5
                d = float(parts[5]) if len(parts) > 5 else 0.6
                h = float(parts[6]) if len(parts) > 6 else 2.0
                name = parts[7] if len(parts) > 7 else f"ropero_{len(designer.objects)+1}"
                print(designer.add_wardrobe(x, y, z, w, d, h, name))
                
            elif command == 'add_nightstand':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 0.5
                d = float(parts[5]) if len(parts) > 5 else 0.4
                name = parts[6] if len(parts) > 6 else f"mesa_luz_{len(designer.objects)+1}"
                print(designer.add_nightstand(x, y, z, w, d, name))
                
            elif command == 'add_table':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 1.2
                d = float(parts[5]) if len(parts) > 5 else 0.8
                name = parts[6] if len(parts) > 6 else f"mesa_{len(designer.objects)+1}"
                print(designer.add_table(x, y, z, w, d, name))
                
            elif command == 'add_fridge':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 0.7
                d = float(parts[5]) if len(parts) > 5 else 0.7
                h = float(parts[6]) if len(parts) > 6 else 1.8
                name = parts[7] if len(parts) > 7 else f"heladera_{len(designer.objects)+1}"
                print(designer.add_fridge(x, y, z, w, d, h, name))
                
            elif command == 'add_stove':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 0.6
                d = float(parts[5]) if len(parts) > 5 else 0.6
                name = parts[6] if len(parts) > 6 else f"cocina_{len(designer.objects)+1}"
                print(designer.add_stove(x, y, z, w, d, name))
                
            elif command == 'add_sink':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 0.8
                d = float(parts[5]) if len(parts) > 5 else 0.6
                name = parts[6] if len(parts) > 6 else f"pileta_{len(designer.objects)+1}"
                print(designer.add_sink(x, y, z, w, d, name))
                
            elif command == 'add_cabinet':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 1.0
                d = float(parts[5]) if len(parts) > 5 else 0.6
                h = float(parts[6]) if len(parts) > 6 else 0.9
                name = parts[7] if len(parts) > 7 else f"alacena_{len(designer.objects)+1}"
                print(designer.add_cabinet(x, y, z, w, d, h, name))
                
            elif command == 'add_counter':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w = float(parts[4]) if len(parts) > 4 else 2.0
                d = float(parts[5]) if len(parts) > 5 else 0.6
                name = parts[6] if len(parts) > 6 else f"mesada_{len(designer.objects)+1}"
                print(designer.add_counter(x, y, z, w, d, name))
            
            elif command == 'add_l_counter':
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                w1 = float(parts[4]) if len(parts) > 4 else 2.0
                w2 = float(parts[5]) if len(parts) > 5 else 1.5
                d = float(parts[6]) if len(parts) > 6 else 0.6
                name = parts[7] if len(parts) > 7 else f"mesada_L_{len(designer.objects)+1}"
                print(designer.add_L_counter(x, y, z, w1, w2, d, name))
            
            elif command == 'add_custom':
                # add_custom nombre z altura x1,y1 x2,y2 x3,y3 ...
                name = parts[1]
                z = float(parts[2])
                height = float(parts[3])
                vertices = []
                for i in range(4, len(parts)):
                    coords = parts[i].split(',')
                    if len(coords) == 2:
                        vertices.append((float(coords[0]), float(coords[1])))
                if len(vertices) >= 3:
                    print(designer.add_custom_furniture(vertices, z, height, name))
                else:
                    print("Error: Se necesitan al menos 3 vértices (formato: x,y)")
            
            elif command == 'add_door':
                # agregar_puerta x y [z] [ancho] [orientación] [bisagra] [swing] [nombre]
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 0
                width = float(parts[4]) if len(parts) > 4 else 0.9
                orientation = parts[5] if len(parts) > 5 else 'horizontal'
                hinge = parts[6] if len(parts) > 6 else 'derecha'
                swing = parts[7] if len(parts) > 7 else 'norte'
                name = parts[8] if len(parts) > 8 else f"puerta_{len(designer.objects)+1}"
                print(designer.add_door(x, y, z, width, orientation, hinge, swing, name))
            
            elif command == 'add_window':
                # agregar_ventana x y [z] [ancho] [alto] [nombre]
                x, y = float(parts[1]), float(parts[2])
                z = float(parts[3]) if len(parts) > 3 else 1.0
                width = float(parts[4]) if len(parts) > 4 else 1.2
                height = float(parts[5]) if len(parts) > 5 else 1.0
                name = parts[6] if len(parts) > 6 else f"ventana_{len(designer.objects)+1}"
                print(designer.add_window(x, y, z, width, height, name))
                
            elif command == 'move':
                name = parts[1]
                x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                print(designer.move(name, x, y, z))
            
            elif command == 'rotate':
                name = parts[1]
                print(designer.rotate(name))
                
            elif command == 'remove':
                name = parts[1]
                print(designer.remove(name))
            
            elif command == 'agrupar':
                # agrupar nombre_grupo obj1 obj2 obj3 ...
                if len(parts) < 3:
                    print("Error: Uso: agrupar nombre_grupo objeto1 objeto2 ...")
                else:
                    group_name = parts[1]
                    object_names = parts[2:]  # Lista de nombres de objetos
                    print(designer.create_group(group_name, object_names))
            
            elif command == 'desagrupar':
                # desagrupar nombre_grupo
                if len(parts) < 2:
                    print("Error: Uso: desagrupar nombre_grupo")
                else:
                    group_name = parts[1]
                    print(designer.ungroup(group_name))
            
            elif command == 'mover_grupo':
                # mover_grupo nombre_grupo offset_x offset_y offset_z
                if len(parts) < 5:
                    print("Error: Uso: mover_grupo nombre_grupo dx dy dz")
                else:
                    group_name = parts[1]
                    dx = float(parts[2])
                    dy = float(parts[3])
                    dz = float(parts[4])
                    print(designer.move_group(group_name, dx, dy, dz))
            
            elif command == 'listar_grupos':
                # listar_grupos
                print(designer.list_groups())

                
            elif command == 'list':
                print(designer.list_objects())
                
            elif command == 'export_stl':
                filename = parts[1] if len(parts) > 1 else "room_design.stl"
                print(designer.export_stl(filename))
            
            elif command == 'import_stl':
                filename = parts[1]
                name = parts[2] if len(parts) > 2 else "imported"
                x = float(parts[3]) if len(parts) > 3 else 0
                y = float(parts[4]) if len(parts) > 4 else 0
                z = float(parts[5]) if len(parts) > 5 else 0
                print(designer.import_stl(filename, name, x, y, z))
                
            elif command == 'plan_view':
                filename = parts[1] if len(parts) > 1 else "plan_view.png"
                print(designer.generate_plan_view(filename))
            
            elif command == 'side_view':
                filename = parts[1] if len(parts) > 1 else "side_view.png"
                print(designer.generate_side_view(filename))
            
            elif command == 'view_3d':
                filename = parts[1] if len(parts) > 1 else "view_3d.png"
                print(designer.generate_3d_view(filename))
                
            elif command == 'save':
                filename = parts[1] if len(parts) > 1 else "design.json"
                print(designer.save_design(filename))
                
            elif command == 'load':
                filename = parts[1]
                # Crear nuevo designer temporal para cargar
                temp_designer = RoomDesigner(4, 5, 2.8)
                result = temp_designer.load_design(filename)
                # Asignar el designer cargado
                designer = temp_designer
                print(result)
                
            else:
                print(f"Comando desconocido: {command}")
                print("Escribe 'help' para ver los comandos disponibles")
                
        except IndexError:
            print("Error: Faltan parámetros. Usa 'help' para ver la sintaxis")
        except ValueError:
            print("Error: Valor numérico inválido")
        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    interactive_mode()

    def add_generic_furniture(self, x, y, z=0, width=1.0, depth=0.6, height=1.0, name="mueble", furniture_type="generic"):
        """
        Agrega un mueble genérico (prisma rectangular)
        
        Args:
            x, y, z: Posición
            width: Ancho (X)
            depth: Profundidad (Y)
            height: Altura (Z)
            name: Nombre
            furniture_type: Tipo para identificar visualmente
                          (generic, shelf, desk, drawer, etc)
        """
        name = self._validar_nombre_unico(name)
        obj = {
            'type': furniture_type,
            'name': name,
            'x': x, 'y': y, 'z': z,
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        self.actualizar_visualizacion()
        return f"{furniture_type.capitalize()} '{name}' agregado en ({x}, {y}, {z})"
    
    def export_obj(self, filename="room_design.obj"):
        """
        Exporta el diseño a formato OBJ (más universal que STL)
        OBJ es fácil de visualizar con Blender, MeshLab, online viewers
        """
        vertices = []
        faces = []
        vertex_count = 0
        
        with open(filename, 'w') as f:
            f.write("# Room Designer OBJ Export\n")
            f.write(f"# {len(self.objects)} objects\n\n")
            
            # Exportar cada objeto
            for obj in self.objects:
                f.write(f"# Object: {obj['name']} ({obj['type']})\n")
                f.write(f"g {obj['name']}\n")
                
                # Obtener vértices del objeto
                if obj.get('is_custom') and 'vertices' in obj:
                    # Forma irregular
                    base_verts = obj['vertices']
                    z_base = obj['z']
                    z_top = z_base + obj.get('height', 1.0)
                    
                    # Base
                    for v in base_verts:
                        f.write(f"v {v[0]} {v[1]} {z_base}\n")
                    # Tope
                    for v in base_verts:
                        f.write(f"v {v[0]} {v[1]} {z_top}\n")
                    
                    n = len(base_verts)
                    # Caras laterales
                    for i in range(n):
                        next_i = (i + 1) % n
                        # Dos triángulos por cara
                        f.write(f"f {vertex_count+i+1} {vertex_count+next_i+1} {vertex_count+next_i+n+1}\n")
                        f.write(f"f {vertex_count+i+1} {vertex_count+next_i+n+1} {vertex_count+i+n+1}\n")
                    
                    # Base (invertida)
                    face_str = "f " + " ".join([str(vertex_count+i+1) for i in range(n-1, -1, -1)]) + "\n"
                    f.write(face_str)
                    
                    # Tope
                    face_str = "f " + " ".join([str(vertex_count+n+i+1) for i in range(n)]) + "\n"
                    f.write(face_str)
                    
                    vertex_count += 2 * n
                    
                else:
                    # Prisma rectangular estándar
                    x, y, z = obj['x'], obj['y'], obj['z']
                    w = obj.get('width', 1.0)
                    d = obj.get('depth', obj.get('length', 1.0))
                    h = obj.get('height', 0.6)
                    
                    # 8 vértices de la caja
                    box_verts = [
                        (x, y, z), (x+w, y, z), (x+w, y+d, z), (x, y+d, z),  # Base
                        (x, y, z+h), (x+w, y, z+h), (x+w, y+d, z+h), (x, y+d, z+h)  # Tope
                    ]
                    
                    for v in box_verts:
                        f.write(f"v {v[0]} {v[1]} {v[2]}\n")
                    
                    # 12 triángulos (6 caras × 2 triángulos)
                    faces_indices = [
                        # Base (0,1,2,3)
                        [1,2,3], [1,3,4],
                        # Tope (4,5,6,7)
                        [5,6,7], [5,7,8],
                        # Frente (0,1,5,4)
                        [1,2,6], [1,6,5],
                        # Atrás (3,2,6,7)
                        [3,4,8], [3,8,7],
                        # Izquierda (0,3,7,4)
                        [1,4,8], [1,8,5],
                        # Derecha (1,2,6,5)
                        [2,3,7], [2,7,6]
                    ]
                    
                    for face in faces_indices:
                        f.write(f"f {vertex_count+face[0]} {vertex_count+face[1]} {vertex_count+face[2]}\n")
                    
                    vertex_count += 8
                
                f.write("\n")
        
        return f"Diseño exportado a {filename} (formato OBJ)"

    def add_generic_furniture(self, x, y, z, width, depth, height, name="mueble", furniture_type="generic"):
        """
        Agrega un mueble genérico como prisma rectangular
        
        Args:
            x, y, z: Posición
            width: Ancho (X)
            depth: Profundidad (Y)
            height: Altura (Z)
            name: Nombre del mueble
            furniture_type: Tipo (mesa, silla, estante, etc) - solo descriptivo
        """
        name = self._validar_nombre_unico(name)
        obj = {
            'type': furniture_type,
            'name': name,
            'x': x,
            'y': y,
            'z': z,
            'width': width,
            'depth': depth,
            'height': height
        }
        self.objects.append(obj)
        self.actualizar_visualizacion()
        return f"{furniture_type.capitalize()} '{name}' agregado en ({x}, {y}, {z}) - {width}×{depth}×{height}m"

