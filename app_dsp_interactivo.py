"""
====================================================================================================
app_dsp_interactivo.py
APLICACIÓN INTUITIVA DE DSP: ADC - DAC, SEPARACIÓN DE INSTRUMENTOS/VOZ Y EFECTOS EN EL CEREBRO
====================================================================================================
Incluye:
  1. Menú intuitivo de carga de audio (examinar archivo WAV o seleccionar de la lista)
     y asignación del género musical.
  2. Separador de instrumentos (Bajos, Instrumentos melódicos, Percusión) y Voz principal
     mediante filtros digitales DSP y guardado en archivos WAV (stems).
  3. Módulo interactivo de DSP: Nyquist-Shannon, FFT, Cuantización ADC/DAC con control
     de bits en tiempo real (resolución LSB, factor de escala y SQNR).
  4. Evaluación Neuroacústica Cerebral: Diagnóstico de cómo afecta la música al cerebro
     (Contento, Triste, Concentrado, Hiperactivo, etc.), ondas cerebrales y análisis TDAH.
  5. Gráficas interactivas y visualización integrada.
====================================================================================================
"""

import os
import sys

# Asegurar codificación utf-8 en consola
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib
import matplotlib.pyplot as plt

# Tkinter imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Módulos del proyecto
from dsp_audio_analisis import INVESTIGACION_GENEROS, AudioDSPAnalyzer
from separador_audio import separar_pistas_audio
from evaluador_cerebro import evaluar_impacto_cerebral

# ==================================================================================================
# CLASE DE LA INTERFAZ GRÁFICA INTUITIVA (GUI)
# ==================================================================================================
class AppDSPInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Audio Lab: ADC/DAC, Separador de Instrumentos/Voz y Neuroacústica Cerebral")
        self.root.geometry("1200x820")
        self.root.minsize(1000, 700)
        
        # Estado actual
        self.ruta_actual = ""
        self.genero_actual = "Clásica - Barroca"
        self.analyzer_actual = None
        self.pistas_separadas = None
        self.impacto_cerebro = None
        
        # Asegurar carpetas necesarias
        os.makedirs("audios", exist_ok=True)
        os.makedirs("pistas_separadas", exist_ok=True)
        os.makedirs("graficas", exist_ok=True)
        
        # Configurar Estilos Visuales
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
            
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground="#1a365d")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10, "bold"), foreground="#2d3748")
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        
        self._construir_interfaz()
        
        # Cargar audio inicial por defecto si existe
        ruta_defecto = os.path.join("audios", "1_clasica_barroca.wav")
        if os.path.exists(ruta_defecto):
            self.ruta_actual = ruta_defecto
            self.combo_canciones.set("1_clasica_barroca.wav")
            self.combo_genero.set("Clásica - Barroca")
            self.cargar_y_analizar()

    def _construir_interfaz(self):
        # Contenedor Principal con Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestañas
        self.tab_carga = ttk.Frame(self.notebook)
        self.tab_separacion = ttk.Frame(self.notebook)
        self.tab_dsp = ttk.Frame(self.notebook)
        self.tab_cerebro = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_carga, text=" 1. Cargar Audio y Género ")
        self.notebook.add(self.tab_separacion, text=" 2. Separar Voz e Instrumentos ")
        self.notebook.add(self.tab_dsp, text=" 3. ADC - DAC y Nyquist-Shannon ")
        self.notebook.add(self.tab_cerebro, text=" 4. Efecto en el Cerebro (TDAH/Emociones) ")
        
        self._construir_tab_carga()
        self._construir_tab_separacion()
        self._construir_tab_dsp()
        self._construir_tab_cerebro()

    # ----------------------------------------------------------------------------------------------
    # 1. PESTAÑA: CARGA DE AUDIO Y SELECCIÓN DE GÉNERO
    # ----------------------------------------------------------------------------------------------
    def _construir_tab_carga(self):
        frame_top = ttk.LabelFrame(self.tab_carga, text=" Menú de Carga y Selección de Canción ", padding=15)
        frame_top.pack(fill="x", padx=15, pady=10)
        
        # Fila 1: Selección desde archivo personalizado
        lbl_file = ttk.Label(frame_top, text="Archivo WAV Personalizado:", style="SubHeader.TLabel")
        lbl_file.grid(row=0, column=0, sticky="w", pady=5)
        
        self.entry_ruta = ttk.Entry(frame_top, width=50, font=("Segoe UI", 9))
        self.entry_ruta.grid(row=0, column=1, padx=8, pady=5, sticky="ew")
        
        btn_browse = ttk.Button(frame_top, text="Examinar Archivo...", command=self.examinar_archivo)
        btn_browse.grid(row=0, column=2, padx=5, pady=5)
        
        # Fila 2: Canciones predefinidas
        lbl_preset = ttk.Label(frame_top, text="O Seleccionar de la Biblioteca:", style="SubHeader.TLabel")
        lbl_preset.grid(row=1, column=0, sticky="w", pady=5)
        
        canciones_disp = [f for f in os.listdir("audios") if f.endswith(".wav")]
        if not canciones_disp:
            canciones_disp = ["1_clasica_barroca.wav", "2_metal.wav", "3_salsa.wav", "4_cantina_al_hombro.wav", "5_reggaeton.wav"]
            
        self.combo_canciones = ttk.Combobox(frame_top, values=canciones_disp, state="readonly", width=48)
        self.combo_canciones.grid(row=1, column=1, padx=8, pady=5, sticky="w")
        self.combo_canciones.bind("<<ComboboxSelected>>", self._on_preset_seleccionado)
        
        # Fila 3: Selección de Género
        lbl_gen = ttk.Label(frame_top, text="Género Musical:", style="SubHeader.TLabel")
        lbl_gen.grid(row=2, column=0, sticky="w", pady=5)
        
        generos = ["Clásica - Barroca", "Metal", "Salsa", "Cantina al hombro", "Reggaeton", "Personalizado"]
        self.combo_genero = ttk.Combobox(frame_top, values=generos, state="readonly", width=30)
        self.combo_genero.set("Clásica - Barroca")
        self.combo_genero.grid(row=2, column=1, padx=8, pady=5, sticky="w")
        
        btn_cargar = ttk.Button(frame_top, text="▶ Cargar y Analizar Señal", command=self.cargar_y_analizar)
        btn_cargar.grid(row=2, column=2, padx=5, pady=5)
        
        # Área de Información de la Canción
        frame_info = ttk.LabelFrame(self.tab_carga, text=" Ficha Técnica y Breve Investigación del Músico/Obra ", padding=15)
        frame_info.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.txt_info = tk.Text(frame_info, wrap="word", font=("Consolas", 10), height=14)
        scroll_info = ttk.Scrollbar(frame_info, command=self.txt_info.yview)
        self.txt_info.configure(yscrollcommand=scroll_info.set)
        self.txt_info.pack(side="left", fill="both", expand=True)
        scroll_info.pack(side="right", fill="y")
        
        self.txt_info.insert("end", "Seleccione un archivo de audio y presione 'Cargar y Analizar Señal' para ver los detalles técnicos y teóricos.\n")
        self.txt_info.configure(state="disabled")

    def _on_preset_seleccionado(self, event=None):
        cancion = self.combo_canciones.get()
        ruta = os.path.join("audios", cancion)
        self.entry_ruta.delete(0, "end")
        self.entry_ruta.insert(0, ruta)
        
        # Auto-seleccionar género según el nombre
        c_low = cancion.lower()
        if "clasica" in c_low or "barroca" in c_low:
            self.combo_genero.set("Clásica - Barroca")
        elif "metal" in c_low:
            self.combo_genero.set("Metal")
        elif "salsa" in c_low:
            self.combo_genero.set("Salsa")
        elif "cantina" in c_low or "carrilera" in c_low:
            self.combo_genero.set("Cantina al hombro")
        elif "reggaeton" in c_low:
            self.combo_genero.set("Reggaeton")

    def examinar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar Archivo de Audio WAV",
            filetypes=[("Archivos WAV", "*.wav"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_ruta.delete(0, "end")
            self.entry_ruta.insert(0, archivo)

    def cargar_y_analizar(self):
        ruta = self.entry_ruta.get().strip()
        if not ruta:
            cancion = self.combo_canciones.get()
            if cancion:
                ruta = os.path.join("audios", cancion)
                
        if not os.path.exists(ruta):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}\n\nGenere primero los audios o seleccione un archivo WAV válido.")
            return
            
        self.ruta_actual = ruta
        self.genero_actual = self.combo_genero.get()
        
        # Mapear investigación histórica
        clave_gen = "clasica_barroca"
        g_low = self.genero_actual.lower()
        if "metal" in g_low:
            clave_gen = "metal"
        elif "salsa" in g_low:
            clave_gen = "salsa"
        elif "cantina" in g_low:
            clave_gen = "cantina_al_hombro"
        elif "reggaeton" in g_low:
            clave_gen = "reggaeton"
            
        info_investigacion = INVESTIGACION_GENEROS.get(clave_gen, {
            "genero": self.genero_actual,
            "obra": os.path.basename(ruta),
            "musico_compositor": "Músico / Artista Independiente",
            "tipo_agrupacion": "Banda / Orquesta / Producción Digital",
            "ano_obra": "Contemporáneo",
            "contexto_historico": "Audio personalizado cargado por el usuario.",
            "impacto_tdh": "Evaluado a partir del contenido de frecuencias y ritmo."
        })
        
        try:
            self.analyzer_actual = AudioDSPAnalyzer(ruta, info_investigacion, v_ref=1.0)
            self.impacto_cerebro = evaluar_impacto_cerebral(self.genero_actual)
            
            # Mostrar datos técnicos en pestaña 1
            fs, raw = self.analyzer_actual.fs, self.analyzer_actual.x_raw
            dur = self.analyzer_actual.duracion
            metricas = self.analyzer_actual.calcular_metricas_frecuencia()
            
            self.txt_info.configure(state="normal")
            self.txt_info.delete("1.0", "end")
            texto = (
                f"========================================================================================\n"
                f" REPORTE TÉCNICO Y FICHA HISTÓRICA DEL AUDIO CARGADO\n"
                f"========================================================================================\n"
                f" • Archivo de Audio       : {os.path.basename(ruta)}\n"
                f" • Ruta Completa          : {ruta}\n"
                f" • Género Musical         : {self.genero_actual}\n"
                f" • Obra Musical           : {info_investigacion.get('obra', 'N/A')} ({info_investigacion.get('ano_obra', 'N/A')})\n"
                f" • Compositor / Músico    : {info_investigacion.get('musico_compositor', 'N/A')}\n"
                f" • Agrupación             : {info_investigacion.get('tipo_agrupacion', 'N/A')}\n"
                f" • Contexto Histórico     : {info_investigacion.get('contexto_historico', 'N/A')}\n"
                f"----------------------------------------------------------------------------------------\n"
                f" PARÁMETROS DE SEÑAL Y DSP:\n"
                f" • Frecuencia de Muestreo (fs)      : {fs} Hz (Periodo de Muestreo Ts = {1.0/fs*1e6:.2f} µs)\n"
                f" • Frecuencia de Nyquist (fs/2)     : {self.analyzer_actual.f_nyquist} Hz\n"
                f" • Frecuencia Máxima Efectiva (fmax): {self.analyzer_actual.f_max_efectiva:.1f} Hz\n"
                f" • Teorema Nyquist-Shannon          : fs >= 2*fmax -> {fs} >= {2*self.analyzer_actual.f_max_efectiva:.1f} Hz (CUMPLE - Sin Aliasing)\n"
                f" • Duración Total de la Señal       : {dur:.2f} segundos ({len(raw)} muestras)\n"
                f" • Centroide Espectral              : {metricas['centroide_hz']:.1f} Hz\n"
                f" • Distribución Espectral           : Graves (20-250 Hz): {metricas['pct_graves']:.1f}% | "
                f"Medios (250-2000 Hz): {metricas['pct_medios']:.1f}% | Agudos (2-8 kHz): {metricas['pct_agudos']:.1f}%\n"
                f"========================================================================================\n"
            )
            self.txt_info.insert("end", texto)
            self.txt_info.configure(state="disabled")
            
            # Actualizar las demás pestañas automáticamente
            self._actualizar_tab_dsp()
            self._actualizar_tab_cerebro()
            messagebox.showinfo("Carga Exitosa", f"Se cargó y analizó correctamente el audio:\n{os.path.basename(ruta)}\n\nPuede explorar las pestañas de 'Separar Voz e Instrumentos', 'ADC - DAC' y 'Efecto en el Cerebro'.")
            
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"Ocurrió un error al procesar el archivo:\n{str(e)}")

    # ----------------------------------------------------------------------------------------------
    # 2. PESTAÑA: SEPARACIÓN DE INSTRUMENTOS Y VOZ
    # ----------------------------------------------------------------------------------------------
    def _construir_tab_separacion(self):
        frame_controles = ttk.LabelFrame(self.tab_separacion, text=" Opciones de Separación de Fuentes Musicales ", padding=10)
        frame_controles.pack(fill="x", padx=15, pady=8)
        
        lbl_desc = ttk.Label(frame_controles, text="Seleccione las pistas que desea aislar mediante filtrado digital IIR / DSP:", font=("Segoe UI", 9))
        lbl_desc.grid(row=0, column=0, columnspan=4, sticky="w", pady=4)
        
        self.var_voz = tk.BooleanVar(value=True)
        self.var_bajos = tk.BooleanVar(value=True)
        self.var_medios = tk.BooleanVar(value=True)
        self.var_agudos = tk.BooleanVar(value=True)
        
        chk_voz = ttk.Checkbutton(frame_controles, text="🎤 1. Voz Principal (300 - 3400 Hz)", variable=self.var_voz)
        chk_voz.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        chk_bajos = ttk.Checkbutton(frame_controles, text="🎸 2. Bajos y Bombos (20 - 260 Hz)", variable=self.var_bajos)
        chk_bajos.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        chk_medios = ttk.Checkbutton(frame_controles, text="🎹 3. Instrumentos Melódicos / Cuerdas (400 - 5500 Hz)", variable=self.var_medios)
        chk_medios.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        chk_agudos = ttk.Checkbutton(frame_controles, text="🥁 4. Percusión y Platillos (> 5000 Hz)", variable=self.var_agudos)
        chk_agudos.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        btn_separar = ttk.Button(frame_controles, text="⚡ Ejecutar Separación y Guardar Stems WAV", command=self.ejecutar_separacion)
        btn_separar.grid(row=2, column=0, columnspan=4, pady=8)
        
        self.lbl_estado_sep = ttk.Label(frame_controles, text="Estado: Listo para separar.", font=("Segoe UI", 9, "italic"), foreground="#4a5568")
        self.lbl_estado_sep.grid(row=3, column=0, columnspan=4, sticky="w")
        
        # Área para gráficas de las pistas separadas
        self.frame_graf_sep = ttk.Frame(self.tab_separacion)
        self.frame_graf_sep.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.fig_sep, self.axes_sep = plt.subplots(4, 1, figsize=(10, 6.5))
        self.fig_sep.subplots_adjust(hspace=0.45)
        for ax in self.axes_sep:
            ax.set_facecolor("#f7fafc")
            ax.grid(True, linestyle="--", alpha=0.5)
            
        self.canvas_sep = FigureCanvasTkAgg(self.fig_sep, master=self.frame_graf_sep)
        self.canvas_sep.get_tk_widget().pack(fill="both", expand=True)

    def ejecutar_separacion(self):
        if self.analyzer_actual is None:
            messagebox.showwarning("Atención", "Primero debe cargar un audio en la Pestaña 1.")
            return
            
        nombre_base = os.path.splitext(os.path.basename(self.ruta_actual))[0]
        self.lbl_estado_sep.config(text="Procesando separación con filtros Butterworth paso-banda...", foreground="#d69e2e")
        self.root.update_idletasks()
        
        # Llamar al separador de audio DSP
        fs, raw = wavfile.read(self.ruta_actual)
        self.pistas_separadas = separar_pistas_audio(raw, fs, carpeta_salida="pistas_separadas", prefijo=nombre_base)
        
        # Graficar las 4 pistas separadas
        titulos = [
            ("Línea de Bajos y Bombo (20 - 260 Hz)", "bajos_y_bombos", "#1f77b4"),
            ("Voz Principal / Formantes Vocales (300 - 3400 Hz)", "voz_principal", "#d62728"),
            ("Instrumentos Melódicos / Cuerdas (400 - 5500 Hz)", "instrumentos_medios", "#2ca02c"),
            ("Percusión de Agudos y Platillos (> 5000 Hz)", "percusion_y_agudos", "#9467bd")
        ]
        
        t_zoom_ms = 40.0
        n_zoom = int((t_zoom_ms / 1000.0) * fs)
        t_ms = (np.arange(n_zoom) / fs) * 1000.0
        
        for i, (titulo, clave, color) in enumerate(titulos):
            ax = self.axes_sep[i]
            ax.clear()
            datos_pista = self.pistas_separadas[clave]
            sig = datos_pista["senal"][:n_zoom]
            ax.plot(t_ms, sig, color=color, linewidth=1.4, label=f"{titulo} (Potencia: {datos_pista['potencia_relativa']:.2e})")
            ax.set_ylabel("Amplitud", fontsize=8)
            ax.set_title(titulo, fontsize=9, fontweight="bold", pad=2)
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(loc="upper right", fontsize=8)
            
        self.axes_sep[-1].set_xlabel("Tiempo (milisegundos)", fontsize=8)
        self.canvas_sep.draw()
        
        self.lbl_estado_sep.config(
            text=f"¡Separación Exitosa! 4 archivos WAV guardados en 'pistas_separadas/'.",
            foreground="#2f855a"
        )
        messagebox.showinfo("Separación Completa", f"Se han generado y guardado las 4 pistas WAV aisladas en la carpeta 'pistas_separadas/':\n\n1. {nombre_base}_voz_principal.wav\n2. {nombre_base}_bajos_y_bombos.wav\n3. {nombre_base}_instrumentos_medios.wav\n4. {nombre_base}_percusion_y_agudos.wav")

    # ----------------------------------------------------------------------------------------------
    # 3. PESTAÑA: ADC - DAC, NYQUIST-SHANNON Y CUANTIZACIÓN
    # ----------------------------------------------------------------------------------------------
    def _construir_tab_dsp(self):
        frame_controles_dsp = ttk.LabelFrame(self.tab_dsp, text=" Control Interactivo de Cuantización ADC - DAC ", padding=10)
        frame_controles_dsp.pack(fill="x", padx=15, pady=8)
        
        lbl_bits = ttk.Label(frame_controles_dsp, text="Resolución en Bits del ADC / DAC (B):", style="SubHeader.TLabel")
        lbl_bits.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.slider_bits = tk.Scale(frame_controles_dsp, from_=2, to=16, orient="horizontal", length=300, command=self._on_slider_bits_change)
        self.slider_bits.set(4)
        self.slider_bits.grid(row=0, column=1, padx=10, pady=5)
        
        self.lbl_metricas_q = ttk.Label(frame_controles_dsp, text="Niveles L: 16 | Resolución Δ (LSB): 133.33 mV | Factor Escala: 133.33 mV/bit | SQNR: 25.84 dB", font=("Consolas", 10, "bold"), foreground="#1a365d")
        self.lbl_metricas_q.grid(row=0, column=2, padx=15, pady=5, sticky="w")
        
        # Lienzo Matplotlib para gráficas DSP
        self.frame_graf_dsp = ttk.Frame(self.tab_dsp)
        self.frame_graf_dsp.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.fig_dsp, self.axes_dsp = plt.subplots(3, 1, figsize=(10, 6.8))
        self.fig_dsp.subplots_adjust(hspace=0.45)
        for ax in self.axes_dsp:
            ax.set_facecolor("#f7fafc")
            ax.grid(True, linestyle="--", alpha=0.5)
            
        self.canvas_dsp = FigureCanvasTkAgg(self.fig_dsp, master=self.frame_graf_dsp)
        self.canvas_dsp.get_tk_widget().pack(fill="both", expand=True)

    def _on_slider_bits_change(self, val):
        self._actualizar_tab_dsp()

    def _actualizar_tab_dsp(self):
        if self.analyzer_actual is None:
            return
            
        bits = int(self.slider_bits.get())
        q = self.analyzer_actual.cuantizar(bits=bits)
        
        # Actualizar texto de métricas
        delta_mv = q["delta_resolucion_v"] * 1000.0
        fe_mv = q["factor_escala_v_bit"] * 1000.0
        self.lbl_metricas_q.config(
            text=f"Niveles L: {q['niveles']} | Resolución Δ: {delta_mv:.2f} mV | Factor Escala: {fe_mv:.2f} mV/bit | SQNR: {q['sqnr_medido_db']:.2f} dB (Teórico: {q['sqnr_teorico_db']:.2f} dB)"
        )
        
        # Subplot 1: x(t) continuo vs muestreo x[n] y cuantizado y[n]
        ax1 = self.axes_dsp[0]
        ax1.clear()
        t_zoom_ms = 15.0
        n_zoom = int((t_zoom_ms / 1000.0) * self.analyzer_actual.fs)
        t_ms = self.analyzer_actual.t[:n_zoom] * 1000.0
        x_ms = self.analyzer_actual.x_v[:n_zoom]
        y_ms = q["y_dac"][:n_zoom]
        
        ax1.plot(t_ms, x_ms, color="#1f77b4", label="Señal Continua x(t)", linewidth=1.8)
        ax1.step(t_ms, y_ms, where="mid", color="#ff7f0e", label=f"Señal Cuantizada y[n] ({bits} bits, L={q['niveles']})", linewidth=1.5)
        ax1.set_title(f"1. Muestreo y Cuantización ADC - DAC ({bits} bits) | fs = {self.analyzer_actual.fs} Hz", fontsize=9, fontweight="bold")
        ax1.set_ylabel("Voltaje (V)", fontsize=8)
        ax1.grid(True, linestyle="--", alpha=0.5)
        ax1.legend(loc="upper right", fontsize=8)
        
        # Subplot 2: Espectro FFT y Nyquist-Shannon
        ax2 = self.axes_dsp[1]
        ax2.clear()
        idx_f = self.analyzer_actual.freqs <= 10000
        ax2.plot(self.analyzer_actual.freqs[idx_f], self.analyzer_actual.fft_mag[idx_f], color="#2ca02c", label="|X(f)| Magnitud Lineal (V)")
        ax2.axvline(self.analyzer_actual.f_max_efectiva, color="#d62728", linestyle="--", label=f"f_max (99%) = {self.analyzer_actual.f_max_efectiva:.1f} Hz")
        ax2.axvline(self.analyzer_actual.f_nyquist, color="#9467bd", linestyle="-.", label=f"f_Nyquist = fs/2 = {self.analyzer_actual.f_nyquist:.1f} Hz")
        ax2.set_title(f"2. Espectro FFT y Criterio de Nyquist-Shannon (fs >= 2*f_max: CUMPLE)", fontsize=9, fontweight="bold")
        ax2.set_ylabel("Magnitud (V)", fontsize=8)
        ax2.grid(True, linestyle="--", alpha=0.5)
        ax2.legend(loc="upper right", fontsize=8)
        
        # Subplot 3: Señal de Error de Cuantización e[n]
        ax3 = self.axes_dsp[2]
        ax3.clear()
        err_ms = q["error"][:n_zoom] * 1000.0
        lim_mv = q["max_error_teorico"] * 1000.0
        ax3.plot(t_ms, err_ms, color="#d62728", label="Error e[n] = x[n] - y[n] (mV)", linewidth=1.2)
        ax3.axhline(lim_mv, color="black", linestyle="--", label=f"+Δ/2 Teórico (+{lim_mv:.2f} mV)")
        ax3.axhline(-lim_mv, color="black", linestyle="--", label=f"-Δ/2 Teórico (-{lim_mv:.2f} mV)")
        ax3.set_title(f"3. Error de Cuantización Acotado en [-Δ/2, +Δ/2]", fontsize=9, fontweight="bold")
        ax3.set_xlabel("Tiempo (milisegundos)", fontsize=8)
        ax3.set_ylabel("Error (mV)", fontsize=8)
        ax3.grid(True, linestyle="--", alpha=0.5)
        ax3.legend(loc="upper right", fontsize=8)
        
        self.canvas_dsp.draw()

    # ----------------------------------------------------------------------------------------------
    # 4. PESTAÑA: EFECTO EN EL CEREBRO, EMOCIONES Y TDAH
    # ----------------------------------------------------------------------------------------------
    def _construir_tab_cerebro(self):
        frame_superior = ttk.LabelFrame(self.tab_cerebro, text=" Diagnóstico Neuroacústico Cerebral ", padding=10)
        frame_superior.pack(fill="x", padx=15, pady=8)
        
        self.lbl_estado_emocional = ttk.Label(
            frame_superior,
            text="ESTADO: CONCENTRADO Y SERENO",
            font=("Segoe UI", 13, "bold"),
            foreground="#2b6cb0"
        )
        self.lbl_estado_emocional.pack(anchor="w", pady=2)
        
        self.lbl_desc_emocional = ttk.Label(
            frame_superior,
            text="Descripción del efecto...",
            font=("Segoe UI", 10),
            wraplength=1100
        )
        self.lbl_desc_emocional.pack(anchor="w", pady=4)
        
        # Lienzo con Gráficas de Emociones y Ondas Cerebrales
        self.frame_graf_cerebro = ttk.Frame(self.tab_cerebro)
        self.frame_graf_cerebro.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.fig_cer, (self.ax_emo, self.ax_ondas) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig_cer.subplots_adjust(wspace=0.35)
        for ax in (self.ax_emo, self.ax_ondas):
            ax.set_facecolor("#f7fafc")
            ax.grid(True, linestyle="--", alpha=0.5)
            
        self.canvas_cer = FigureCanvasTkAgg(self.fig_cer, master=self.frame_graf_cerebro)
        self.canvas_cer.get_tk_widget().pack(fill="both", expand=True)

    def _actualizar_tab_cerebro(self):
        if self.impacto_cerebro is None:
            return
            
        imp = self.impacto_cerebro
        self.lbl_estado_emocional.config(
            text=f"ESTADO CEREBRAL PREDOMINANTE: {imp['estado_predominante']}"
        )
        self.lbl_desc_emocional.config(
            text=f"• Efecto Neuropsicológico: {imp['descripcion_emocional']}\n"
                 f"• Neurotransmisores Activados: {imp['neurotransmisores']}\n"
                 f"• Utilidad Recomendada para el Estudiante: {imp['actividad_ideal']}\n"
                 f"• Advertencia / TDAH: {imp['advertencia']}"
        )
        
        # Gráfica 1: Puntuaciones Emocionales (Contento, Triste, Concentrado, Hiperactivo, Enérgico)
        self.ax_emo.clear()
        estados = list(imp["puntuaciones"].keys())
        valores = list(imp["puntuaciones"].values())
        colores_emo = ["#2b6cb0", "#38a169", "#805ad5", "#dd6b20", "#e53e3e"]
        
        y_pos = np.arange(len(estados))
        bars = self.ax_emo.barh(y_pos, valores, color=colores_emo, edgecolor="black", height=0.55)
        self.ax_emo.set_yticks(y_pos)
        self.ax_emo.set_yticklabels(estados, fontsize=9, fontweight="bold")
        self.ax_emo.set_xlim([0, 110])
        self.ax_emo.set_xlabel("Nivel de Respuesta Emocional (%)", fontsize=9)
        self.ax_emo.set_title("Respuesta Emocional en el Cerebro", fontsize=10, fontweight="bold")
        self.ax_emo.grid(True, linestyle="--", alpha=0.5, axis="x")
        
        for bar in bars:
            w = bar.get_width()
            self.ax_emo.text(w + 2, bar.get_y() + bar.get_height()/2.0, f"{w}%", va="center", fontsize=8, fontweight="bold")
            
        # Gráfica 2: Estimulación de Ondas Cerebrales (Delta, Theta, Alfa, Beta, Gamma)
        self.ax_ondas.clear()
        ondas = list(imp["ondas_cerebrales"].keys())
        val_ondas = list(imp["ondas_cerebrales"].values())
        colores_ondas = ["#4a5568", "#d69e2e", "#3182ce", "#319795", "#d53f8c"]
        
        bars_ondas = self.ax_ondas.bar(range(len(ondas)), val_ondas, color=colores_ondas, edgecolor="black", width=0.55)
        self.ax_ondas.set_xticks(range(len(ondas)))
        self.ax_ondas.set_xticklabels(["Delta", "Theta", "Alfa", "Beta", "Gamma"], fontsize=9, fontweight="bold")
        self.ax_ondas.set_ylabel("Estimulación Cortical (%)", fontsize=9)
        self.ax_ondas.set_ylim([0, 115])
        self.ax_ondas.set_title("Estimulación de Ondas Cerebrales (EEG)", fontsize=10, fontweight="bold")
        self.ax_ondas.grid(True, linestyle="--", alpha=0.5, axis="y")
        
        for bar in bars_ondas:
            h = bar.get_height()
            self.ax_ondas.text(bar.get_x() + bar.get_width()/2.0, h + 2, f"{h}%", ha="center", fontsize=8, fontweight="bold")
            
        self.canvas_cer.draw()

# ==================================================================================================
# MODO INTERACTIVO POR CONSOLA (CLI FALLBACK)
# ==================================================================================================
def ejecutar_modo_consola_interactivo():
    """Permite utilizar todo el sistema de manera interactiva a través del teclado y la consola."""
    print("\n" + "=" * 80)
    print(" MENÚ INTERACTIVO DSP: CARGA DE AUDIO, SEPARACIÓN DE PISTAS Y EFECTOS EN EL CEREBRO")
    print("=" * 80)
    
    canciones = [f for f in os.listdir("audios") if f.endswith(".wav")]
    if not canciones:
        print("[AVISO] Generando audios de muestra iniciales...")
        from generar_audios_muestras import sintetizar_generos
        sintetizar_generos()
        canciones = [f for f in os.listdir("audios") if f.endswith(".wav")]
        
    print("\nSeleccione una opción de audio:")
    for idx, c in enumerate(canciones, 1):
        print(f"  [{idx}] {c}")
    print(f"  [{len(canciones)+1}] Ingresar ruta de mi propia canción (.wav personalizada)")
    
    opc = input(f"\nSeleccione opción [1-{len(canciones)+1}]: ").strip()
    try:
        opc_num = int(opc)
        if 1 <= opc_num <= len(canciones):
            ruta_audio = os.path.join("audios", canciones[opc_num - 1])
        else:
            ruta_audio = input("Ingrese la ruta absoluta o relativa de su archivo WAV: ").strip()
    except Exception:
        ruta_audio = os.path.join("audios", canciones[0])
        
    if not os.path.exists(ruta_audio):
        print(f"[ERROR] No existe el archivo: {ruta_audio}")
        return
        
    print("\nSeleccione el género musical de la canción:")
    generos = ["Clásica - Barroca", "Metal", "Salsa", "Cantina al hombro", "Reggaeton", "Personalizado"]
    for i, g in enumerate(generos, 1):
        print(f"  [{i}] {g}")
    opc_g = input("Seleccione género [1-6]: ").strip()
    try:
        gen_seleccionado = generos[int(opc_g) - 1]
    except Exception:
        gen_seleccionado = "Clásica - Barroca"
        
    print(f"\n[OK] Cargando audio: {ruta_audio} con género '{gen_seleccionado}'...")
    fs, raw = wavfile.read(ruta_audio)
    
    # Menú de Separación
    print("\n" + "-" * 80)
    print(" OPCIONES DE SEPARACIÓN DE INSTRUMENTOS Y VOZ (STEMS DSP)")
    print("-" * 80)
    print("  [1] Separar Voz Principal, Bajos, Instrumentos Melódicos y Percusión")
    print("  [2] Omitir separación y pasar directo al análisis de DSP y Cerebro")
    opc_sep = input("Seleccione opción [1 o 2]: ").strip()
    
    if opc_sep == "1":
        print("\nEjecutando separación de fuentes con filtros Butterworth digitales...")
        nombre_base = os.path.splitext(os.path.basename(ruta_audio))[0]
        stems = separar_pistas_audio(raw, fs, carpeta_salida="pistas_separadas", prefijo=nombre_base)
        print("Pistas generadas y guardadas exitosamente en 'pistas_separadas/':")
        for k, v in stems.items():
            print(f"  -> {v['ruta']} (Potencia relativa: {v['potencia_relativa']:.2e})")
            
    # Evaluación de DSP y Cerebro
    print("\n" + "-" * 80)
    print(" ANÁLISIS DE EFECTOS EN EL CEREBRO (TDAH Y ESTADOS EMOCIONALES)")
    print("-" * 80)
    impacto = evaluar_impacto_cerebral(gen_seleccionado)
    print(f"  • ESTADO PREDOMINANTE: {impacto['estado_predominante']}")
    print(f"  • Descripción         : {impacto['descripcion_emocional']}")
    print(f"  • Neurotransmisores   : {impacto['neurotransmisores']}")
    print(f"  • Actividad Ideal     : {impacto['actividad_ideal']}")
    print(f"  • Advertencia / TDAH  : {impacto['advertencia']}")
    print("\n  Puntuaciones Emocionales Estimadas:")
    for k, v in impacto["puntuaciones"].items():
        print(f"    - {k:25s}: {v}%")
    print("\n  Estimulación de Ondas Cerebrales (EEG):")
    for k, v in impacto["ondas_cerebrales"].items():
        print(f"    - {k:25s}: {v}%")
        
    print("\n" + "=" * 80)
    print(" Proceso interactivo finalizado con éxito.")
    print("=" * 80 + "\n")

# ==================================================================================================
# PUNTO DE ENTRADA
# ==================================================================================================
def main():
    # Si se pasa el argumento --cli se ejecuta directamente en terminal
    if "--cli" in sys.argv:
        ejecutar_modo_consola_interactivo()
        return

    # Si hay soporte de interfaz gráfica Tkinter
    try:
        root = tk.Tk()
        app = AppDSPInteractivo(root)
        root.mainloop()
    except Exception as e:
        print(f"[AVISO] No se pudo abrir la ventana gráfica ({e}). Cambiando a Modo Consola Interactivo...")
        ejecutar_modo_consola_interactivo()

if __name__ == "__main__":
    main()
