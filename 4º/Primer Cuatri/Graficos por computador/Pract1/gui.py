import tkinter as tk
from tkinter import ttk, messagebox

class LineDrawingGUI(ttk.Frame):
    def __init__(self, parent, draw_callback):
        super().__init__(parent)
        self.parent = parent
        self.draw_callback = draw_callback
        self.parent.title("Visualizador de Algoritmos de Línea")
        self.parent.geometry("820x620")
        self.points = []
        # Canvas SIEMPRE 500x500
        self.canvas_size = 500
        self.canvas = tk.Canvas(self, bg="white", width=self.canvas_size, height=self.canvas_size, bd=2, relief="sunken")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Estado de clicks (coordenadas lógicas de cuadrícula)
        self.start = None
        self.end = None
        self.last_start = None
        self.last_end = None

        # Centro en coordenadas de pantalla (para ejes)
        self.width = int(self.canvas["width"])
        self.height = int(self.canvas["height"])
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # Panel de controles
        controles = ttk.Frame(self)
        controles.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        algos = [           
            "slope_intercept_modified",
            "dda_algorithm",
            "bresenham_integer",
        ]


        ttk.Label(controles, text="Algoritmo:").grid(row=0, column=0, padx=(0,5), pady=5, sticky="e")
        self.algo_var = tk.StringVar(value=algos[0])
        ttk.Combobox(controles, textvariable=self.algo_var, values=algos, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Tamaño de píxel (k entero para PhotoImage.zoom)
        ttk.Label(controles, text="Tamaño píxel:").grid(row=1, column=0, padx=(0,5), pady=5, sticky="e")
        self.pixel_size_var = tk.IntVar(value=8)  # k
        ttk.Spinbox(controles, from_=1, to=40, increment=1, textvariable=self.pixel_size_var, width=6, command=self.on_pixel_size_change).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(controles, text="Limpiar", command=self.clear).grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(controles, text="Coordenadas", command=self.show_coords).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        #Boton para tener la lista de puntos
        ttk.Button(controles, text="Lista de Puntos", command=self.show_points).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        #Modo para chekear a mano los 3 algoritmos
        ttk.Label(controles, text="Modo Manual:").grid(row=7, column=0, padx=(0,5), pady=5, sticky="e")
        
        
        # Frame para organizar los dos recuadros de entrada
        frame_coordenadas = ttk.Frame(controles)
        frame_coordenadas.grid(row=8, column=0, columnspan=2, pady=5) 

        # Primer recuadro: Punto inicial
        ttk.Label(frame_coordenadas, text="Inicio (x1,y1):").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.entry_x1 = ttk.Entry(frame_coordenadas, width=7)
        self.entry_x1.grid(row=0, column=1, padx=2)
        ttk.Label(frame_coordenadas, text=",").grid(row=0, column=2)
        self.entry_y1 = ttk.Entry(frame_coordenadas, width=7)
        self.entry_y1.grid(row=0, column=3, padx=2)

        # Segundo recuadro: Punto final
        ttk.Label(frame_coordenadas, text="Fin (x2,y2):").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.entry_x2 = ttk.Entry(frame_coordenadas, width=7)
        self.entry_x2.grid(row=1, column=1, padx=2)
        ttk.Label(frame_coordenadas, text=",").grid(row=1, column=2)
        self.entry_y2 = ttk.Entry(frame_coordenadas, width=7)
        self.entry_y2.grid(row=1, column=3, padx=2)

        # Botón "Dibujar"
        btn_dibujar_manual = ttk.Button(controles, text="Dibujar", 
                                        command=self.dibujar_manual,
                                        width=20)
        btn_dibujar_manual.grid(row=10, column=0, columnspan=2, pady=10)  








        # Info
        self.info = tk.Text(self, height=10, width=100)
        self.info.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.info.insert("end", "1) Clic: punto inicial\n2) Clic: punto final\n")







        # Framebuffer lógico (imagen) + ejes
        self.img = None
        self.img_zoom = None
        self.img_id = None
        self._rebuild_framebuffer()
        self.draw_axes()

        # Eventos de ratón
        self.canvas.bind("<Button-1>", self.on_click)
        self.grid()

    # Conversión pantalla <-> cuadrícula lógica (origen en centro, y hacia arriba)
    def screen_to_grid(self, sx, sy):
        k = self.pixel_size_var.get()
        gx = round(sx / k) - self.grid_w // 2
        gy = self.grid_h // 2 - round(sy / k)
        return gx, gy

    def grid_to_screen(self, gx, gy):
        k = self.pixel_size_var.get()
        sx = self.center_x + gx * k
        sy = self.center_y - gy * k
        return sx, sy

    # Framebuffer lógico con PhotoImage y versión ampliada con zoom(k)
    def _rebuild_framebuffer(self):
        k = self.pixel_size_var.get()
        self.grid_w = max(1, self.canvas_size // k)
        self.grid_h = max(1, self.canvas_size // k)
        self.img = tk.PhotoImage(width=self.grid_w, height=self.grid_h)
        self.img_zoom = self.img.zoom(k)  # escala entera k×k
        if self.img_id is None:
            self.img_id = self.canvas.create_image(0, 0, image=self.img_zoom, anchor="nw")
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_zoom)
        self.canvas.tag_lower(self.img_id)

    def _refresh_image(self):
        k = self.pixel_size_var.get()
        self.img_zoom = self.img.zoom(k)  # vuelve a aplicar zoom con k actual
        self.canvas.itemconfig(self.img_id, image=self.img_zoom)

    def _put_pixel(self, gx, gy, color="#0000ff"):
        ix = gx + self.grid_w // 2
        iy = self.grid_h // 2 - gy
        if 0 <= ix < self.grid_w and 0 <= iy < self.grid_h:
            self.img.put(color, (ix, iy))

    def on_pixel_size_change(self):
        self._rebuild_framebuffer()
        self.canvas.delete("axes")
        self.draw_axes()

    def clear(self):
        self.start = self.end = None
        self.last_start = self.last_end = None
        self.info.delete("1.0", "end")
        self._rebuild_framebuffer()
        self.canvas.delete("axes")
        self.draw_axes()
        self.info.insert("end", "Canvas limpio. Empieza de nuevo.\n")

    def on_click(self, event):
        gx, gy = self.screen_to_grid(event.x, event.y)
        if self.start is None:
            self.start = (gx, gy)
            sx, sy = self.grid_to_screen(gx, gy)
            #self.canvas.create_oval(sx-3, sy-3, sx+3, sy+3, fill="green")
            self.info.insert("end", f"Inicio: {self.start}\n")
        else:
            self.end = (gx, gy)
            sx, sy = self.grid_to_screen(gx, gy)
            #self.canvas.create_oval(sx-3, sy-3, sx+3, sy+3, fill="red")
            self.info.insert("end", f"Fin: {self.end}\n")
            algo = self.algo_var.get()
            self.points = self.draw_callback(self.start, self.end, algo)  # puntos en coords lógicas
            for px, py in self.points:
                self._put_pixel(px, py, color="#0000ff")
            self._refresh_image()
            self.info.insert("end", f"{algo}: {len(self.points)} puntos\n\n")
            self.last_start, self.last_end = self.start, self.end
            self.start = self.end = None

    def show_coords(self):
        if self.start is not None and self.end is None:
            msg = f"Inicio: {self.start}\nFin: None"
        elif self.last_start is not None and self.last_end is not None:
            msg = f"Inicio: {self.last_start}\nFin: {self.last_end}"
        else:
            msg = "Inicio: None\nFin: None"
        messagebox.showinfo("Coordenadas actuales", msg)

    def draw_axes(self):
        self.canvas.delete("axes")
        # Ejes en pantalla (se superponen a la imagen)
        self.canvas.create_line(0, self.center_y, self.width, self.center_y, fill="gray", width=1, tags="axes")
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height, fill="gray", width=1, tags="axes")
        self.canvas.tag_raise("axes")

    def show_points(self):
        if self.last_start is not None and self.last_end is not None: #BORRAR: Aqui pondre la linea, en el resto no estaria terminada o sería inexistente por tanto solo un enaje de qu eno esta
            msg = ""
            for i in range (len(self.points)):
                msg += f"{self.points[i]}\n" 
           
        else:
            msg = "No tenemos ninguna linea guardada"
        messagebox.showinfo("Coordenadas de la última línea\n", msg)



    def dibujar_manual(self):
        """Dibuja línea con coordenadas introducidas manualmente"""
        try:
            # Obtener valores de los Entry
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
            
            # Dibujar (igual que on_click) - USAR TUPLAS
            self.start = (x1, y1)
            self.end = (x2, y2)
            algo = self.algo_var.get()
            
            # ← CAMBIO: Pasar tuplas, no coordenadas individuales
            self.points = self.draw_callback(self.start, self.end, algo)
            
            for px, py in self.points:
                self._put_pixel(px, py, color="#0000ff")
            self._refresh_image()
            
            self.info.insert("end", f"Manual - Inicio: {self.start}, Fin: {self.end}\n")
            self.info.insert("end", f"{algo}: {len(self.points)} puntos\n\n")
            
            self.last_start, self.last_end = self.start, self.end
            self.start = self.end = None
            
            # Limpiar campos después de dibujar
            self.entry_x1.delete(0, 'end')
            self.entry_y1.delete(0, 'end')
            self.entry_x2.delete(0, 'end')
            self.entry_y2.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error", "Introduce números enteros válidos")