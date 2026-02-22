#!/usr/bin/env python3
"""
Room Designer GUI v3.2 - VERSIÓN FINAL COMPLETA
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Arc
import numpy as np
import sys
import os
import subprocess
import platform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from room_designer import RoomDesigner

class RoomDesignerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Designer v3.2")
        self.root.geometry("1600x900")
        
        # Interceptar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.salir_con_confirmacion)
        
        self.designer = None
        self.mostrar_ayuda = True
        self.visualizacion_activa = 'planta'
        self.historial = []
        self.historial_pos = -1
        self.objeto_seleccionado = None
        self.colores_personalizados = {}
        
        self.ayuda_comandos = {
            'nuevo': 'nuevo <ancho> <largo> [altura]\n  Ej: nuevo 5 5 2.8',
            'agregar_cama': 'agregar_cama <x> <y> [z] [ancho] [largo] [nombre]\n  Ej: agregar_cama 1 1 0 1.4 1.9 cama_queen',
            'agregar_heladera': 'agregar_heladera <x> <y> [z] [ancho] [prof] [alto] [nombre]\n  Ej: agregar_heladera 0 0 0 0.7 0.7 1.8 heladera',
            'agregar_cocina': 'agregar_cocina <x> <y> [z] [ancho] [prof] [nombre]\n  Ej: agregar_cocina 1 0 0 0.6 0.6 cocina',
            'agregar_pileta': 'agregar_pileta <x> <y> [z] [ancho] [prof] [nombre]\n  Ej: agregar_pileta 2 0 0 0.8 0.6 pileta',
            'agregar_mesada': 'agregar_mesada <x> <y> [z] [ancho] [prof] [nombre]\n  Ej: agregar_mesada 0.5 0 0 2.0 0.6 mesada',
            'agregar_puerta': 'agregar_puerta <x> <y> [z] [ancho] [orient] [bisagra] [swing] [nombre]\n  orient: horizontal|vertical\n  Ej: agregar_puerta 2 0 0 0.9 horizontal derecha norte entrada',
            'agregar_mueble': 'agregar_mueble <x> <y> <z> <ancho> <prof> <alto> <nombre> [tipo]\n  Ej: agregar_mueble 2 2 0 0.8 0.6 1.5 estante biblioteca',
            'mover': 'mover <nombre> <dx> <dy> <dz>\n  Mueve RELATIVO\n  Ej: mover cama 0.5 0 0',
            'rotar': 'rotar <nombre>\n  Ej: rotar cama',
            'redimensionar': 'redimensionar <nombre> <dw> <dd> <dh>\n  Cambio RELATIVO en dimensiones\n  Ej: redimensionar mesa 0.2 -0.1 0.5\n  Con objeto seleccionado: usar flechas (0.01m/tecla)',
            'eliminar': 'eliminar <nombre>\n  Ej: eliminar cama',
            'select': 'select <nombre>\n  Selecciona objeto (desactiva ↑↓ historial)\n  Usa flechas para redimensionar\n  Ej: select cama',
            'unselect': 'unselect\n  Deselecciona objeto (reactiva ↑↓ historial)\n  Sin argumentos',
            'renombrar': 'renombrar <viejo> <nuevo>\n  Ej: renombrar cama cama_principal',
            'color': 'color <nombre> [color]\n  Ej: color cama rojo',
            'guardar': 'guardar [archivo.json]\n  Ej: guardar diseño.json',
            'cargar': 'cargar <archivo.json>\n  Ej: cargar diseño.json',
            'exportar_stl': 'exportar_stl [archivo.stl]\n  Exporta STL (sin colores, espejo corregido)\n  Ej: exportar_stl modelo.stl',
            'exportar_obj': 'exportar_obj [nombre_base]\n  Exporta OBJ+MTL (CON COLORES)\n  Ej: exportar_obj cocina\n  Genera: cocina.obj y cocina.mtl',
        }
        
        self.abreviaturas = {
            'n': 'nuevo', 'c': 'agregar_cama', 'p': 'agregar_puerta',
            'v': 'agregar_ventana', 'h': 'agregar_heladera',
            'co': 'agregar_cocina', 'pi': 'agregar_pileta',
            'ms': 'agregar_mesada', 'mb': 'agregar_mueble',
            'm': 'mover', 'r': 'rotar', 'rd': 'redimensionar', 'd': 'eliminar',
            'l': 'listar', 'g': 'guardar', 's': 'select', 'us': 'unselect',
            'e': 'exportar_stl', 'obj': 'exportar_obj',
        }
        
        self.crear_interfaz()
        self.configurar_atajos()
        
    def crear_interfaz(self):
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=7)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=0)
        
        # VISUALIZACIÓN
        viz_frame = ttk.LabelFrame(self.root, text="Visualización", padding=10)
        viz_frame.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=(10, 5))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=0)
        viz_frame.rowconfigure(1, weight=1)
        
        # Botones
        btn_frame = tk.Frame(viz_frame)
        btn_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        ttk.Button(btn_frame, text="F2: Planta", 
                  command=lambda: self.cambiar_viz('planta')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="F3: Norte", 
                  command=lambda: self.cambiar_viz('norte')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="F4: Sur", 
                  command=lambda: self.cambiar_viz('sur')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="F5: Este", 
                  command=lambda: self.cambiar_viz('este')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="F6: Oeste", 
                  command=lambda: self.cambiar_viz('oeste')).pack(side=tk.LEFT, padx=2)
        
        # BOTÓN EXPORTAR STL
        ttk.Button(btn_frame, text="📦 Exportar STL", 
                  command=self.exportar_stl_dialogo,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        
        self.btn_ayuda = ttk.Button(btn_frame, text="F1", command=self.toggle_ayuda)
        self.btn_ayuda.pack(side=tk.RIGHT, padx=5)
        
        # Canvas
        self.fig = Figure(figsize=(8, 6), dpi=90)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
        
        # AYUDA
        self.help_frame = ttk.LabelFrame(self.root, text="Ayuda", padding=10)
        self.help_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=(10, 5))
        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.rowconfigure(0, weight=1)
        
        self.help_text = scrolledtext.ScrolledText(self.help_frame, font=('Courier', 8), wrap=tk.NONE)
        self.help_text.grid(row=0, column=0, sticky='nsew')
        
        ayuda = """═══════════════════════════════════════════════════════════════════
                    ROOM DESIGNER v3.2 - GUÍA COMPLETA
═══════════════════════════════════════════════════════════════════

NAVEGACIÓN:
  F1         Panel ayuda (toggle)
  F2-F6      Vistas (Planta, Norte, Sur, Este, Oeste)
  Ctrl+E     Exportar STL (diálogo)

ESPACIO:
  nuevo [w] [l] [h]        Crear (n)              4×5×2.8m
  cargar <archivo.json>    Cargar diseño (load)
  guardar [archivo.json]   Guardar diseño (g)
  listar                   Lista objetos (l)
  salir / exit             Salir (pregunta si guardar)

MUEBLES BÁSICOS:
  agregar_cama <x> <y> [nombre]                    (c)
  agregar_puerta <x> <y> [z] [w] [o] [b] [s] [n]  (p)
  agregar_ventana <x> <y> <z> <w> <h> [nombre]    (v)
    Orient: horizontal|vertical
    Bisagra: derecha|izquierda
    Swing: norte|sur|este|oeste

COCINA:
  agregar_heladera <x> <y> [z] [w] [d] [h] [n]    (h)
  agregar_cocina <x> <y> [z] [w] [d] [n]          (co)
  agregar_pileta <x> <y> [z] [w] [d] [n]          (pi)
  agregar_mesada <x> <y> [z] [w] [d] [n]          (ms)

MUEBLE PERSONALIZADO:
  agregar_mueble <x> <y> <z> <w> <d> <h> <n> [tipo]  (mb)

EDICIÓN:
  select <nombre>          Seleccionar (s) → modo redimensionar
  unselect                 Deseleccionar (us) → restaura historial
  mover <obj> <dx> <dy> <dz>                 Relativo (m)
  rotar <obj>              90° (r)
  redimensionar <obj> <dw> <dd> <dh>         Relativo (rd)
    CON OBJETO SELECCIONADO usar FLECHAS (0.01m/tecla):
    Vista Planta:  ←→ ancho(W)  ↑↓ prof(D)
    Vista N/S:     ←→ ancho(W)  ↑↓ alto(H)
    Vista E/O:     ←→ prof(D)   ↑↓ alto(H)
  
  renombrar <viejo> <nuevo>
  color <nombre> [color]   Sin color → abre selector
  eliminar <nombre>        (d)

EXPORTAR:
  exportar_stl [archivo.stl]      Sin colores (e)
  exportar_obj [nombre]            CON COLORES (obj)
    Genera: nombre.obj + nombre.mtl

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
  Escribir comando solo (sin parámetros) muestra sintaxis
  Ejemplo: >>> redimensionar
           ℹ️  redimensionar <nombre> <dw> <dd> <dh>

AUTOCOMPLETAR:
  Ctrl+Space    Completa comando

HISTORIAL:
  ↑↓           Comandos anteriores (si NO hay objeto seleccionado)
  
MÚLTIPLES COMANDOS:
  cmd1; cmd2; cmd3    Ejecuta secuencia

═══════════════════════════════════════════════════════════════════
Presiona F1 para ocultar esta ayuda
═══════════════════════════════════════════════════════════════════
"""
        self.help_text.insert('1.0', ayuda)
        self.help_text.config(state=tk.DISABLED)
        
        # SALIDA
        output_frame = ttk.LabelFrame(self.root, text="Salida", padding=5)
        output_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, font=('Courier', 9))
        self.output_text.grid(row=0, column=0, sticky='nsew')
        
        # COMANDOS
        cmd_frame = ttk.LabelFrame(self.root, text="Comandos (↑/↓)", padding=8)
        cmd_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=(5, 10))
        cmd_frame.columnconfigure(1, weight=1)
        
        tk.Label(cmd_frame, text=">>>", font=('Courier', 12, 'bold')).grid(row=0, column=0, padx=(0, 8))
        
        self.command_entry = ttk.Entry(cmd_frame, font=('Courier', 11))
        self.command_entry.grid(row=0, column=1, sticky='ew', padx=(0, 8))
        self.command_entry.bind('<Return>', self.ejecutar_comando)
        self.command_entry.bind('<Control-space>', self.autocompletar)
        
        # Guardar referencias a los bindings originales
        self.historial_bindings_activos = True
        self.activar_historial_bindings()
        
        ttk.Button(cmd_frame, text="Ejecutar", command=self.ejecutar_comando).grid(row=0, column=2, padx=3)
        ttk.Button(cmd_frame, text="Limpiar", command=self.limpiar_salida).grid(row=0, column=3, padx=3)
        
        self.command_entry.focus()
        
        self.escribir_salida("="*60)
        self.escribir_salida("ROOM DESIGNER v3.2 FINAL")
        self.escribir_salida("="*60)
        self.escribir_salida("✓ Ayuda completa: F1")
        self.escribir_salida("✓ Autocompletar: Ctrl+Space")
        self.escribir_salida("✓ Exportar: exportar_stl (e) | exportar_obj (obj)")
        self.escribir_salida("✓ Redimensionar: select + flechas | rd comando\n")
        
        self.mostrar_mensaje_inicial()
    
    def configurar_atajos(self):
        self.root.bind('<F1>', lambda e: self.toggle_ayuda())
        self.root.bind('<F2>', lambda e: self.cambiar_viz('planta'))
        self.root.bind('<F3>', lambda e: self.cambiar_viz('norte'))
        self.root.bind('<F4>', lambda e: self.cambiar_viz('sur'))
        self.root.bind('<F5>', lambda e: self.cambiar_viz('este'))
        self.root.bind('<F6>', lambda e: self.cambiar_viz('oeste'))
        self.root.bind('<Control-e>', lambda e: self.exportar_stl_dialogo())
        
        # Flechas para redimensionar objeto seleccionado
        self.root.bind('<Left>', lambda e: self.redimensionar_con_flecha('left'))
        self.root.bind('<Right>', lambda e: self.redimensionar_con_flecha('right'))
        self.root.bind('<Up>', lambda e: self.redimensionar_con_flecha('up'))
        self.root.bind('<Down>', lambda e: self.redimensionar_con_flecha('down'))
    
    def redimensionar_con_flecha(self, direccion):
        """Redimensiona el objeto seleccionado según la vista y dirección"""
        # Solo redimensionar si:
        # 1. Hay objeto seleccionado
        # 2. Los bindings de historial están desactivados
        if not self.objeto_seleccionado or not self.designer or self.historial_bindings_activos:
            return
        
        delta = 0.01  # 1cm por tecla
        dw, dd, dh = 0, 0, 0
        
        if self.visualizacion_activa == 'planta':
            # Vista de planta: flechas controlan width (X) y depth (Y)
            if direccion == 'left':
                dw = -delta  # Reduce width
            elif direccion == 'right':
                dw = delta   # Aumenta width
            elif direccion == 'up':
                dd = -delta  # Reduce depth
            elif direccion == 'down':
                dd = delta   # Aumenta depth
        
        elif self.visualizacion_activa in ['norte', 'sur']:
            # Vistas Norte/Sur: flechas controlan width (X) y height (Z)
            if direccion == 'left':
                dw = -delta  # Reduce width
            elif direccion == 'right':
                dw = delta   # Aumenta width
            elif direccion == 'up':
                dh = delta   # Aumenta height
            elif direccion == 'down':
                dh = -delta  # Reduce height
        
        elif self.visualizacion_activa in ['este', 'oeste']:
            # Vistas Este/Oeste: flechas controlan depth (Y) y height (Z)
            if direccion == 'left':
                dd = -delta  # Reduce depth
            elif direccion == 'right':
                dd = delta   # Aumenta depth
            elif direccion == 'up':
                dh = delta   # Aumenta height
            elif direccion == 'down':
                dh = -delta  # Reduce height
        
        # Aplicar redimensionamiento
        resultado = self.designer.resize(self.objeto_seleccionado, dw, dd, dh)
        self.escribir_salida(resultado)
        self.actualizar_viz()
    
    def activar_historial_bindings(self):
        """Activa los bindings de flechas para historial de comandos"""
        self.command_entry.bind('<Up>', self.historial_anterior)
        self.command_entry.bind('<Down>', self.historial_siguiente)
        self.historial_bindings_activos = True
    
    def desactivar_historial_bindings(self):
        """Desactiva los bindings de flechas (para modo redimensionar)"""
        self.command_entry.unbind('<Up>')
        self.command_entry.unbind('<Down>')
        self.historial_bindings_activos = False
    
    def autocompletar(self, event=None):
        """Autocompleta el comando actual (Ctrl+Space)"""
        texto_actual = self.command_entry.get().strip()
        if not texto_actual:
            return
        
        # Buscar comandos que empiecen con el texto actual
        comandos_posibles = []
        
        # Buscar en comandos principales
        for cmd in self.ayuda_comandos.keys():
            if cmd.startswith(texto_actual.lower()):
                comandos_posibles.append(cmd)
        
        # Buscar en abreviaturas
        for abrev, cmd in self.abreviaturas.items():
            if abrev.startswith(texto_actual.lower()):
                comandos_posibles.append(abrev)
        
        # Eliminar duplicados y ordenar
        comandos_posibles = sorted(list(set(comandos_posibles)))
        
        if len(comandos_posibles) == 0:
            self.escribir_salida(f"❌ No hay comandos que empiecen con '{texto_actual}'")
        elif len(comandos_posibles) == 1:
            # Un solo match - completar
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, comandos_posibles[0] + " ")
        else:
            # Múltiples matches - mostrar opciones
            self.escribir_salida(f"\n💡 Comandos disponibles con '{texto_actual}':")
            for cmd in comandos_posibles:
                # Mostrar si es abreviatura
                if cmd in self.abreviaturas:
                    self.escribir_salida(f"  {cmd} → {self.abreviaturas[cmd]}")
                else:
                    self.escribir_salida(f"  {cmd}")
            
            # Completar con el prefijo común más largo
            if comandos_posibles:
                prefijo_comun = comandos_posibles[0]
                for cmd in comandos_posibles[1:]:
                    # Encontrar prefijo común
                    i = 0
                    while i < min(len(prefijo_comun), len(cmd)) and prefijo_comun[i] == cmd[i]:
                        i += 1
                    prefijo_comun = prefijo_comun[:i]
                
                if len(prefijo_comun) > len(texto_actual):
                    self.command_entry.delete(0, tk.END)
                    self.command_entry.insert(0, prefijo_comun)
        
        return "break"  # Prevenir comportamiento por defecto
    
    def salir_con_confirmacion(self):
        """Pregunta si guardar antes de salir"""
        if not self.designer or len(self.designer.objects) == 0:
            # No hay nada que guardar
            if messagebox.askyesno("Salir", "¿Salir del programa?"):
                self.root.quit()
            return
        
        # Preguntar si quiere guardar
        respuesta = messagebox.askyesnocancel(
            "Guardar cambios",
            "¿Desea guardar los cambios antes de salir?"
        )
        
        if respuesta is None:  # Cancelar
            return
        elif respuesta:  # Sí - guardar
            # Pedir nombre de archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile="design.json",
                title="Guardar diseño"
            )
            
            if filename:
                try:
                    resultado = self.designer.save_design(filename)
                    self.escribir_salida(f"\n✓ {resultado}")
                    # Cerrar directamente sin messagebox adicional
                    self.root.quit()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al guardar:\n{e}")
            # Si canceló el guardar, no salir
        else:  # No - salir sin guardar
            self.root.quit()
    
    def exportar_stl_dialogo(self):
        """Exportar STL con diálogo"""
        if not self.designer:
            messagebox.showwarning("Exportar STL", "Crea un espacio primero")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")],
            initialfile="modelo.stl"
        )
        
        if filename:
            try:
                result = self.designer.export_stl(filename)
                self.escribir_salida(f"\n✓ {result}")
                
                # Preguntar si abrir
                if messagebox.askyesno("STL Exportado", 
                    f"Archivo guardado:\n{filename}\n\n¿Abrir en visor 3D?"):
                    self.abrir_visor_3d(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Error exportando STL:\n{e}")
    
    def abrir_visor_3d(self, filename):
        """Abre archivo 3D en visor del sistema"""
        sistema = platform.system()
        
        try:
            if sistema == "Windows":
                os.startfile(filename)
            elif sistema == "Darwin":  # macOS
                subprocess.call(['open', filename])
            else:  # Linux
                visores = ['meshlab', 'blender', 'f3d', 'xdg-open']
                for visor in visores:
                    try:
                        subprocess.Popen([visor, filename])
                        self.escribir_salida(f"✓ Abriendo en {visor}")
                        return
                    except FileNotFoundError:
                        continue
                self.escribir_salida("ℹ️ Instala: meshlab o blender")
        except Exception as e:
            self.escribir_salida(f"ℹ️ Abre manualmente: {filename}")
    
    def historial_anterior(self, event):
        if not self.historial:
            return "break"
        if self.historial_pos == -1:
            self.historial_pos = len(self.historial) - 1
        elif self.historial_pos > 0:
            self.historial_pos -= 1
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, self.historial[self.historial_pos])
        return "break"
    
    def historial_siguiente(self, event):
        if not self.historial or self.historial_pos == -1:
            return "break"
        if self.historial_pos < len(self.historial) - 1:
            self.historial_pos += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.historial[self.historial_pos])
        else:
            self.historial_pos = -1
            self.command_entry.delete(0, tk.END)
        return "break"
    
    def mostrar_mensaje_inicial(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, 
                    'ROOM DESIGNER v3.2\n\n'
                    'Nuevo:\n'
                    '📦 Botón "Exportar STL"\n'
                    '📦 Comando: exportar_stl\n\n'
                    'Prueba:\n'
                    'n 5 5\n'
                    'h 0 0\n'
                    'exportar_stl\n\n'
                    'Grid cada 0.1m\n'
                    'Coordenadas visibles',
                    ha='center', va='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        self.ax.axis('off')
        self.canvas.draw()
    
    def toggle_ayuda(self):
        if self.mostrar_ayuda:
            self.help_frame.grid_remove()
            self.mostrar_ayuda = False
        else:
            self.help_frame.grid()
            self.mostrar_ayuda = True
    
    def limpiar_salida(self):
        self.output_text.delete('1.0', tk.END)
    
    def cambiar_viz(self, tipo):
        self.visualizacion_activa = tipo
        self.escribir_salida(f"✓ Vista {tipo.upper()}")
        if self.designer:
            self.actualizar_viz()
    
    def actualizar_viz(self):
        if not self.designer:
            return
        self.ax.clear()
        if self.visualizacion_activa == 'planta':
            self._dibujar_planta()
        elif self.visualizacion_activa in ['norte', 'sur', 'este', 'oeste']:
            self._dibujar_lateral(self.visualizacion_activa)
        self.canvas.draw()
    
    def _dibujar_planta(self):
        # Cuarto
        if self.designer.is_irregular:
            xs = [v[0] for v in self.designer.vertices] + [self.designer.vertices[0][0]]
            ys = [v[1] for v in self.designer.vertices] + [self.designer.vertices[0][1]]
            self.ax.fill(xs, ys, facecolor='white', edgecolor='black', linewidth=2.5)
        else:
            rect = Rectangle((0, 0), self.designer.width, self.designer.length,
                           linewidth=2.5, edgecolor='black', facecolor='white')
            self.ax.add_patch(rect)
        
        colors_default = {
            'bed': '#FFB6C1', 'wardrobe': '#8B4513', 'table': '#DEB887',
            'fridge': '#B0C4DE', 'counter': '#F5DEB3', 'door': '#D2B48C',
            'window': '#87CEEB', 'nightstand': '#D2691E', 'stove': '#FF6347',
            'sink': '#4682B4', 'cabinet': '#A0522D', 'generic': '#DDA0DD'
        }
        
        for obj in self.designer.objects:
            if obj['name'] in self.colores_personalizados:
                color = self.colores_personalizados[obj['name']]
            else:
                color = colors_default.get(obj['type'], '#CCC')
            
            x, y = obj['x'], obj['y']
            
            if obj['type'] == 'door':
                self._dibujar_puerta_con_arco(obj, color)
            else:
                w = obj.get('width', 1.0)
                d = obj.get('depth', obj.get('length', 1.0))
                rect = Rectangle((x, y), w, d, linewidth=1.5,
                               edgecolor='black', facecolor=color, alpha=0.7)
                self.ax.add_patch(rect)
                
                nombre = obj['name']
                coords = f"({x:.2f}, {y:.2f})"
                texto = f"{nombre}\n{coords}"
                self.ax.text(x + w/2, y + d/2, texto,
                           ha='center', va='center', fontsize=7, fontweight='bold')
        
        self.ax.set_xlim(-0.5, self.designer.width + 0.5)
        self.ax.set_ylim(-0.5, self.designer.length + 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        
        self.ax.grid(True, alpha=0.5, linestyle='-', linewidth=0.8, color='gray')
        self.ax.set_xticks(np.arange(0, self.designer.width + 0.5, 0.1), minor=True)
        self.ax.set_yticks(np.arange(0, self.designer.length + 0.5, 0.1), minor=True)
        self.ax.grid(True, which='minor', alpha=0.2, linestyle=':', linewidth=0.5)
        self.ax.set_xticks(np.arange(0, self.designer.width + 0.5, 0.5))
        self.ax.set_yticks(np.arange(0, self.designer.length + 0.5, 0.5))
        
        self.ax.set_title(f'Planta - {self.designer.width:.1f}m × {self.designer.length:.1f}m')
    
    def _dibujar_puerta_con_arco(self, obj, color):
        x, y = obj['x'], obj['y']
        w = obj.get('width', 0.9)
        t = obj.get('thickness', 0.1)
        o = obj.get('orientation', 'horizontal')
        h = obj.get('hinge', 'derecha')
        s = obj.get('swing', 'norte')
        
        if o == 'horizontal':
            rect = Rectangle((x, y), w, t, linewidth=1.5, 
                           edgecolor='black', facecolor=color, alpha=0.8)
            self.ax.add_patch(rect)
            if h == 'derecha':
                pivot_x = x + w
                if s == 'norte':
                    pivot_y = y
                    theta1, theta2 = 90, 180
                    end_x, end_y = pivot_x - w, pivot_y + w
                else:
                    pivot_y = y + t
                    theta1, theta2 = 180, 270
                    end_x, end_y = pivot_x - w, pivot_y - w
            else:
                pivot_x = x
                if s == 'norte':
                    pivot_y = y
                    theta1, theta2 = 0, 90
                    end_x, end_y = pivot_x + w, pivot_y + w
                else:
                    pivot_y = y + t
                    theta1, theta2 = 270, 360
                    end_x, end_y = pivot_x + w, pivot_y - w
            cx, cy = x + w/2, y + t/2
        else:
            rect = Rectangle((x, y), t, w, linewidth=1.5,
                           edgecolor='black', facecolor=color, alpha=0.8)
            self.ax.add_patch(rect)
            if h == 'abajo':
                pivot_y = y
                if s == 'este':
                    pivot_x = x + t
                    theta1, theta2 = 0, 90
                    end_x, end_y = pivot_x + w, pivot_y + w
                else:
                    pivot_x = x
                    theta1, theta2 = 90, 180
                    end_x, end_y = pivot_x - w, pivot_y + w
            else:
                pivot_y = y + w
                if s == 'este':
                    pivot_x = x + t
                    theta1, theta2 = 270, 360
                    end_x, end_y = pivot_x + w, pivot_y - w
                else:
                    pivot_x = x
                    theta1, theta2 = 180, 270
                    end_x, end_y = pivot_x - w, pivot_y - w
            cx, cy = x + t/2, y + w/2
        
        arc = Arc((pivot_x, pivot_y), w*2, w*2, 
                 angle=0, theta1=theta1, theta2=theta2,
                 color='red', linewidth=1.5, linestyle='--', alpha=0.7)
        self.ax.add_patch(arc)
        self.ax.plot([pivot_x, end_x], [pivot_y, end_y], 
                    color='red', linewidth=1.5, alpha=0.6)
        
        nombre = obj['name']
        coords = f"({x:.2f}, {y:.2f})"
        texto = f"{nombre}\n{coords}"
        self.ax.text(cx, cy, texto, ha='center', va='center',
                   fontsize=6, fontweight='bold')
    
    def _dibujar_lateral(self, vista):
        """Dibuja vista lateral (elevación) con muebles"""
        w, l, h = self.designer.width, self.designer.length, self.designer.height
        
        # Colores para muebles
        colors_default = {
            'bed': '#FFB6C1', 'wardrobe': '#8B4513', 'table': '#DEB887',
            'fridge': '#B0C4DE', 'counter': '#F5DEB3', 'door': '#D2B48C',
            'window': '#87CEEB', 'nightstand': '#D2691E', 'stove': '#FF6347',
            'sink': '#4682B4', 'cabinet': '#A0522D', 'generic': '#DDA0DD'
        }
        
        if vista == 'norte':
            # Vista desde +Y mirando hacia -Y
            # Eje X horizontal (izq a der), Z vertical (abajo a arriba)
            # Dibujar paredes (piso, izquierda, derecha)
            self.ax.plot([0, w], [0, 0], 'k-', lw=3)  # Piso
            self.ax.plot([0, 0], [0, h], 'k-', lw=3)  # Pared izquierda
            self.ax.plot([w, w], [0, h], 'k-', lw=3)  # Pared derecha
            
            # Dibujar muebles que están cerca del frente (Y pequeño)
            for obj in self.designer.objects:
                obj_y = obj['y']
                obj_depth = obj.get('depth', obj.get('length', 1.0))
                
                # Solo mostrar objetos del frente (Y entre 0 y 1m aproximadamente)
                if obj_y < 1.5:
                    obj_x = obj['x']
                    obj_z = obj['z']
                    obj_w = obj.get('width', 1.0)
                    obj_h = obj.get('height', 1.0)
                    
                    color = self.colores_personalizados.get(obj['name'], 
                            colors_default.get(obj['type'], '#CCC'))
                    
                    # Dibujar rectángulo (proyección en XZ)
                    rect = Rectangle((obj_x, obj_z), obj_w, obj_h,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    self.ax.add_patch(rect)
                    self.ax.text(obj_x + obj_w/2, obj_z + obj_h/2, obj['name'],
                               ha='center', va='center', fontsize=7)
            
            self.ax.set_xlim(-0.5, w + 0.5)
            titulo = f'Norte (frente) - {w:.1f}m × {h:.1f}m'
            
        elif vista == 'sur':
            # Vista desde -Y mirando hacia +Y (estás al sur mirando al norte)
            # El eje X debe invertirse para mantener coherencia
            self.ax.plot([0, w], [0, 0], 'k-', lw=3)
            self.ax.plot([0, 0], [0, h], 'k-', lw=3)
            self.ax.plot([w, w], [0, h], 'k-', lw=3)
            
            # Muebles del fondo (Y grande)
            for obj in self.designer.objects:
                obj_y = obj['y']
                obj_depth = obj.get('depth', obj.get('length', 1.0))
                
                # Objetos del fondo (Y > l-1.5)
                if obj_y > l - 1.5:
                    obj_x = obj['x']
                    obj_z = obj['z']
                    obj_w = obj.get('width', 1.0)
                    obj_h = obj.get('height', 1.0)
                    
                    color = self.colores_personalizados.get(obj['name'], 
                            colors_default.get(obj['type'], '#CCC'))
                    
                    # INVERTIR X para corregir espejo: usar (w - obj_x - obj_w) en lugar de obj_x
                    rect = Rectangle((w - obj_x - obj_w, obj_z), obj_w, obj_h,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    self.ax.add_patch(rect)
                    self.ax.text((w - obj_x - obj_w) + obj_w/2, obj_z + obj_h/2, obj['name'],
                               ha='center', va='center', fontsize=7)
            
            self.ax.set_xlim(-0.5, w + 0.5)
            titulo = f'Sur (fondo) - {w:.1f}m × {h:.1f}m'
            
        elif vista == 'este':
            # Vista desde +X mirando hacia -X
            # Eje Y horizontal (izq a der), Z vertical
            self.ax.plot([0, l], [0, 0], 'k-', lw=3)
            self.ax.plot([0, 0], [0, h], 'k-', lw=3)
            self.ax.plot([l, l], [0, h], 'k-', lw=3)
            
            # Muebles de la derecha (X grande)
            for obj in self.designer.objects:
                obj_x = obj['x']
                obj_w = obj.get('width', 1.0)
                
                # Objetos de la derecha (X > w-1.5)
                if obj_x > w - 1.5:
                    obj_y = obj['y']
                    obj_z = obj['z']
                    obj_d = obj.get('depth', obj.get('length', 1.0))
                    obj_h = obj.get('height', 1.0)
                    
                    color = self.colores_personalizados.get(obj['name'], 
                            colors_default.get(obj['type'], '#CCC'))
                    
                    rect = Rectangle((obj_y, obj_z), obj_d, obj_h,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    self.ax.add_patch(rect)
                    self.ax.text(obj_y + obj_d/2, obj_z + obj_h/2, obj['name'],
                               ha='center', va='center', fontsize=7)
            
            self.ax.set_xlim(-0.5, l + 0.5)
            titulo = f'Este (derecha) - {l:.1f}m × {h:.1f}m'
            
        else:  # oeste
            # Vista desde -X mirando hacia +X (estás al oeste mirando al este)
            # El eje Y debe invertirse para mantener coherencia
            self.ax.plot([0, l], [0, 0], 'k-', lw=3)
            self.ax.plot([0, 0], [0, h], 'k-', lw=3)
            self.ax.plot([l, l], [0, h], 'k-', lw=3)
            
            # Muebles de la izquierda (X pequeño)
            for obj in self.designer.objects:
                obj_x = obj['x']
                
                # Objetos de la izquierda (X < 1.5)
                if obj_x < 1.5:
                    obj_y = obj['y']
                    obj_z = obj['z']
                    obj_d = obj.get('depth', obj.get('length', 1.0))
                    obj_h = obj.get('height', 1.0)
                    
                    color = self.colores_personalizados.get(obj['name'], 
                            colors_default.get(obj['type'], '#CCC'))
                    
                    # INVERTIR Y para corregir espejo: usar (l - obj_y - obj_d)
                    rect = Rectangle((l - obj_y - obj_d, obj_z), obj_d, obj_h,
                                   linewidth=1.5, edgecolor='black', 
                                   facecolor=color, alpha=0.7)
                    self.ax.add_patch(rect)
                    self.ax.text((l - obj_y - obj_d) + obj_d/2, obj_z + obj_h/2, obj['name'],
                               ha='center', va='center', fontsize=7)
            
            self.ax.set_xlim(-0.5, l + 0.5)
            titulo = f'Oeste (izquierda) - {l:.1f}m × {h:.1f}m'
        
        self.ax.set_ylim(-0.2, h + 0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title(titulo)
    
    def ejecutar_comando(self, event=None):
        cmd = self.command_entry.get().strip()
        if not cmd:
            return
        
        self.historial.append(cmd)
        self.historial_pos = -1
        
        parts = cmd.split()
        if len(parts) == 1:
            comando = parts[0].lower()
            if comando in self.abreviaturas:
                comando = self.abreviaturas[comando]
            if comando in self.ayuda_comandos:
                self.escribir_salida(f"\nℹ️  {self.ayuda_comandos[comando]}\n")
                self.command_entry.delete(0, tk.END)
                return
        
        if ';' in cmd:
            for subcmd in cmd.split(';'):
                subcmd = subcmd.strip()
                if subcmd:
                    self.escribir_salida(f"\n>>> {subcmd}")
                    try:
                        res = self.procesar_comando(subcmd)
                        if res:
                            self.escribir_salida(res)
                    except Exception as e:
                        self.escribir_salida(f"❌ {e}")
        else:
            self.escribir_salida(f"\n>>> {cmd}")
            try:
                res = self.procesar_comando(cmd)
                if res:
                    self.escribir_salida(res)
            except Exception as e:
                self.escribir_salida(f"❌ {e}")
        
        self.command_entry.delete(0, tk.END)
        if self.designer:
            self.actualizar_viz()
    
    def procesar_comando(self, cmd):
        parts = cmd.split()
        if not parts:
            return ""
        
        c = parts[0].lower()
        if c in self.abreviaturas:
            parts[0] = self.abreviaturas[c]
            c = parts[0]
        
        if c in ['salir', 'exit']:
            self.salir_con_confirmacion()
            return ""
        
        if c in ['nuevo', 'new']:
            w = float(parts[1]) if len(parts) > 1 else 4.0
            l = float(parts[2]) if len(parts) > 2 else 5.0
            h = float(parts[3]) if len(parts) > 3 else 2.8
            self.designer = RoomDesigner(w, l, h)
            return f"✓ {w}×{l}×{h}m"
        
        if c in ['cargar', 'load']:
            f = parts[1] if len(parts) > 1 else "design.json"
            t = RoomDesigner(4, 5, 2.8)
            r = t.load_design(f)
            self.designer = t
            return f"✓ {r}"
        
        if not self.designer:
            return "❌ Crea espacio: nuevo <ancho> <largo>"
        
        # EXPORTAR STL
        if c == 'exportar_stl':
            f = parts[1] if len(parts) > 1 else "modelo.stl"
            return self.designer.export_stl(f)
        
        # EXPORTAR OBJ CON COLORES
        if c in ['exportar_obj', 'export_obj']:
            f = parts[1] if len(parts) > 1 else "modelo"
            return self.designer.export_obj_with_colors(f)
        
        if c == 'select':
            if len(parts) > 1:
                self.objeto_seleccionado = parts[1]
                self.desactivar_historial_bindings()
                return f"✓ '{parts[1]}' seleccionado\n  Flechas: redimensionar (↑↓ deshabilitadas para historial)\n  Usar 'unselect' para restaurar historial"
            return "select <nombre>"
        
        if c in ['unselect', 'deseleccionar']:
            if self.objeto_seleccionado:
                nombre = self.objeto_seleccionado
                self.objeto_seleccionado = None
                self.activar_historial_bindings()
                return f"✓ '{nombre}' deseleccionado\n  Flechas ↑↓ restauradas para historial de comandos"
            return "No hay objeto seleccionado"
        
        if c == 'renombrar':
            if len(parts) < 3:
                return "renombrar <viejo> <nuevo>"
            viejo, nuevo = parts[1], parts[2]
            for obj in self.designer.objects:
                if obj['name'] == viejo:
                    obj['name'] = nuevo
                    return f"✓ '{viejo}' → '{nuevo}'"
            return f"❌ No encontrado: {viejo}"
        
        if c == 'color':
            if len(parts) < 2:
                return "color <nombre> [color]"
            nombre = parts[1]
            if len(parts) >= 3:
                color = parts[2]
                self.colores_personalizados[nombre] = color
                return f"✓ Color '{color}' para '{nombre}'"
            else:
                color = colorchooser.askcolor(title=f"Color para {nombre}")
                if color[1]:
                    self.colores_personalizados[nombre] = color[1]
                    return f"✓ Color aplicado a '{nombre}'"
                return "Cancelado"
        
        if c == 'agregar_heladera':
            x, y = float(parts[1]), float(parts[2])
            z = float(parts[3]) if len(parts) > 3 else 0
            w = float(parts[4]) if len(parts) > 4 else 0.7
            d = float(parts[5]) if len(parts) > 5 else 0.7
            h = float(parts[6]) if len(parts) > 6 else 1.8
            n = parts[7] if len(parts) > 7 else "heladera"
            return self.designer.add_fridge(x, y, z, w, d, h, n)
        
        elif c == 'agregar_cocina':
            x, y = float(parts[1]), float(parts[2])
            z = float(parts[3]) if len(parts) > 3 else 0
            w = float(parts[4]) if len(parts) > 4 else 0.6
            d = float(parts[5]) if len(parts) > 5 else 0.6
            n = parts[6] if len(parts) > 6 else "cocina"
            return self.designer.add_stove(x, y, z, w, d, n)
        
        elif c == 'agregar_pileta':
            x, y = float(parts[1]), float(parts[2])
            z = float(parts[3]) if len(parts) > 3 else 0
            w = float(parts[4]) if len(parts) > 4 else 0.8
            d = float(parts[5]) if len(parts) > 5 else 0.6
            n = parts[6] if len(parts) > 6 else "pileta"
            return self.designer.add_sink(x, y, z, w, d, n)
        
        elif c == 'agregar_mesada':
            x, y = float(parts[1]), float(parts[2])
            z = float(parts[3]) if len(parts) > 3 else 0
            w = float(parts[4]) if len(parts) > 4 else 2.0
            d = float(parts[5]) if len(parts) > 5 else 0.6
            n = parts[6] if len(parts) > 6 else "mesada"
            return self.designer.add_counter(x, y, z, w, d, n)
        
        elif c == 'agregar_mueble':
            if len(parts) < 8:
                return "agregar_mueble <x> <y> <z> <w> <d> <h> <nombre> [tipo]"
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            w, d, h = float(parts[4]), float(parts[5]), float(parts[6])
            n = parts[7]
            tipo = parts[8] if len(parts) > 8 else "mueble"
            return self.designer.add_generic_furniture(x, y, z, w, d, h, n, tipo)
        
        elif c == 'agregar_cama':
            x, y = float(parts[1]), float(parts[2])
            n = parts[3] if len(parts) > 3 else "cama"
            return self.designer.add_bed(x, y, 0, 1.4, 1.9, n)
        
        elif c == 'agregar_puerta':
            x, y = float(parts[1]), float(parts[2])
            w = float(parts[3]) if len(parts) > 3 else 0.9
            o = parts[4] if len(parts) > 4 else 'horizontal'
            h = parts[5] if len(parts) > 5 else 'derecha'
            s = parts[6] if len(parts) > 6 else 'norte'
            n = parts[7] if len(parts) > 7 else "puerta"
            return self.designer.add_door(x, y, 0, w, o, h, s, n)
        
        elif c == 'mover':
            if self.objeto_seleccionado and len(parts) == 4:
                dx, dy, dz = float(parts[1]), float(parts[2]), float(parts[3])
                return self.designer.move(self.objeto_seleccionado, dx, dy, dz)
            elif len(parts) >= 5:
                n = parts[1]
                dx, dy, dz = float(parts[2]), float(parts[3]), float(parts[4])
                return self.designer.move(n, dx, dy, dz)
            return "mover <obj> <dx> <dy> <dz>"
        
        elif c == 'rotar':
            n = parts[1] if len(parts) > 1 else self.objeto_seleccionado
            if n:
                return self.designer.rotate(n)
            return "rotar <nombre>"
        
        elif c == 'redimensionar':
            if self.objeto_seleccionado and len(parts) == 4:
                dw, dd, dh = float(parts[1]), float(parts[2]), float(parts[3])
                return self.designer.resize(self.objeto_seleccionado, dw, dd, dh)
            elif len(parts) >= 5:
                n = parts[1]
                dw, dd, dh = float(parts[2]), float(parts[3]), float(parts[4])
                return self.designer.resize(n, dw, dd, dh)
            return "redimensionar <nombre> <dw> <dd> <dh>"
        
        elif c == 'eliminar':
            n = parts[1] if len(parts) > 1 else self.objeto_seleccionado
            if n:
                return self.designer.remove(n)
            return "eliminar <nombre>"
        
        elif c == 'listar':
            return self.designer.list_objects()
        
        elif c == 'guardar':
            f = parts[1] if len(parts) > 1 else "design.json"
            return self.designer.save_design(f)
        
        return f"❓ Desconocido: {c}"
    
    def escribir_salida(self, txt):
        self.output_text.insert(tk.END, txt + '\n')
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomDesignerGUI(root)
    root.mainloop()
