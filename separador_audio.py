"""
================================================================================
separador_audio.py
Módulo DSP de Separación de Fuentes de Audio:
  - Voz Principal (Aislamiento vocal / formantes)
  - Bajos y Sub-bajos (Línea de bajo y bombo)
  - Instrumentos Melódicos / Armónicos (Guitarras, cuerdas, pianos, sintetizadores)
  - Percusión y Agudos (Batería, caja, platillos, sibilancias)
================================================================================
"""

import os
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import butter, sosfiltfilt

def disenar_filtro_pasabajas(f_corte, fs, orden=4):
    """Diseña un filtro Butterworth paso-bajas estable en secciones de segundo orden (SOS)."""
    nyq = 0.5 * fs
    f_norm = min(max(f_corte / nyq, 0.001), 0.99)
    sos = butter(orden, f_norm, btype="low", output="sos")
    return sos

def disenar_filtro_pasabanda(f_baja, f_alta, fs, orden=4):
    """Diseña un filtro Butterworth paso-banda estable en SOS."""
    nyq = 0.5 * fs
    f_low = max(f_baja / nyq, 0.001)
    f_high = min(f_alta / nyq, 0.99)
    if f_low >= f_high:
        f_high = min(f_low + 0.05, 0.99)
    sos = butter(orden, [f_low, f_high], btype="band", output="sos")
    return sos

def disenar_filtro_pasaaltas(f_corte, fs, orden=4):
    """Diseña un filtro Butterworth paso-altas estable en SOS."""
    nyq = 0.5 * fs
    f_norm = min(max(f_corte / nyq, 0.001), 0.99)
    sos = butter(orden, f_norm, btype="high", output="sos")
    return sos

def separar_pistas_audio(audio_data, fs, carpeta_salida="pistas_separadas", prefijo="pista"):
    """
    Separa una señal de audio en 4 componentes instrumentales/vocales principales
    utilizando filtrado digital IIR de fase cero (filtfilt) y técnicas de Mid-Side:
      1. Bajos / Sub-bajos (20 Hz - 260 Hz)
      2. Voz Principal / Formantes Vocales (300 Hz - 3400 Hz)
      3. Instrumentos Melódicos / Cuerdas / Armonía (400 Hz - 5500 Hz)
      4. Percusión de Agudos / Platillos (> 5000 Hz)
    """
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Manejo estéreo vs mono
    es_estereo = (audio_data.ndim > 1 and audio_data.shape[1] > 1)
    if es_estereo:
        canal_l = audio_data[:, 0].astype(np.float64)
        canal_r = audio_data[:, 1].astype(np.float64)
        mono = 0.5 * (canal_l + canal_r)
        # En estéreo, la voz principal suele estar paneada al centro exacto (L = R)
        # Componente central (Mid) y componente estéreo lateral (Sides)
        mid = 0.5 * (canal_l + canal_r)
        sides = 0.5 * (canal_l - canal_r)
    else:
        if audio_data.ndim > 1:
            mono = audio_data[:, 0].astype(np.float64)
        else:
            mono = audio_data.astype(np.float64)
        mid = mono
        sides = np.zeros_like(mono)

    # 1. Pista de Bajos / Sub-bajos (Filtro paso-bajas fc = 260 Hz)
    sos_bajos = disenar_filtro_pasabajas(260.0, fs, orden=4)
    pista_bajos = sosfiltfilt(sos_bajos, mono)
    
    # 2. Pista de Voz Principal (Filtro paso-banda 320 Hz - 3400 Hz con énfasis central)
    sos_voz = disenar_filtro_pasabanda(320.0, 3400.0, fs, orden=4)
    # Extraer formantes vocales
    voz_base = sosfiltfilt(sos_voz, mid)
    if es_estereo and np.max(np.abs(sides)) > 0:
        # Reducir instrumentos paneados a los lados para resaltar la voz central
        pista_voz = voz_base - 0.3 * sosfiltfilt(sos_voz, sides)
    else:
        pista_voz = voz_base
        
    # 3. Pista de Instrumentos Melódicos / Armónicos (400 Hz - 5500 Hz)
    sos_medios = disenar_filtro_pasabanda(400.0, 5500.0, fs, orden=4)
    pista_medios = sosfiltfilt(sos_medios, mono)
    # Atenuar el componente vocal puro para favorecer las guitarras/cuerdas
    pista_medios = pista_medios - 0.4 * pista_voz
    
    # 4. Pista de Percusión y Agudos (Filtro paso-altas fc = 5000 Hz)
    sos_agudos = disenar_filtro_pasaaltas(5000.0, fs, orden=4)
    pista_agudos = sosfiltfilt(sos_agudos, mono)

    # Normalización para evitar clipping al guardar en WAV PCM 16-bit
    pistas = {
        "bajos_y_bombos": pista_bajos,
        "voz_principal": pista_voz,
        "instrumentos_medios": pista_medios,
        "percusion_y_agudos": pista_agudos
    }
    
    rutas_guardadas = {}
    for nombre_clave, senal in pistas.items():
        max_val = np.max(np.abs(senal))
        if max_val > 0:
            senal_norm = senal / max_val * 0.90
        else:
            senal_norm = senal
            
        audio_int16 = (senal_norm * 32767).astype(np.int16)
        ruta_archivo = os.path.join(carpeta_salida, f"{prefijo}_{nombre_clave}.wav")
        wavfile.write(ruta_archivo, fs, audio_int16)
        rutas_guardadas[nombre_clave] = {
            "ruta": ruta_archivo,
            "senal": senal_norm,
            "potencia_relativa": float(np.mean(senal**2))
        }

    return rutas_guardadas

if __name__ == "__main__":
    # Prueba con un audio sintético existente
    ruta_test = os.path.join("audios", "1_clasica_barroca.wav")
    if os.path.exists(ruta_test):
        fs, data = wavfile.read(ruta_test)
        rutas = separar_pistas_audio(data, fs, prefijo="test")
        print("Pistas separadas con éxito:")
        for k, v in rutas.items():
            print(f"  - {k}: {v['ruta']} (Potencia: {v['potencia_relativa']:.4e})")
