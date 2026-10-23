"""
====================================================================================================
servidor_web_dsp.py
SERVIDOR WEB INTERACTIVO PARA DSP EN EL NAVEGADOR
====================================================================================================
Permite:
  1. Cargar canciones en el navegador (examinar archivo WAV propio o seleccionar predeterminados).
  2. Seleccionar el género de la canción.
  3. Separar voz e instrumentos con filtros DSP y escucharlos/descargarlos directamente en la web.
  4. Graficar x(t), muestreo, Nyquist-Shannon y cuantización ADC-DAC interactiva (cambio de bits).
  5. Evaluar el impacto en el cerebro (Contento, Triste, Concentrado, Hiperactivo) y patología TDAH.
====================================================================================================
"""

import os
import sys
import io
import base64
import webbrowser
import threading
import time

try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Importar lógica DSP desarrollada
from dsp_audio_analisis import INVESTIGACION_GENEROS, AudioDSPAnalyzer
from separador_audio import separar_pistas_audio
from evaluador_cerebro import evaluar_impacto_cerebral

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'audios'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB

os.makedirs("audios", exist_ok=True)
os.makedirs("pistas_separadas", exist_ok=True)
os.makedirs("graficas", exist_ok=True)

# Estado global en memoria para la sesión activa
ESTADO = {
    "ruta_actual": os.path.join("audios", "1_clasica_barroca.wav"),
    "genero_actual": "Clásica - Barroca",
    "analyzer": None,
    "pistas": None,
    "cerebro": None
}

def inicializar_audio_defecto():
    ruta = os.path.join("audios", "1_clasica_barroca.wav")
    if not os.path.exists(ruta):
        from generar_audios_muestras import sintetizar_generos
        sintetizar_generos()
    if os.path.exists(ruta):
        ESTADO["ruta_actual"] = ruta
        ESTADO["genero_actual"] = "Clásica - Barroca"
        info = INVESTIGACION_GENEROS["clasica_barroca"]
        ESTADO["analyzer"] = AudioDSPAnalyzer(ruta, info, v_ref=1.0)
        ESTADO["cerebro"] = evaluar_impacto_cerebral("Clásica - Barroca")

def fig_a_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{img_b64}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/biblioteca', methods=['GET'])
def obtener_biblioteca():
    canciones = [f for f in os.listdir("audios") if f.endswith(".wav")]
    canciones.sort()
    return jsonify({
        "canciones": canciones,
        "actual": os.path.basename(ESTADO["ruta_actual"]) if ESTADO["ruta_actual"] else "",
        "genero_actual": ESTADO["genero_actual"]
    })

@app.route('/api/cargar_audio', methods=['POST'])
def cargar_audio():
    tipo = request.form.get("tipo", "preset")
    genero = request.form.get("genero", "Clásica - Barroca")
    
    if tipo == "upload":
        if 'archivo' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400
        nombre_seguro = secure_filename(archivo.filename)
        ruta_guardado = os.path.join("audios", nombre_seguro)
        archivo.save(ruta_guardado)
        ruta_audio = ruta_guardado
    else:
        nombre_cancion = request.form.get("cancion", "1_clasica_barroca.wav")
        ruta_audio = os.path.join("audios", nombre_cancion)
        
    if not os.path.exists(ruta_audio):
        return jsonify({"error": f"Archivo no encontrado: {ruta_audio}"}), 404
        
    ESTADO["ruta_actual"] = ruta_audio
    ESTADO["genero_actual"] = genero
    
    # Determinar información de investigación
    clave_gen = "clasica_barroca"
    g_low = genero.lower()
    if "metal" in g_low:
        clave_gen = "metal"
    elif "salsa" in g_low:
        clave_gen = "salsa"
    elif "cantina" in g_low or "carrilera" in g_low:
        clave_gen = "cantina_al_hombro"
    elif "reggaeton" in g_low:
        clave_gen = "reggaeton"
        
    info = INVESTIGACION_GENEROS.get(clave_gen, {
        "genero": genero,
        "obra": os.path.basename(ruta_audio),
        "musico_compositor": "Artista / Intérprete",
        "tipo_agrupacion": "Banda / Orquesta / Ensamble",
        "ano_obra": "Contemporáneo",
        "contexto_historico": "Audio cargado por el usuario en el navegador web.",
        "impacto_tdh": "Evaluado según métricas DSP."
    })
    
    ESTADO["analyzer"] = AudioDSPAnalyzer(ruta_audio, info, v_ref=1.0)
    ESTADO["cerebro"] = evaluar_impacto_cerebral(genero)
    ESTADO["pistas"] = None # Reiniciar pistas separadas
    
    dsp = ESTADO["analyzer"]
    metricas = dsp.calcular_metricas_frecuencia()
    
    # Generar gráfica inicial de señal x(t) y FFT
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
    fig.subplots_adjust(hspace=0.45)
    
    t_zoom_ms = 25.0
    n_zoom = int((t_zoom_ms / 1000.0) * dsp.fs)
    t_ms = dsp.t[:n_zoom] * 1000.0
    x_ms = dsp.x_v[:n_zoom]
    
    ax1.plot(t_ms, x_ms, color="#2b6cb0", linewidth=1.5, label="Señal x(t)")
    ax1.set_title(f"Señal Continua x(t) - Ventana de {t_zoom_ms} ms", fontsize=10, fontweight="bold")
    ax1.set_xlabel("Tiempo (ms)", fontsize=8)
    ax1.set_ylabel("Voltaje (V)", fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=8)
    
    idx_f = dsp.freqs <= 8000
    ax2.plot(dsp.freqs[idx_f], dsp.fft_mag[idx_f], color="#2f855a", linewidth=1.2, label="|X(f)| Magnitud FFT")
    ax2.axvline(dsp.f_max_efectiva, color="#e53e3e", linestyle="--", label=f"f_max (99%) = {dsp.f_max_efectiva:.1f} Hz")
    ax2.axvline(dsp.f_nyquist, color="#805ad5", linestyle="-.", label=f"f_Nyquist = {dsp.f_nyquist:.1f} Hz")
    ax2.set_title(f"Espectro de Magnitud FFT y Nyquist-Shannon (fs = {dsp.fs} Hz)", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Frecuencia (Hz)", fontsize=8)
    ax2.set_ylabel("Magnitud (V)", fontsize=8)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=8)
    
    grafica_b64 = fig_a_base64(fig)
    
    return jsonify({
        "mensaje": "Audio cargado exitosamente",
        "archivo": os.path.basename(ruta_audio),
        "url_audio": f"/audio/original/{os.path.basename(ruta_audio)}",
        "genero": genero,
        "investigacion": info,
        "dsp": {
            "fs": dsp.fs,
            "periodo_us": (1.0 / dsp.fs) * 1e6,
            "f_nyquist": dsp.f_nyquist,
            "f_max_efectiva": dsp.f_max_efectiva,
            "duracion_seg": round(dsp.duracion, 2),
            "num_muestras": dsp.n_muestras,
            "centroide_hz": round(metricas["centroide_hz"], 1),
            "pct_graves": round(metricas["pct_graves"], 1),
            "pct_medios": round(metricas["pct_medios"], 1),
            "pct_agudos": round(metricas["pct_agudos"], 1)
        },
        "grafica_senal": grafica_b64
    })

@app.route('/api/cuantizar', methods=['POST'])
def cuantizar():
    if ESTADO["analyzer"] is None:
        return jsonify({"error": "No hay audio cargado"}), 400
        
    data = request.get_json() or {}
    bits = int(data.get("bits", 4))
    
    dsp = ESTADO["analyzer"]
    q = dsp.cuantizar(bits=bits)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5.2))
    fig.subplots_adjust(hspace=0.45)
    
    t_zoom_ms = 15.0
    n_zoom = int((t_zoom_ms / 1000.0) * dsp.fs)
    t_ms = dsp.t[:n_zoom] * 1000.0
    x_ms = dsp.x_v[:n_zoom]
    y_ms = q["y_dac"][:n_zoom]
    err_ms = q["error"][:n_zoom] * 1000.0
    lim_mv = q["max_error_teorico"] * 1000.0
    
    ax1.plot(t_ms, x_ms, color="#2b6cb0", alpha=0.6, linestyle=":", label="Señal original x[n]")
    ax1.step(t_ms, y_ms, where="mid", color="#dd6b20", linewidth=1.8, label=f"Cuantizada y[n] ({bits} bits, L={q['niveles']})")
    ax1.set_title(f"Cuantización ADC - DAC ({bits} bits) | Δ = {q['delta_resolucion_v']*1000:.2f} mV | SQNR = {q['sqnr_medido_db']:.2f} dB", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Voltaje (V)", fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=8)
    
    ax2.plot(t_ms, err_ms, color="#e53e3e", linewidth=1.2, label="Error e[n] (mV)")
    ax2.axhline(lim_mv, color="black", linestyle="--", label=f"+Δ/2 ({lim_mv:.2f} mV)")
    ax2.axhline(-lim_mv, color="black", linestyle="--", label=f"-Δ/2 (-{lim_mv:.2f} mV)")
    ax2.set_title("Señal de Error de Cuantización e[n] = x[n] - y[n]", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Tiempo (ms)", fontsize=8)
    ax2.set_ylabel("Error (mV)", fontsize=8)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=8)
    
    grafica_b64 = fig_a_base64(fig)
    
    return jsonify({
        "bits": bits,
        "niveles": q["niveles"],
        "delta_mv": round(q["delta_resolucion_v"] * 1000.0, 3),
        "factor_escala_mv_bit": round(q["factor_escala_v_bit"] * 1000.0, 3),
        "sqnr_medido_db": round(q["sqnr_medido_db"], 2),
        "sqnr_teorico_db": round(q["sqnr_teorico_db"], 2),
        "grafica_cuantizacion": grafica_b64
    })

@app.route('/api/separar_audio', methods=['POST'])
def separar():
    if ESTADO["analyzer"] is None:
        return jsonify({"error": "No hay audio cargado"}), 400
        
    ruta = ESTADO["ruta_actual"]
    nombre_base = os.path.splitext(os.path.basename(ruta))[0]
    
    fs, raw = wavfile.read(ruta)
    stems = separar_pistas_audio(raw, fs, carpeta_salida="pistas_separadas", prefijo=nombre_base)
    ESTADO["pistas"] = stems
    
    # Generar gráfica de las 4 pistas
    fig, axes = plt.subplots(4, 1, figsize=(10, 6.5))
    fig.subplots_adjust(hspace=0.45)
    
    t_zoom_ms = 35.0
    n_zoom = int((t_zoom_ms / 1000.0) * fs)
    t_ms = (np.arange(n_zoom) / fs) * 1000.0
    
    pistas_info = [
        ("Voz Principal (300 - 3400 Hz)", "voz_principal", "#e53e3e"),
        ("Línea de Bajos y Bombos (20 - 260 Hz)", "bajos_y_bombos", "#2b6cb0"),
        ("Instrumentos Melódicos / Cuerdas (400 - 5500 Hz)", "instrumentos_medios", "#2f855a"),
        ("Percusión y Agudos (> 5000 Hz)", "percusion_y_agudos", "#805ad5")
    ]
    
    urls_pistas = {}
    for i, (titulo, clave, color) in enumerate(pistas_info):
        ax = axes[i]
        datos = stems[clave]
        ax.plot(t_ms, datos["senal"][:n_zoom], color=color, linewidth=1.2, label=titulo)
        ax.set_ylabel("Amplitud", fontsize=8)
        ax.set_title(titulo, fontsize=9, fontweight="bold", pad=2)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="upper right", fontsize=8)
        urls_pistas[clave] = {
            "nombre": titulo,
            "url": f"/audio/stem/{os.path.basename(datos['ruta'])}",
            "archivo": os.path.basename(datos['ruta'])
        }
        
    axes[-1].set_xlabel("Tiempo (ms)", fontsize=8)
    grafica_b64 = fig_a_base64(fig)
    
    return jsonify({
        "mensaje": "Separación de fuentes realizada con éxito",
        "pistas": urls_pistas,
        "grafica_stems": grafica_b64
    })

@app.route('/api/efecto_cerebro', methods=['GET'])
def efecto_cerebro():
    genero = ESTADO["genero_actual"]
    imp = evaluar_impacto_cerebral(genero)
    return jsonify(imp)

@app.route('/audio/original/<filename>')
def servir_audio_original(filename):
    return send_from_directory('audios', filename)

@app.route('/audio/stem/<filename>')
def servir_audio_stem(filename):
    return send_from_directory('pistas_separadas', filename)

@app.route('/graficas/<filename>')
def servir_grafica(filename):
    return send_from_directory('graficas', filename)

def abrir_navegador(url, delay=1.2):
    time.sleep(delay)
    print(f"\n[NAVEGADOR]: Abriendo automáticamente la interfaz web en {url}...\n")
    webbrowser.open(url)

if __name__ == '__main__':
    inicializar_audio_defecto()
    puerto = 5000
    url_local = f"http://127.0.0.1:{puerto}"
    print("=" * 80)
    print(f" SERVIDOR WEB DSP ACTIVO EN: {url_local}")
    print("=" * 80)
    
    # Lanzar apertura del navegador en un hilo separado
    hilo_browser = threading.Thread(target=abrir_navegador, args=(url_local,), daemon=True)
    hilo_browser.start()
    
    app.run(host="127.0.0.1", port=puerto, debug=False)
