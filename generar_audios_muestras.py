"""
================================================================================
generar_audios_muestras.py
Generador sintético de muestras de audio representativas para 5 géneros musicales
Diseñado para la tarea de DSP: ADC - DAC y análisis de frecuencias para TDAH.
================================================================================
"""

import os
import numpy as np
import scipy.io.wavfile as wavfile

def sintetizar_generos(directorio_salida="audios", duracion=5.0, fs=44100):
    """
    Sintetiza 5 archivos WAV de audio de alta fidelidad acústica que reproducen
    las características espectrales y temporales típicas de cada género musical.
    """
    os.makedirs(directorio_salida, exist_ok=True)
    t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
    
    # -------------------------------------------------------------------------
    # 1. CLÁSICA - BARROCA
    # Johann Sebastian Bach - Concierto de Brandeburgo No. 3 en Sol Mayor, BWV 1048 (1721)
    # Timbre: Cuerdas frotadas (violines, viola, violonchelo) y clavicémbalo.
    # Armónicos suaves, vibrato, bajo continuo a 60-100 bpm.
    # -------------------------------------------------------------------------
    print("Sintetizando: 1. Clásica - Barroca (Bach - Brandeburgo BWV 1048)...")
    # Melodía de violines (Sol mayor: G4=392Hz, B4=493.88Hz, D5=587.33Hz, G5=783.99Hz)
    notas_g = [392.00, 493.88, 587.33, 783.99, 587.33, 493.88, 392.00, 293.66]
    melodia_barroca = np.zeros_like(t)
    dur_nota = duracion / len(notas_g)
    for i, freq in enumerate(notas_g):
        t_sub = t[(t >= i * dur_nota) & (t < (i + 1) * dur_nota)]
        t_local = t_sub - i * dur_nota
        # Violín: fundamental + armónicos pares e impares con decaimiento natural
        env = (1 - np.exp(-t_local * 15)) * np.exp(-t_local * 1.5)
        vibrato = 1 + 0.015 * np.sin(2 * np.pi * 5.5 * t_local)
        violon = (
            0.6 * np.sin(2 * np.pi * freq * vibrato * t_local) +
            0.3 * np.sin(2 * np.pi * 2 * freq * vibrato * t_local) +
            0.15 * np.sin(2 * np.pi * 3 * freq * vibrato * t_local) +
            0.08 * np.sin(2 * np.pi * 4 * freq * vibrato * t_local)
        ) * env
        melodia_barroca[(t >= i * dur_nota) & (t < (i + 1) * dur_nota)] = violon
        
    # Bajo continuo (violonchelo a 98 Hz - Sol2 y 146.8 Hz - Re3)
    bajo_continuo = 0.4 * np.sin(2 * np.pi * 98.0 * t) + 0.2 * np.sin(2 * np.pi * 146.8 * t)
    # Clavicémbalo (ataque rápido con agudos de plectro)
    clavicembal = 0.15 * np.sin(2 * np.pi * 587.33 * t) * (np.sin(2 * np.pi * 4 * t) > 0)
    audio_clasica = melodia_barroca + bajo_continuo + clavicembal
    audio_clasica = audio_clasica / np.max(np.abs(audio_clasica)) * 0.85

    # -------------------------------------------------------------------------
    # 2. METAL
    # Metallica - Master of Puppets (1986)
    # Timbre: Guitarra con distorsión pesada (clipping armónico), doble bombo rápido,
    # platillo crash brillante. Alto contenido de agudos estridentes y transitorios.
    # -------------------------------------------------------------------------
    print("Sintetizando: 2. Metal (Metallica - Master of Puppets)...")
    # Riff de guitarra con acordes de quinta (E power chord: E2=82.4Hz, B2=123.5Hz, E3=164.8Hz)
    riff_base = (
        np.sin(2 * np.pi * 82.4 * t) +
        0.8 * np.sin(2 * np.pi * 123.5 * t) +
        0.6 * np.sin(2 * np.pi * 164.8 * t)
    )
    # Distorsión no lineal severa (overdrive / clipping) que genera armónicos de alta frecuencia
    riff_distorsionado = np.tanh(4.0 * riff_base)
    # Doble bombo veloz (pulsos de baja frecuencia 60Hz a 180 bpm = 3 golpes por segundo)
    bombo_metal = np.zeros_like(t)
    bpm = 180
    intervalo_beat = 60.0 / bpm
    for beat in np.arange(0, duracion, intervalo_beat / 2):
        idx = (t >= beat) & (t < beat + 0.08)
        t_b = t[idx] - beat
        bombo_metal[idx] += np.sin(2 * np.pi * 65 * np.exp(-t_b * 30) * t_b) * np.exp(-t_b * 35)
    # Platillo crash / hi-hat rápido (ruido blanco filtrado en agudos 4kHz - 10kHz)
    ruido_platillo = np.random.normal(0, 0.15, size=len(t))
    modulador_platillo = np.abs(np.sin(2 * np.pi * (bpm/60) * t))**4
    platillo = ruido_platillo * modulador_platillo
    
    audio_metal = 0.5 * riff_distorsionado + 0.35 * bombo_metal + 0.25 * platillo
    audio_metal = audio_metal / np.max(np.abs(audio_metal)) * 0.92

    # -------------------------------------------------------------------------
    # 3. SALSA
    # Héctor Lavoe & Willie Colón - El Cantante (1978)
    # Timbre: Clave rítmica sincopada 2-3, tumbao de bajo, campana de timbal,
    # sección de bronces (trombón / trompeta) vibrante.
    # -------------------------------------------------------------------------
    print("Sintetizando: 3. Salsa (Héctor Lavoe - El Cantante)...")
    # Patrón de clave de son 2-3 (golpes secos a frecuencias 800Hz y 1200Hz)
    patron_clave = [0.0, 0.5, 1.25, 1.75, 2.25]  # segundos dentro de ciclo de 2.5s
    clave_senal = np.zeros_like(t)
    for c_start in np.arange(0, duracion, 2.5):
        for pulso in patron_clave:
            t_p = c_start + pulso
            idx = (t >= t_p) & (t < t_p + 0.04)
            if np.any(idx):
                t_l = t[idx] - t_p
                clave_senal[idx] += np.sin(2 * np.pi * 1200 * t_l) * np.exp(-t_l * 80)
    # Tumbao de bajo sincopado (Baby Bass en Fa y Do: 87.3Hz y 130.8Hz)
    tumbao = (
        0.5 * np.sin(2 * np.pi * 87.3 * t) * (np.sin(2 * np.pi * 1.6 * t) > 0) +
        0.4 * np.sin(2 * np.pi * 130.8 * t) * (np.cos(2 * np.pi * 1.6 * t) > 0)
    )
    # Metales / Trombones brillantes (acordes con armónicos ricos en 400Hz - 2500Hz)
    bronces = (
        0.3 * np.sin(2 * np.pi * 349.2 * t) +   # Fa4
        0.25 * np.sin(2 * np.pi * 440.0 * t) +  # La4
        0.2 * np.sin(2 * np.pi * 523.2 * t) +   # Do5
        0.15 * np.sin(2 * np.pi * 698.4 * t)    # Fa5
    ) * (np.sin(2 * np.pi * 0.8 * t)**2)
    # Timbal / Campana de percusión menor
    timbal = 0.15 * np.sin(2 * np.pi * 600 * t) * (np.sin(2 * np.pi * 3.2 * t)**6)
    audio_salsa = 0.35 * tumbao + 0.35 * bronces + 0.2 * clave_senal + 0.15 * timbal
    audio_salsa = audio_salsa / np.max(np.abs(audio_salsa)) * 0.88

    # -------------------------------------------------------------------------
    # 4. CANTINA AL HOMBRO (Música Popular / Carrilera / Despecho)
    # Darío Gómez - Nadie es eterno en el mundo (1989)
    # Timbre: Requinto con trémolo punteado acústico (frecuencias medias nasales
    # 350-1500 Hz), bajo caminante sencillo en compás de 3/4 o corrido, maracas/güiro suave.
    # -------------------------------------------------------------------------
    print("Sintetizando: 4. Cantina al hombro (Darío Gómez - Nadie es eterno)...")
    # Punteo de Requinto (Tonalidad La menor / Mi mayor con trémolo rápido característico)
    frecuencias_requinto = [440.0, 493.88, 523.25, 587.33, 659.25, 523.25, 493.88, 440.0]
    requinto = np.zeros_like(t)
    dur_paso = duracion / len(frecuencias_requinto)
    for i, freq in enumerate(frecuencias_requinto):
        idx = (t >= i * dur_paso) & (t < (i + 1) * dur_paso)
        t_l = t[idx] - i * dur_paso
        # Efecto de púa / trémolo a 12 Hz típico del requinto colombiano
        tremolo = 1 + 0.4 * np.sin(2 * np.pi * 12 * t_l)
        onda_requinto = (
            0.6 * np.sin(2 * np.pi * freq * t_l) +
            0.35 * np.sin(2 * np.pi * 2 * freq * t_l) +
            0.2 * np.sin(2 * np.pi * 3 * freq * t_l)
        ) * np.exp(-t_l * 2.5) * tremolo
        requinto[idx] = onda_requinto
    # Acompañamiento rítmico de guitarra campesina (rasgueo 3/4)
    guitarra_ritmica = 0.3 * np.sin(2 * np.pi * 220 * t) * (np.sin(2 * np.pi * 3 * t)**4)
    # Bajo acústico de cantina (La1=55Hz, Mi2=82.4Hz)
    bajo_cantina = 0.4 * np.sin(2 * np.pi * 82.4 * t) * (np.sin(2 * np.pi * 1.5 * t) > 0)
    audio_cantina = 0.5 * requinto + 0.3 * guitarra_ritmica + 0.25 * bajo_cantina
    audio_cantina = audio_cantina / np.max(np.abs(audio_cantina)) * 0.85

    # -------------------------------------------------------------------------
    # 5. REGGAETON
    # Daddy Yankee - Gasolina (2004)
    # Timbre: Bombo sub-grave "808" hiper-saturado en 45-60 Hz, patrón rítmico
    # "Dembow" (bombo en tierra y caja/snare sincopada en contratiempo), sintetizador lead.
    # -------------------------------------------------------------------------
    print("Sintetizando: 5. Reggaeton (Daddy Yankee - Gasolina)...")
    tempo_reggaeton = 95 # bpm
    t_compas = 60.0 / tempo_reggaeton
    reggaeton_dembow = np.zeros_like(t)
    # Generar patrón rítmico Dembow recurrente
    for bar in np.arange(0, duracion, t_compas):
        # Bombo 808 en el pulso 0 y pulso 0.5 (pesado sub-bass en 50Hz)
        for kick_p in [0.0, 0.5 * t_compas]:
            t_k = bar + kick_p
            idx = (t >= t_k) & (t < t_k + 0.15)
            if np.any(idx):
                tl = t[idx] - t_k
                # Sub-bajo 808 con caída de frecuencia rápida (pitch envelope)
                f_kick = 90 * np.exp(-tl * 25) + 45
                reggaeton_dembow[idx] += 0.8 * np.sin(2 * np.pi * f_kick * tl) * np.exp(-tl * 10)
        # Snare sincopado Dembow en pulso 0.375 y 0.75 del compás (caja típica)
        for snare_p in [0.375 * t_compas, 0.75 * t_compas]:
            t_s = bar + snare_p
            idx = (t >= t_s) & (t < t_s + 0.10)
            if np.any(idx):
                tl = t[idx] - t_s
                snare_sound = (
                    0.4 * np.sin(2 * np.pi * 220 * tl) + 
                    0.4 * np.random.normal(0, 0.2, size=len(tl))
                ) * np.exp(-tl * 25)
                reggaeton_dembow[idx] += snare_sound
                
    # Sintetizador lead digital repetitivo y agudo
    lead_sint = 0.25 * np.sin(2 * np.pi * 523.25 * t) * (np.sin(2 * np.pi * (tempo_reggaeton/60) * 2 * t) > 0)
    audio_reggaeton = reggaeton_dembow + lead_sint
    audio_reggaeton = audio_reggaeton / np.max(np.abs(audio_reggaeton)) * 0.95

    # -------------------------------------------------------------------------
    # Guardar los 5 archivos en formato WAV estándar (16 bits PCM, 44100 Hz)
    # -------------------------------------------------------------------------
    canciones = {
        "1_clasica_barroca.wav": audio_clasica,
        "2_metal.wav": audio_metal,
        "3_salsa.wav": audio_salsa,
        "4_cantina_al_hombro.wav": audio_cantina,
        "5_reggaeton.wav": audio_reggaeton
    }
    
    rutas_generadas = {}
    for nombre_archivo, audio_data in canciones.items():
        ruta = os.path.join(directorio_salida, nombre_archivo)
        # Convertir a formato PCM 16-bit
        audio_int16 = (audio_data * 32767).astype(np.int16)
        wavfile.write(ruta, fs, audio_int16)
        rutas_generadas[nombre_archivo] = ruta
        print(f" -> Guardado: {ruta} ({duracion}s, {fs}Hz, 16-bit)")
        
    print("\n[OK] Se han sintetizado exitosamente los 5 audios WAV de referencia.\n")
    return rutas_generadas

if __name__ == "__main__":
    sintetizar_generos()
