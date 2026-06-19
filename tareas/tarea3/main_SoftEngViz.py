"""
Software Engineering Visualization Tool
SP Innovación — Replicación exacta de la imagen de referencia
+ automatización con IA (Claude API)

Pestañas: Desarrollo y Operaciones | Gráfico de Gantt | Aspectos
Panel izq: campos editables + botones
Panel der: diagrama circular con flechas curvas animadas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import math, threading, json, urllib.request, urllib.error
import datetime, os

# ──────────────────────────────────────────
#  PALETA — fiel a la imagen de referencia
# ──────────────────────────────────────────
BG        = "#F0F0F0"   # fondo general (gris Windows clásico)
SURFACE   = "#FFFFFF"
PANEL_BG  = "#ECECEC"
BTN_BG    = "#D4D0C8"   # botón Windows clásico
BTN_FG    = "#000000"
NODE_FILL = "#8FA8C8"   # azul-gris suave de los nodos
NODE_BRD  = "#3A5A8A"   # borde azul oscuro
ARROW_CLR = "#6B6B8A"   # gris azulado para flechas
TEXT_CLR  = "#000000"
MENU_BG   = "#D4D0C8"
MENU_SEL  = "#FFFFFF"
STATUS_BG = "#D4D0C8"

F_NORM  = ("Tahoma", 9)
F_BOLD  = ("Tahoma", 9, "bold")
F_HEAD  = ("Tahoma", 11, "bold")
F_MONO  = ("Courier New", 9)
F_TITLE = ("Tahoma", 10, "bold")

API_KEY = ""   # se ingresa en pestaña Aspectos

# ──────────────────────────────────────────
#  CLAUDE API
# ──────────────────────────────────────────
def call_claude(system: str, user: str, max_tokens: int = 1200) -> str:
    if not API_KEY:
        return "⚠  Por favor ingresa tu API Key de Anthropic en la pestaña Aspectos → API."
    try:
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"Error HTTP {e.code}: {e.read().decode()}"
    except Exception as ex:
        return f"Error: {ex}"


def run_in_thread(fn, *args):
    threading.Thread(target=fn, args=args, daemon=True).start()


# ──────────────────────────────────────────
#  VENTANA PRINCIPAL
# ──────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software Engineering Visualization Tool")
        self.geometry("1100x660")
        self.minsize(900, 540)
        self.configure(bg=BG)
        self._style()
        self._build_menu_bar()
        self._build_tabs()

    # ── ttk style ──
    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        # Notebook como barra de menú clásica
        s.configure("Menu.TNotebook",
                    background=MENU_BG, borderwidth=0, tabmargins=[2, 2, 2, 0])
        s.configure("Menu.TNotebook.Tab",
                    background=MENU_BG, foreground=TEXT_CLR,
                    padding=[12, 4], font=F_NORM, relief="flat")
        s.map("Menu.TNotebook.Tab",
              background=[("selected", SURFACE)],
              foreground=[("selected", "#000080")])
        # Inner notebooks
        s.configure("Inner.TNotebook",
                    background=BG, borderwidth=1, relief="sunken")
        s.configure("Inner.TNotebook.Tab",
                    background=PANEL_BG, foreground=TEXT_CLR,
                    padding=[10, 3], font=F_NORM)
        s.map("Inner.TNotebook.Tab",
              background=[("selected", SURFACE)])
        s.configure("TEntry", fieldbackground=SURFACE)
        s.configure("TCombobox", fieldbackground=SURFACE)

    # ── Barra de título separada (como en la ref) ──
    def _build_menu_bar(self):
        self.nb = ttk.Notebook(self, style="Menu.TNotebook")
        self.nb.pack(fill="both", expand=True)

    # ── Pestañas ──
    def _build_tabs(self):
        self.tab_dev   = tk.Frame(self.nb, bg=BG)
        self.tab_gantt = tk.Frame(self.nb, bg=BG)
        self.tab_asp   = tk.Frame(self.nb, bg=BG)

        self.nb.add(self.tab_dev,   text="Desarrollo y Operaciones")
        self.nb.add(self.tab_gantt, text="Grafico de Gantt")
        self.nb.add(self.tab_asp,   text="Aspectos")

        self._build_dev()
        self._build_gantt()
        self._build_asp()


# ══════════════════════════════════════════════════════
#  TAB 1 — DESARROLLO Y OPERACIONES
#  Replicación exacta de la imagen de referencia
# ══════════════════════════════════════════════════════
    def _build_dev(self):
        parent = self.tab_dev

        # ── Panel izquierdo (ancho fijo ~290px) ──
        left = tk.Frame(parent, bg=BG, width=290, relief="flat")
        left.pack(side="left", fill="y", padx=(6, 0), pady=6)
        left.pack_propagate(False)

        # Campos editables — exactos a la imagen
        FIELDS = [
            ("Titulo",       "Lift Track"),
            ("Codigo",       "JavaScript / React"),
            ("Construccion", "Frontend/Backend folders"),
            ("Pruebas",      "30+ Unit Tests"),
            ("Liberar",      "Release May 2026"),
            ("Desplegar",    "Cloud Deployment"),
            ("Operar",       "Infrastructure Maint."),
            ("Monitorear",   "User Monitoring"),
        ]
        self.fvars = {}
        fields_outer = tk.Frame(left, bg=BG, relief="sunken", bd=1)
        fields_outer.pack(fill="x", pady=(4, 2))
        for label, default in FIELDS:
            row = tk.Frame(fields_outer, bg=BG)
            row.pack(fill="x")
            tk.Label(row, text=label, font=F_NORM, bg=BG,
                     fg=TEXT_CLR, width=13, anchor="w",
                     padx=4, pady=2).pack(side="left")
            v = tk.StringVar(value=default)
            self.fvars[label] = v
            e = tk.Entry(row, textvariable=v, font=F_NORM,
                         relief="sunken", bd=1, width=22)
            e.pack(side="left", fill="x", expand=True, padx=(0, 4), pady=1)
            # redibujar al escribir
            v.trace_add("write", lambda *a: self._draw_cycle())

        # ── Separador ──
        tk.Frame(left, bg="#A0A0A0", height=1).pack(fill="x", pady=4)

        # ── Botones (mínimo 3, con estilo Windows clásico) ──
        BTN_W = 18
        self._classic_btn(left, "Generate Cycle",   self._on_generate,  BTN_W)
        self._classic_btn(left, "Save as PNG",      self._on_save_png,  BTN_W)
        self._classic_btn(left, "Analyze with AI",  self._on_analyze_ai, BTN_W)
        self._classic_btn(left, "Reset Fields",     self._on_reset,     BTN_W)
        self._classic_btn(left, "Export Report",    self._on_export,    BTN_W)

        # ── Panel derecho — Canvas ──
        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        self.canvas = tk.Canvas(right, bg=BG,
                                 highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_cycle())

        # ── Barra de estado ──
        self.status_var = tk.StringVar(value="Listo")
        st = tk.Label(parent, textvariable=self.status_var,
                      font=F_NORM, bg=STATUS_BG, fg=TEXT_CLR,
                      relief="sunken", bd=1, anchor="w", padx=8)
        st.pack(side="bottom", fill="x")

    def _classic_btn(self, parent, text, cmd, width=16):
        """Botón estilo Windows clásico — exacto como en la imagen."""
        b = tk.Button(parent, text=text, command=cmd,
                      font=F_NORM, bg=BTN_BG, fg=BTN_FG,
                      relief="raised", bd=2, cursor="hand2",
                      width=width, pady=3,
                      activebackground="#C0C0C0")
        b.pack(pady=3, padx=6, anchor="w")
        return b

    # ── Dibujar el diagrama circular ──
    def _draw_cycle(self):
        cv   = self.canvas
        cv.delete("all")
        W    = cv.winfo_width()
        H    = cv.winfo_height()
        if W < 20 or H < 20:
            return

        # Orden de nodos como en la imagen (horario desde arriba-derecha):
        # User Monitoring (arriba-centro), Lift Track (arriba-der),
        # JavaScript/React (der), Frontend/Backend (abajo-der),
        # 30+ Unit Tests (abajo-centro), Release May 2026 (abajo-izq),
        # Cloud Deployment (izq), Infrastructure Maint. (arriba-izq)
        order = ["Monitorear","Titulo","Codigo","Construccion",
                 "Pruebas","Liberar","Desplegar","Operar"]
        labels = [self.fvars[k].get() for k in order]

        n    = len(labels)
        cx   = W / 2
        cy   = H / 2
        R    = min(W, H) * 0.37   # radio del círculo
        NW   = 140                 # ancho nodo
        NH   = 52                  # alto nodo
        RX   = 10                  # radio esquinas

        # Fondo sutil
        cv.create_oval(cx - R - 10, cy - R - 10,
                       cx + R + 10, cy + R + 10,
                       outline="#C0C0C8", dash=(4, 8), width=1)

        # Calcular posiciones
        pos = []
        for i in range(n):
            # -90° = arriba; sentido horario
            a = math.radians(-90 + i * 360 / n)
            x = cx + R * math.cos(a)
            y = cy + R * math.sin(a)
            pos.append((x, y))

        # ── Flechas curvas entre nodos ──
        for i in range(n):
            x1, y1 = pos[i]
            x2, y2 = pos[(i + 1) % n]
            dx, dy = x2 - x1, y2 - y1
            dist   = math.hypot(dx, dy)
            if dist < 1:
                continue
            ux, uy = dx / dist, dy / dist

            # acortar para no entrar en los nodos
            pad = NH * 0.55
            sx  = x1 + ux * pad;  sy = y1 + uy * pad
            ex  = x2 - ux * pad;  ey = y2 - uy * pad

            # punto de control: curvado suavemente hacia el interior del círculo
            mx  = (sx + ex) / 2
            my  = (sy + ey) / 2
            # vector hacia el centro
            to_cx = cx - mx;  to_cy = cy - my
            to_c  = math.hypot(to_cx, to_cy)
            if to_c > 0:
                factor = R * 0.18
                mx += (to_cx / to_c) * factor
                my += (to_cy / to_c) * factor

            # Flecha
            cv.create_line(sx, sy, mx, my, ex, ey,
                           smooth=True, arrow="last",
                           arrowshape=(10, 14, 4),
                           fill=ARROW_CLR, width=2,
                           capstyle="round")

        # ── Nodos ──
        for i, (x, y) in enumerate(pos):
            x0, y0 = x - NW / 2, y - NH / 2
            x1, y1 = x + NW / 2, y + NH / 2

            # Sombra
            cv.create_rectangle(x0 + 4, y0 + 4, x1 + 4, y1 + 4,
                                 fill="#B0B8C8", outline="",
                                 width=0)
            # Cuerpo del nodo — estilo exacto a la imagen
            cv.create_rectangle(x0, y0, x1, y1,
                                 fill=NODE_FILL,
                                 outline=NODE_BRD,
                                 width=2)
            # Texto (partido en líneas si es largo)
            lbl = labels[i]
            cv.create_text(x, y, text=lbl,
                           font=("Tahoma", 9, "bold"),
                           fill=TEXT_CLR,
                           width=NW - 10,
                           justify="center")

    # ── Handlers de botones ──
    def _on_generate(self):
        self._draw_cycle()
        self.status_var.set("✓  Diagrama generado")

    def _on_save_png(self):
        """Guarda el canvas como PostScript (convertible a PNG con Pillow)."""
        path = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps"), ("All", "*.*")],
            initialfile="ciclo_devops.ps")
        if not path:
            return
        try:
            self.canvas.postscript(file=path, colormode="color")
            # Intentar convertir a PNG con Pillow si está disponible
            try:
                from PIL import Image
                png = path.replace(".ps", ".png")
                img = Image.open(path)
                img.save(png)
                os.remove(path)
                messagebox.showinfo("Guardado",
                    f"Diagrama guardado como PNG:\n{png}")
                self.status_var.set(f"✓  Guardado: {os.path.basename(png)}")
            except ImportError:
                messagebox.showinfo("Guardado como PostScript",
                    f"Guardado:\n{path}\n\n(Instala Pillow para exportar PNG directo)")
                self.status_var.set("✓  Guardado como .ps")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _on_analyze_ai(self):
        """Abre ventana nueva con análisis IA del ciclo."""
        data = {k: v.get() for k, v in self.fvars.items()}
        system = (
            "Eres un arquitecto de software sénior experto en DevOps y ciclos de vida "
            "de desarrollo de software. Analiza el ciclo de vida del proyecto proporcionado. "
            "Responde en español con las siguientes secciones claramente separadas:\n"
            "1️⃣  EVALUACIÓN DE FASES — evalúa cada etapa del ciclo\n"
            "2️⃣  RIESGOS DETECTADOS — lista los principales riesgos técnicos y operativos\n"
            "3️⃣  RECOMENDACIONES — mejoras concretas por fase\n"
            "4️⃣  ESTIMACIÓN DE TIEMPO — tiempo total estimado justificado\n"
            "5️⃣  PUNTUACIÓN DEL PROYECTO — del 1 al 10 con justificación\n"
            "Sé profesional, directo y estructurado. Máximo 500 palabras."
        )
        user = "Datos del proyecto:\n" + json.dumps(data, ensure_ascii=False, indent=2)
        self._open_ai_window("🤖  Análisis IA — Ciclo DevOps", system, user)

    def _on_reset(self):
        defaults = {
            "Titulo":       "Lift Track",
            "Codigo":       "JavaScript / React",
            "Construccion": "Frontend/Backend folders",
            "Pruebas":      "30+ Unit Tests",
            "Liberar":      "Release May 2026",
            "Desplegar":    "Cloud Deployment",
            "Operar":       "Infrastructure Maint.",
            "Monitorear":   "User Monitoring",
        }
        for k, v in defaults.items():
            self.fvars[k].set(v)
        self._draw_cycle()
        self.status_var.set("↺  Campos restaurados")

    def _on_export(self):
        """Genera un reporte completo del proyecto en TXT."""
        data = {k: v.get() for k, v in self.fvars.items()}
        system = (
            "Eres un consultor de proyectos de software. Genera un reporte ejecutivo "
            "profesional en español para el proyecto dado. Incluye: resumen ejecutivo, "
            "descripción de cada fase del ciclo de vida, equipo recomendado, "
            "tecnologías utilizadas, plan de acción inmediato, y conclusiones. "
            "Formato estructurado, listo para presentar a un cliente."
        )
        user = json.dumps(data, ensure_ascii=False, indent=2)
        self.status_var.set("⏳  Generando reporte con IA…")
        self._open_ai_window("📄  Reporte Ejecutivo del Proyecto", system, user,
                              export_btn=True)


# ══════════════════════════════════════════════════════
#  TAB 2 — GRÁFICO DE GANTT
# ══════════════════════════════════════════════════════
    def _build_gantt(self):
        parent = self.tab_gantt

        # Panel izquierdo
        left = tk.Frame(parent, bg=BG, width=290, relief="flat")
        left.pack(side="left", fill="y", padx=(6, 0), pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="Fases del Proyecto",
                 font=F_BOLD, bg=BG).pack(anchor="w", padx=6, pady=(6, 4))

        # Filas de tareas
        self.gantt_tasks = []
        defaults_g = [
            ("Planificación",  2),
            ("Análisis",       3),
            ("Diseño",         2),
            ("Desarrollo",     8),
            ("Pruebas",        3),
            ("Despliegue",     1),
            ("Monitoreo",      4),
        ]
        hdr = tk.Frame(left, bg=MENU_BG, relief="sunken", bd=1)
        hdr.pack(fill="x", padx=6)
        tk.Label(hdr, text="Fase", font=F_BOLD, bg=MENU_BG, width=14, anchor="w").pack(side="left")
        tk.Label(hdr, text="Sem.", font=F_BOLD, bg=MENU_BG, width=5).pack(side="left")

        rows_frame = tk.Frame(left, bg=BG, relief="sunken", bd=1)
        rows_frame.pack(fill="x", padx=6)
        for task, dur in defaults_g:
            r   = tk.Frame(rows_frame, bg=BG)
            r.pack(fill="x", pady=1)
            tv  = tk.StringVar(value=task)
            dv  = tk.StringVar(value=str(dur))
            tk.Entry(r, textvariable=tv, font=F_NORM, width=14,
                     relief="sunken", bd=1).pack(side="left", padx=2)
            tk.Entry(r, textvariable=dv, font=F_NORM, width=5,
                     relief="sunken", bd=1).pack(side="left", padx=2)
            self.gantt_tasks.append((tv, dv))

        tk.Frame(left, bg="#A0A0A0", height=1).pack(fill="x", padx=6, pady=6)

        self._classic_btn(left, "Generate Gantt",   self._on_gantt_draw)
        self._classic_btn(left, "Analyze Gantt AI", self._on_gantt_ai)
        self._classic_btn(left, "Add Task",         self._on_gantt_add)
        self._classic_btn(left, "Export Gantt",     self._on_gantt_export)

        # Canvas Gantt
        right = tk.Frame(parent, bg=SURFACE, relief="sunken", bd=1)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self.gantt_cv = tk.Canvas(right, bg=SURFACE, highlightthickness=0)
        self.gantt_cv.pack(fill="both", expand=True)
        self.gantt_cv.bind("<Configure>", lambda e: self._draw_gantt())

    def _draw_gantt(self):
        cv  = self.gantt_cv
        cv.delete("all")
        W   = cv.winfo_width()
        H   = cv.winfo_height()
        if W < 20 or H < 20:
            return
        tasks  = self.gantt_tasks
        n      = len(tasks)
        lbl_w  = 140
        bar_w  = W - lbl_w - 20
        row_h  = max(28, min(44, (H - 60) // max(n, 1)))
        COLORS = ["#4A6FA5","#5B7FC4","#6B8FD8","#7A9FE0",
                  "#8AAFE8","#9ABFF0","#3A5A8A"]
        try:
            durations = [max(1, int(dv.get())) for _, dv in tasks]
        except ValueError:
            durations = [1] * n
        max_dur = max(durations)

        # Encabezado
        cv.create_rectangle(0, 0, W, 36, fill="#4A5FC1", outline="")
        cv.create_text(lbl_w / 2, 18, text="Fase",
                       font=("Tahoma", 9, "bold"), fill="white")
        cv.create_text(lbl_w + bar_w / 2, 18,
                       text="Cronograma (semanas)",
                       font=("Tahoma", 9, "bold"), fill="white")

        for i, ((tv, _), dur) in enumerate(zip(tasks, durations)):
            y0 = 38 + i * row_h
            y1 = y0 + row_h - 2
            # Fondo alternado
            bg = SURFACE if i % 2 == 0 else "#F0F4FA"
            cv.create_rectangle(0, y0, W, y1, fill=bg, outline="#D8DCE8")
            # Etiqueta
            cv.create_text(8, (y0 + y1) / 2, text=tv.get(),
                           font=F_NORM, fill=TEXT_CLR, anchor="w")
            # Barra
            bw = int(bar_w * dur / max_dur)
            bx0 = lbl_w
            bx1 = bx0 + bw
            bh  = row_h - 8
            by0 = y0 + 4
            by1 = by0 + bh
            col = COLORS[i % len(COLORS)]
            cv.create_rectangle(bx0, by0, bx1, by1,
                                 fill=col, outline="", width=0)
            if bw > 40:
                cv.create_text((bx0 + bx1) / 2, (by0 + by1) / 2,
                                text=f"{dur} sem",
                                font=("Tahoma", 8, "bold"), fill="white")
        # Escala
        for t in range(0, max_dur + 1, max(1, max_dur // 8)):
            x = lbl_w + int(bar_w * t / max_dur)
            cv.create_line(x, 36, x, H, fill="#E0E4F0", dash=(3, 5))
            cv.create_text(x, H - 8, text=str(t),
                           font=("Tahoma", 8), fill="#606080")

    def _on_gantt_draw(self):
        self._draw_gantt()

    def _on_gantt_ai(self):
        try:
            tasks_data = [{"tarea": tv.get(), "semanas": int(dv.get())}
                          for tv, dv in self.gantt_tasks]
        except ValueError:
            tasks_data = [{"tarea": tv.get(), "semanas": dv.get()}
                          for tv, dv in self.gantt_tasks]
        system = (
            "Eres un experto en gestión de proyectos y metodologías ágiles. "
            "Analiza el cronograma Gantt proporcionado en español y responde con:\n"
            "📌 EVALUACIÓN DEL CRONOGRAMA — ¿es realista y equilibrado?\n"
            "⚠  CUELLOS DE BOTELLA — fases con mayor riesgo de retraso\n"
            "🔄 RUTA CRÍTICA — identifica las tareas que no pueden retrasarse\n"
            "💡 OPTIMIZACIONES — cómo reducir tiempos sin sacrificar calidad\n"
            "📋 RECOMENDACIÓN FINAL — ¿aprobarías este cronograma? ¿por qué?\n"
            "Sé concreto, técnico y útil. Máximo 400 palabras."
        )
        user = "Cronograma:\n" + json.dumps(tasks_data, ensure_ascii=False, indent=2)
        self._open_ai_window("📊  Análisis IA — Gráfico de Gantt", system, user)

    def _on_gantt_add(self):
        """Añade una fila extra a las tareas del Gantt."""
        win = tk.Toplevel(self)
        win.title("Agregar Tarea")
        win.geometry("320x150")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.grab_set()
        tk.Label(win, text="Nombre de la tarea:", font=F_NORM, bg=BG).pack(anchor="w", padx=12, pady=(12,2))
        tv = tk.StringVar()
        tk.Entry(win, textvariable=tv, font=F_NORM, relief="sunken", bd=1, width=36).pack(padx=12)
        tk.Label(win, text="Duración (semanas):", font=F_NORM, bg=BG).pack(anchor="w", padx=12, pady=(8,2))
        dv = tk.StringVar(value="2")
        tk.Entry(win, textvariable=dv, font=F_NORM, relief="sunken", bd=1, width=10).pack(anchor="w", padx=12)
        def confirm():
            if tv.get().strip():
                self.gantt_tasks.append((tk.StringVar(value=tv.get()),
                                         tk.StringVar(value=dv.get())))
                # rebuildear la vista (simplificado)
                win.destroy()
                self._draw_gantt()
        tk.Button(win, text="Agregar", command=confirm, font=F_NORM,
                  bg=BTN_BG, relief="raised", bd=2, pady=4).pack(pady=10)

    def _on_gantt_export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps"), ("All", "*.*")],
            initialfile="gantt.ps")
        if path:
            self.gantt_cv.postscript(file=path, colormode="color")
            messagebox.showinfo("Exportado", f"Gantt guardado:\n{path}")


# ══════════════════════════════════════════════════════
#  TAB 3 — ASPECTOS  (Sub-pestañas de IA)
# ══════════════════════════════════════════════════════
    def _build_asp(self):
        parent = self.tab_asp

        inner_nb = ttk.Notebook(parent, style="Inner.TNotebook")
        inner_nb.pack(fill="both", expand=True, padx=6, pady=6)

        t_doc  = tk.Frame(inner_nb, bg=BG)
        t_risk = tk.Frame(inner_nb, bg=BG)
        t_code = tk.Frame(inner_nb, bg=BG)
        t_api  = tk.Frame(inner_nb, bg=BG)

        inner_nb.add(t_doc,  text="  Documentación IA  ")
        inner_nb.add(t_risk, text="  Gestión de Riesgos  ")
        inner_nb.add(t_code, text="  Asistente de Código  ")
        inner_nb.add(t_api,  text="  Configuración API  ")

        self._build_doc(t_doc)
        self._build_risk(t_risk)
        self._build_code(t_code)
        self._build_api(t_api)

    # ── Sub: Documentación IA ──
    def _build_doc(self, parent):
        left = tk.Frame(parent, bg=BG, width=280)
        left.pack(side="left", fill="y", padx=(4, 0), pady=4)
        left.pack_propagate(False)

        tk.Label(left, text="Tipo de documento:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6, pady=(8,2))
        self.doc_tipo = ttk.Combobox(left, font=F_NORM, state="readonly",
            values=["Especificación de Requisitos (SRS)",
                    "Plan de Pruebas",
                    "Manual de Despliegue",
                    "Informe de Estado del Proyecto",
                    "Documento de Arquitectura",
                    "Acta de Reunión",
                    "Plan de Proyecto"])
        self.doc_tipo.set("Especificación de Requisitos (SRS)")
        self.doc_tipo.pack(fill="x", padx=6, pady=(0,8))

        tk.Label(left, text="Contexto / descripción:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6)
        self.doc_ctx = scrolledtext.ScrolledText(left, height=8, font=F_MONO,
                                                  bg=SURFACE, fg=TEXT_CLR,
                                                  relief="sunken", bd=1, wrap="word")
        self.doc_ctx.pack(fill="both", expand=True, padx=6, pady=4)
        self.doc_ctx.insert("end",
            "Proyecto: Lift Track\n"
            "Tecnología: JavaScript / React\n"
            "Fase actual: Construcción\n"
            "Equipo: 4 desarrolladores")

        tk.Frame(left, bg="#A0A0A0", height=1).pack(fill="x", padx=6, pady=4)
        self._classic_btn(left, "Generate Document", self._doc_generate)
        self._classic_btn(left, "Copy to Clipboard", self._doc_copy)
        self._classic_btn(left, "Save as .TXT",      self._doc_save)

        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.doc_result = scrolledtext.ScrolledText(right, font=F_MONO,
                                                     bg=SURFACE, fg=TEXT_CLR,
                                                     relief="sunken", bd=1, wrap="word",
                                                     padx=10, pady=10)
        self.doc_result.pack(fill="both", expand=True)
        self.doc_result.insert("end", "El documento generado aparecerá aquí…")
        self.doc_result.config(state="disabled")

    def _doc_generate(self):
        tipo = self.doc_tipo.get()
        ctx  = self.doc_ctx.get("1.0", "end").strip()
        system = (
            f"Eres un ingeniero de software sénior certificado. "
            f"Genera un documento técnico de tipo '{tipo}' completo, "
            "profesional y bien estructurado en español. "
            "Incluye todas las secciones estándar de la industria para este tipo de documento. "
            "El resultado debe ser listo para entregar a un cliente o equipo de desarrollo. "
            "Solo el documento, sin comentarios adicionales ni explicaciones fuera del mismo."
        )
        self._set_text(self.doc_result, "⏳  Generando documento con IA Claude…")
        run_in_thread(self._ia_to_widget, system, ctx, self.doc_result)

    def _doc_copy(self):
        txt = self.doc_result.get("1.0", "end").strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")

    def _doc_save(self):
        txt = self.doc_result.get("1.0", "end").strip()
        if not txt:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Texto", "*.txt")], initialfile="documento.txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            messagebox.showinfo("Guardado", f"Documento guardado:\n{path}")

    # ── Sub: Gestión de Riesgos ──
    def _build_risk(self, parent):
        left = tk.Frame(parent, bg=BG, width=280)
        left.pack(side="left", fill="y", padx=(4, 0), pady=4)
        left.pack_propagate(False)

        tk.Label(left, text="Área de análisis:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6, pady=(8,2))
        self.risk_area = ttk.Combobox(left, font=F_NORM, state="readonly",
            values=["Análisis Completo PMBOK",
                    "Riesgos Técnicos",
                    "Riesgos de Cronograma",
                    "Riesgos de Presupuesto",
                    "Riesgos de Seguridad",
                    "Riesgos de Equipo"])
        self.risk_area.set("Análisis Completo PMBOK")
        self.risk_area.pack(fill="x", padx=6, pady=(0,8))

        tk.Label(left, text="Contexto del proyecto:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6)
        self.risk_ctx = scrolledtext.ScrolledText(left, height=7, font=F_MONO,
                                                   bg=SURFACE, fg=TEXT_CLR,
                                                   relief="sunken", bd=1, wrap="word")
        self.risk_ctx.pack(fill="both", expand=True, padx=6, pady=4)
        self.risk_ctx.insert("end",
            "Proyecto: Lift Track\n"
            "Equipo: 4 desarrolladores, 1 PM\n"
            "Presupuesto: $80,000\n"
            "Plazo: 6 meses\n"
            "Tecnología: JavaScript/React")

        tk.Frame(left, bg="#A0A0A0", height=1).pack(fill="x", padx=6, pady=4)
        self._classic_btn(left, "Identify Risks",      self._risk_identify)
        self._classic_btn(left, "Mitigation Plan",     self._risk_mitigate)
        self._classic_btn(left, "Risk Matrix",         self._risk_matrix)
        self._classic_btn(left, "Save Risk Report",    self._risk_save)

        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.risk_result = scrolledtext.ScrolledText(right, font=F_MONO,
                                                      bg=SURFACE, fg=TEXT_CLR,
                                                      relief="sunken", bd=1, wrap="word",
                                                      padx=10, pady=10)
        self.risk_result.pack(fill="both", expand=True)
        self.risk_result.insert("end", "El análisis de riesgos aparecerá aquí…")
        self.risk_result.config(state="disabled")

    def _risk_identify(self):
        area = self.risk_area.get()
        ctx  = self.risk_ctx.get("1.0", "end").strip()
        system = (
            f"Eres un experto en gestión de riesgos de proyectos de software (PMBOK/PMI). "
            f"Realiza un '{area}' del proyecto dado. "
            "Para cada riesgo incluye:\n"
            "• ID del riesgo (R-001, R-002…)\n"
            "• Descripción detallada\n"
            "• Categoría (técnico / humano / financiero / externo)\n"
            "• Probabilidad: Alta / Media / Baja\n"
            "• Impacto: Alto / Medio / Bajo\n"
            "• Nivel de riesgo = Probabilidad × Impacto\n"
            "• Acción de respuesta recomendada\n"
            "Formato de tabla estructurada en español. Mínimo 6 riesgos."
        )
        self._set_text(self.risk_result, "⏳  Identificando riesgos con IA…")
        run_in_thread(self._ia_to_widget, system,
                      ctx, self.risk_result)

    def _risk_mitigate(self):
        ctx = self.risk_ctx.get("1.0", "end").strip()
        system = (
            "Eres un consultor sénior de gestión de proyectos (PMP). "
            "Crea un Plan de Mitigación de Riesgos detallado en español con:\n"
            "✅ ESTRATEGIAS PREVENTIVAS — acciones para evitar que ocurran\n"
            "🛡  PLANES DE CONTINGENCIA — qué hacer si ocurren\n"
            "👤 RESPONSABLES — quién lidera cada mitigación\n"
            "📅 CRONOGRAMA DE REVISIÓN — frecuencia de revisión de riesgos\n"
            "📊 KPIs DE RIESGO — indicadores a monitorear\n"
            "Formato estructurado, profesional, en español."
        )
        self._set_text(self.risk_result, "⏳  Generando plan de mitigación…")
        run_in_thread(self._ia_to_widget, system, ctx, self.risk_result)

    def _risk_matrix(self):
        ctx = self.risk_ctx.get("1.0", "end").strip()
        system = (
            "Eres un experto en gestión de riesgos. "
            "Genera una Matriz de Riesgos en formato texto para el proyecto dado. "
            "La matriz debe mostrar: filas = Impacto (Alto/Medio/Bajo), "
            "columnas = Probabilidad (Alta/Media/Baja), "
            "cada celda = color de riesgo (🔴 Alto, 🟡 Medio, 🟢 Bajo) "
            "y lista los riesgos del proyecto en cada celda. "
            "Incluye leyenda y recomendaciones por zona. Responde en español."
        )
        self._set_text(self.risk_result, "⏳  Generando matriz de riesgos…")
        run_in_thread(self._ia_to_widget, system, ctx, self.risk_result)

    def _risk_save(self):
        txt = self.risk_result.get("1.0", "end").strip()
        if not txt:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Texto", "*.txt")], initialfile="riesgos.txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            messagebox.showinfo("Guardado", f"Reporte de riesgos:\n{path}")

    # ── Sub: Asistente de Código ──
    def _build_code(self, parent):
        left = tk.Frame(parent, bg=BG, width=280)
        left.pack(side="left", fill="y", padx=(4, 0), pady=4)
        left.pack_propagate(False)

        tk.Label(left, text="Lenguaje:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6, pady=(8,2))
        self.code_lang = ttk.Combobox(left, font=F_NORM, state="readonly",
            values=["JavaScript / React", "Python", "TypeScript",
                    "SQL", "Bash / Shell", "HTML + CSS", "Java", "C#"])
        self.code_lang.set("JavaScript / React")
        self.code_lang.pack(fill="x", padx=6, pady=(0,8))

        tk.Label(left, text="Tarea / descripción:", font=F_BOLD, bg=BG).pack(anchor="w", padx=6)
        self.code_input = scrolledtext.ScrolledText(left, height=9, font=F_MONO,
                                                     bg=SURFACE, fg=TEXT_CLR,
                                                     relief="sunken", bd=1, wrap="word")
        self.code_input.pack(fill="both", expand=True, padx=6, pady=4)
        self.code_input.insert("end",
            "Crea un componente React que muestre\n"
            "una tabla de tareas con filtrado y paginación.")

        tk.Frame(left, bg="#A0A0A0", height=1).pack(fill="x", padx=6, pady=4)
        self._classic_btn(left, "Generate Code",  self._code_generate)
        self._classic_btn(left, "Debug / Fix",    self._code_debug)
        self._classic_btn(left, "Explain Code",   self._code_explain)
        self._classic_btn(left, "Copy Code",      self._code_copy)

        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.code_result = scrolledtext.ScrolledText(right, font=F_MONO,
                                                      bg="#1E1E2E", fg="#CDD6F4",
                                                      insertbackground="#89B4FA",
                                                      relief="sunken", bd=1, wrap="none",
                                                      padx=10, pady=10)
        self.code_result.pack(fill="both", expand=True)
        self.code_result.insert("end", "// El código generado aparecerá aquí…")
        self.code_result.config(state="disabled")

    def _code_generate(self):
        lang = self.code_lang.get()
        desc = self.code_input.get("1.0", "end").strip()
        system = (
            f"Eres un desarrollador sénior experto en {lang}. "
            "Genera código limpio, bien comentado, funcional y listo para producción. "
            "Incluye: código completo, comentarios en español en líneas clave, "
            "y al final una breve nota de uso. "
            "Solo el código y los comentarios necesarios, nada más."
        )
        self._set_text(self.code_result, "// ⏳  Generando código con IA…")
        run_in_thread(self._ia_to_widget, system, desc, self.code_result)

    def _code_debug(self):
        lang = self.code_lang.get()
        code = self.code_input.get("1.0", "end").strip()
        system = (
            f"Eres un debugger experto en {lang}. "
            "Analiza el código dado, identifica TODOS los errores y problemas, "
            "y devuelve la versión corregida y mejorada. "
            "Antes del código corregido incluye una sección '// CAMBIOS REALIZADOS:' "
            "listando qué se corrigió y por qué. En español."
        )
        self._set_text(self.code_result, "// ⏳  Analizando y corrigiendo código…")
        run_in_thread(self._ia_to_widget, system, code, self.code_result)

    def _code_explain(self):
        code = self.code_input.get("1.0", "end").strip()
        system = (
            "Eres un instructor de programación. "
            "Explica el siguiente código de manera clara y didáctica en español. "
            "Estructura: 1) Qué hace el código, 2) Cómo funciona línea por línea "
            "o bloque por bloque, 3) Conceptos clave utilizados, "
            "4) Posibles mejoras o alternativas."
        )
        self._set_text(self.code_result, "// ⏳  Explicando código con IA…")
        run_in_thread(self._ia_to_widget, system, code, self.code_result)

    def _code_copy(self):
        txt = self.code_result.get("1.0", "end").strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("Copiado", "Código copiado al portapapeles.")

    # ── Sub: Configuración API ──
    def _build_api(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True)

        card = tk.Frame(frame, bg=SURFACE, relief="raised", bd=2)
        card.place(relx=.5, rely=.5, anchor="center", width=500, height=340)

        tk.Label(card, text="⚙  Configuración de API — Anthropic Claude",
                 font=F_HEAD, bg=SURFACE, fg="#000080").pack(anchor="w", padx=20, pady=(20,4))
        tk.Frame(card, bg="#C0C0C0", height=1).pack(fill="x", padx=20)
        tk.Label(card, text="Obtén tu API Key en: console.anthropic.com",
                 font=F_NORM, bg=SURFACE, fg="#606060").pack(anchor="w", padx=20, pady=(8,16))

        tk.Label(card, text="API Key:", font=F_BOLD, bg=SURFACE).pack(anchor="w", padx=20)
        self.api_entry = tk.Entry(card, font=F_NORM, show="*",
                                   relief="sunken", bd=2, width=56)
        self.api_entry.pack(padx=20, pady=(4,4), ipady=5, fill="x")
        if API_KEY:
            self.api_entry.insert(0, API_KEY)

        show_v = tk.BooleanVar()
        tk.Checkbutton(card, text="Mostrar API Key", variable=show_v,
                       command=lambda: self.api_entry.config(show="" if show_v.get() else "*"),
                       font=F_NORM, bg=SURFACE, activebackground=SURFACE).pack(anchor="w", padx=20)

        btn_row = tk.Frame(card, bg=SURFACE)
        btn_row.pack(pady=16, padx=20, anchor="w")
        tk.Button(btn_row, text="  Guardar API Key",
                  command=self._api_save, font=F_NORM,
                  bg=BTN_BG, relief="raised", bd=2, pady=5, padx=10).pack(side="left", padx=(0,8))
        tk.Button(btn_row, text="  Probar Conexión",
                  command=self._api_test, font=F_NORM,
                  bg=BTN_BG, relief="raised", bd=2, pady=5, padx=10).pack(side="left")

        self.api_status = tk.Label(card, text="", font=F_NORM, bg=SURFACE)
        self.api_status.pack(anchor="w", padx=20)

        tk.Label(card,
                 text="La API Key se guarda solo en memoria (esta sesión).\n"
                      "No se almacena en disco por seguridad.",
                 font=("Tahoma", 8), bg=SURFACE, fg="#909090",
                 justify="left").pack(anchor="w", padx=20, pady=(8,0))

    def _api_save(self):
        global API_KEY
        API_KEY = self.api_entry.get().strip()
        self.api_status.config(text="✓  API Key guardada en esta sesión.", fg="#006400")

    def _api_test(self):
        global API_KEY
        API_KEY = self.api_entry.get().strip()
        self.api_status.config(text="⏳  Probando conexión…", fg="#8B6914")
        def worker():
            r = call_claude("Responde solo la palabra: CONECTADO", "test")
            ok = "CONECTADO" in r or "conectado" in r.lower()
            msg   = "✓  Conexión exitosa con Claude API!" if ok else f"✗  {r[:100]}"
            color = "#006400" if ok else "#8B0000"
            self.after(0, lambda: self.api_status.config(text=msg, fg=color))
        run_in_thread(worker)


# ══════════════════════════════════════════════════════
#  HELPERS GLOBALES
# ══════════════════════════════════════════════════════
    def _open_ai_window(self, title: str, system: str, user: str,
                         export_btn: bool = False):
        """Abre una ventana secundaria con resultado de IA."""
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("680x520")
        win.configure(bg=BG)

        # Barra superior
        hdr = tk.Frame(win, bg="#000080", height=30)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"  {title}", font=F_BOLD,
                 bg="#000080", fg="white").pack(side="left", fill="y")

        # Área de texto
        txt = scrolledtext.ScrolledText(win, font=F_MONO,
                                         bg=SURFACE, fg=TEXT_CLR,
                                         relief="sunken", bd=1, wrap="word",
                                         padx=12, pady=10)
        txt.pack(fill="both", expand=True, padx=8, pady=8)
        txt.insert("end", "⏳  Procesando con IA Claude, por favor espera…")
        txt.config(state="disabled")

        # Botones de la ventana secundaria
        btn_row = tk.Frame(win, bg=BG)
        btn_row.pack(fill="x", padx=8, pady=(0, 8))
        tk.Button(btn_row, text="Copiar texto", font=F_NORM,
                  bg=BTN_BG, relief="raised", bd=2, pady=4,
                  command=lambda: (self.clipboard_clear(),
                                   self.clipboard_append(txt.get("1.0", "end")))).pack(side="left", padx=(0,6))
        if export_btn:
            def save_txt():
                content = txt.get("1.0", "end").strip()
                path = filedialog.asksaveasfilename(
                    parent=win, defaultextension=".txt",
                    filetypes=[("Texto", "*.txt")],
                    initialfile="reporte.txt")
                if path:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    messagebox.showinfo("Guardado", f"Reporte:\n{path}")
            tk.Button(btn_row, text="Guardar .TXT", font=F_NORM,
                      bg=BTN_BG, relief="raised", bd=2, pady=4,
                      command=save_txt).pack(side="left", padx=(0,6))
        tk.Button(btn_row, text="Cerrar", font=F_NORM,
                  bg=BTN_BG, relief="raised", bd=2, pady=4,
                  command=win.destroy).pack(side="right")

        # Ejecutar IA en hilo
        def worker():
            r = call_claude(system, user, max_tokens=1400)
            def upd():
                txt.config(state="normal")
                txt.delete("1.0", "end")
                txt.insert("end", r)
                txt.config(state="disabled")
                self.status_var.set("✓  Análisis IA completado")
            win.after(0, upd)

        run_in_thread(worker)

    def _ia_to_widget(self, system: str, user: str, widget):
        r = call_claude(system, user, max_tokens=1400)
        self.after(0, lambda: self._set_text(widget, r))

    def _set_text(self, widget, text: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.config(state="disabled")


# ──────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
