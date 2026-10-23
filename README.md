# 🎵 Suite de Procesamiento Digital de Señales (DSP) para Audio WAV
### ADC – DAC, Análisis Espectral (FFT), Separación de Pistas y Evaluación Psicoacústica para TDAH

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-green.svg)
![DSP](https://img.shields.io/badge/DSP-ADC%20%2F%20DAC%20%2F%20FFT-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

---

## 📌 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Estructura del Repositorio](#-estructura-del-repositorio)
3. [Requisitos e Instalación](#-requisitos-e-instalación)
4. [Modos de Ejecución](#-modos-de-ejecución)
   - [Opción 1: Servidor Web Interactivo en Navegador](#opción-1-servidor-web-interactivo-en-el-navegador-recomendado)
   - [Opción 2: Aplicación Gráfica de Escritorio (GUI)](#opción-2-aplicación-gráfica-de-escritorio-gui)
   - [Opción 3: Modo Consola Interactivo (CLI)](#opción-3-modo-consola-interactivo-cli)
   - [Opción 4: Procesamiento Batch Automatizado](#opción-4-procesamiento-batch-automatizado)
5. [Fundamentación Teórica y Métricas DSP](#-fundamentación-teórica-y-métricas-dsp)
6. [Investigación de los 5 Géneros Musicales](#-investigación-de-los-5-géneros-musicales)
7. [Separación de Pistas por DSP (Stems)](#-separación-de-pistas-por-dsp-stems)
8. [Diagnóstico y Análisis Neuroacústico para TDAH](#-diagnóstico-y-análisis-neuroacústico-para-tdah)
9. [Documentación Formal](#-documentación-formal)

---

## 📖 Descripción General

Este proyecto implementa una suite integral de **Procesamiento Digital de Señales (DSP)** aplicada a señales sonoras en formato WAV para la asignatura de **Comunicaciones 1**. 

El sistema cubre todo el flujo del procesamiento digital:
- **Conversión Analógico-Digital (ADC) y Digital-Analógica (DAC):** modelado riguroso de muestreo uniforme a frecuencia de Nyquist, cuantización a $B \in \{4, 8, 16\}$ bits, cálculo de paso $\Delta$ (LSB), señal de error de cuantización $e[n]$ y relación señal a ruido de cuantización ($\text{SQNR}$).
- **Análisis Espectral de Fourier:** Transformada Rápida de Fourier (FFT), densidad espectral, envolventes y cálculo de centroides espectrales.
- **Separación de Pistas (Stems):** división espectral en tiempo real mediante filtros digitales pasa-bajas, pasa-bandas y pasa-altas para aislar:
  1. *Voz Principal* ($250\text{ Hz} - 4000\text{ Hz}$).
  2. *Bajos y Bombos Sub-bass* ($20\text{ Hz} - 250\text{ Hz}$).
  3. *Instrumentos Medios y Armónicos* ($400\text{ Hz} - 4500\text{ Hz}$).
  4. *Percusión, Platillos y Agudos* ($4000\text{ Hz} - 20000\text{ Hz}$).
- **Evaluación Psicoacústica y Neuroacústica para TDAH:** análisis de estimulación sensorial y respuesta neurológica (estados Alfa, Beta, Theta y Gamma) para evaluar la idoneidad terapéutica de cada género musical en personas con Déficit de Atención e Hiperactividad.

---

## 📁 Estructura del Repositorio

```text
.
├── audios/                                 # Directorio para audios WAV de entrada (44.1 kHz, 16-bit PCM)
│   └── .gitkeep
├── pistas_separadas/                       # Archivos WAV separados generados por DSP (stems)
│   └── .gitkeep
├── graficas/                               # Gráficas generadas en alta definición (300 DPI)
│   ├── comparativa_general_generos_y_tdah.png
│   ├── analisis_individual_1_analisis_clasica_barroca.png
│   ├── analisis_individual_2_analisis_metal.png
│   ├── analisis_individual_3_analisis_salsa.png
│   ├── analisis_individual_4_analisis_cantina_al_hombro.png
│   └── analisis_individual_5_analisis_reggaeton.png
├── templates/
│   └── index.html                          # Interfaz web responsiva con reproductor y visualizador
├── app_dsp_interactivo.py                  # Interfaz gráfica de escritorio (Tkinter) y modo CLI
├── servidor_web_dsp.py                     # Servidor Web Flask con reproductor de stems y análisis interactivo
├── separador_audio.py                      # Módulo de filtrado DSP para separación de pistas
├── evaluador_cerebro.py                    # Evaluador neuroacústico de ondas cerebrales y TDAH
├── dsp_audio_analisis.py                   # Script de análisis por lotes y generación de figuras
├── generar_audios_muestras.py             # Generador acústico sintético para los 5 géneros
├── INFORME_TEORICO_DSP.md                  # Informe formal con deducciones matemáticas y tablas comparativas
├── requirements.txt                        # Dependencias de Python
└── README.md                               # Documentación principal del proyecto
```

---

## ⚙️ Requisitos e Instalación

### Requisitos Previos
- **Python 3.10 o superior** (probado en Python 3.10, 3.11, 3.12 y 3.13 en Windows/Linux/macOS).
- Navegador web moderno (Chrome, Edge, Firefox, Safari).

### Instalación de Dependencias

1. Clonar el repositorio:
```bash
git clone https://github.com/<tu-usuario>/<tu-repositorio>.git
cd "tarea audio de canciones"
```

2. Instalar los paquetes requeridos:
```bash
pip install -r requirements.txt
```

---

## 🚀 Modos de Ejecución

### Opción 1: Servidor Web Interactivo en el Navegador (Recomendado)
Inicia una aplicación web completa con reproductor multimedia, controles interactivos de cuantización ADC-DAC, separación de voz e instrumentos y diagnóstico en tiempo real:

```bash
python servidor_web_dsp.py
# O en Windows con lanzador py:
py -3.13 servidor_web_dsp.py
```
> El navegador se abrirá automáticamente en `http://localhost:5000`.

**Características de la Web:**
- Permite subir cualquier canción en formato WAV o elegir las predeterminadas.
- Reproductor de audio HTML5 independiente para cada pista separada (Voz, Bajos, Medios, Percusión).
- Selector interactivo de bits de cuantización ($B = 4, 8, 16\text{ bits}$) con cálculo dinámico de $\Delta$ y SQNR.
- Tarjeta de diagnóstico cerebral y compatibilidad con el TDAH.

---

### Opción 2: Aplicación Gráfica de Escritorio (GUI)
Interfaz basada en ventanas de escritorio nativas:
```bash
python app_dsp_interactivo.py
```

---

### Opción 3: Modo Consola Interactivo (CLI)
Menú interactivo en terminal para entornos sin servidor gráfico:
```bash
python app_dsp_interactivo.py --cli
```

---

### Opción 4: Procesamiento Batch Automatizado
Analiza automáticamente los 5 géneros en lote, calcula las tablas numéricas y genera todas las gráficas de 300 DPI en la carpeta `graficas/`:
```bash
python dsp_audio_analisis.py
```

> **Sintetizador Automático:** Si la carpeta `audios/` no cuenta con archivos, el sistema ejecuta automáticamente `generar_audios_muestras.py` para sintetizar piezas de prueba con fidelidad espectral representativa.

---

## 📊 Fundamentación Teórica y Métricas DSP

### 1. Muestreo y Teorema de Nyquist-Shannon
Para evitar el fenómeno de *aliasing* (traslape espectral):
$$f_s \ge 2 f_{max} \implies f_{Nyquist} = \frac{f_s}{2} = 22050\text{ Hz}$$
A una tasa de muestreo estándar de $f_s = 44.1\text{ kHz}$, el período entre muestras consecutivas es:
$$T_s = \frac{1}{f_s} \approx 22.68\text{ }\mu\text{s}$$

### 2. Cuantización Uniforme ADC - DAC
La señal continua $x(t)$ se escala al rango $[-1.0\text{ V}, +1.0\text{ V}]$ ($V_{pp} = 2.0\text{ V}$). Para una profundidad de $B$ bits:
- **Niveles de cuantización:** $L = 2^B$
- **Resolución / Tamaño de Paso ($\Delta$ o LSB):**
$$\Delta = \frac{V_{max} - V_{min}}{2^B - 1}$$
- **Señal de Error de Cuantización:** $e[n] = x[n] - y[n]$, acotada estrictamente en $[-\Delta / 2, +\Delta / 2]$.
- **Relación Señal a Ruido de Cuantización (SQNR):**
$$\text{SQNR}_{teorico} \approx 6.02 B + 1.76 \text{ dB}$$

| Bits ($B$) | Niveles ($L$) | Paso $\Delta$ (LSB) | $\text{SQNR}$ Teórico | $\text{SQNR}$ Medido (Promedio) | Calidad Perceptual |
|:---:|:---:|:---:|:---:|:---:|:---|
| **4 bits** | 16 | $133.33\text{ mV}$ | $25.84\text{ dB}$ | $18.5 - 23.2\text{ dB}$ | Distorsión audible severa |
| **8 bits** | 256 | $7.843\text{ mV}$ | $49.92\text{ dB}$ | $40.1 - 46.8\text{ dB}$ | Calidad telefónica / Lo-Fi |
| **16 bits** | 65536 | $30.52\text{ }\mu\text{V}$ | $98.08\text{ dB}$ | $88.4 - 95.1\text{ dB}$ | Alta Fidelidad (CD Estándar) |

---

## 🎼 Investigación de los 5 Géneros Musicales

1. **Clásica - Barroca:**
   - *Obra:* Concierto de Brandeburgo No. 3 en Sol Mayor, BWV 1048 (I. Allegro).
   - *Compositor:* Johann Sebastian Bach (1685–1750).
   - *Instrumentación:* Orquesta de cuerdas barroca (violines, violas, cellos y bajo continuo con clavecín).
2. **Metal (Thrash Metal):**
   - *Obra:* Master of Puppets (1986).
   - *Banda:* Metallica.
   - *Instrumentación:* Doble guitarra eléctrica con distorsión de alta ganancia, bajo punzante y batería de doble bombo rápido.
3. **Salsa Clásica:**
   - *Obra:* El Cantante (1978).
   - *Intérprete:* Héctor Lavoe (Compositor: Rubén Blades, Productor: Willie Colón).
   - *Instrumentación:* Big band latina con trombones, congas, timbales, piano en montuno y bajo sincopado.
4. **Música de Cantina / Despecho / Popular:**
   - *Obra:* Nadie es eterno en el mundo (1989).
   - *Compositor/Intérprete:* Darío Gómez Zapata ("El Rey del Despecho").
   - *Instrumentación:* Requinto puntero campesino, guitarra marcante, maracas y bajo continuo.
5. **Reggaeton (Urbano Latino):**
   - *Obra:* Gasolina (2004).
   - *Intérprete:* Daddy Yankee (Productores: Luny Tunes).
   - *Instrumentación:* Síntesis digital con sub-graves TR-808, caja sincopada Dembow ($3:3:2$) y sintetizadores digitales.

---

## 🎛️ Separación de Pistas por DSP (Stems)

El script `separador_audio.py` aplica filtros digitales tipo Butterworth IIR implementados con funciones `sosfiltfilt` de fase cero (zero-phase filtering) para evitar distorsiones temporales:
- **Pista 1: Voz Principal:** Filtro pasa-banda con realce de formantes ($250\text{ Hz} - 4000\text{ Hz}$) con supresión de sub-graves.
- **Pista 2: Bajos y Bombos:** Filtro pasa-bajas de 4to orden ($20\text{ Hz} - 250\text{ Hz}$) para aislar líneas de bajo y transitorios de percusión baja.
- **Pista 3: Instrumentos Medios:** Filtro pasa-banda ($400\text{ Hz} - 4500\text{ Hz}$) para cuerdas, vientos, guitarras y teclados.
- **Pista 4: Percusión y Agudos:** Filtro pasa-altas de 4to orden ($4000\text{ Hz} - 20000\text{ Hz}$) para platillos, charles y armónicos brillantes.

---

## 🧠 Diagnóstico y Análisis Neuroacústico para TDAH

El sistema integra un módulo de evaluación neuropsicoacústica (`evaluador_cerebro.py`) para cuantificar el impacto sobre el sistema dopaminérgico y los patrones de ondas cerebrales en personas con **Trastorno por Déficit de Atención e Hiperactividad (TDAH)**:

### 🏆 Género Recomendado: **Clásica - Barroca (J.S. Bach)**
- **Fundamento Neurocientífico:**
  1. **Estimulación de Ondas Alfa ($8-12\text{ Hz}$) y Beta ($13-30\text{ Hz}$):** Promueve la sincronización interhemisférica en la corteza prefrontal dorsolateral, reduciendo el ratio Theta/Beta elevado típico del TDAH.
  2. **Estructura Matemática y Predecible:** La regularidad rítmica barroca (60 a 90 bpm) no satura el bucle fonológico de la memoria de trabajo.
  3. **Ausencia de Letra:** Evita la competencia lingüística en los centros de Broca y Wernicke.

### ⚠️ Géneros Contraindicados para TDAH:
- **Metal:** Los transitorios aperiódicos de alta ganancia y la distorsión elevan el cortisol y desencadenan respuestas de sobrecarga sensorial o fatiga atencional.
- **Reggaeton:** La percusión Dembow a $95\text{ bpm}$ y el refuerzo de sub-graves a $50-60\text{ Hz}$ estimulan la liberación rápida de dopamina fásica, incrementando la inquietud psicomotriz e impulsividad.
- **Salsa y Cantina:** Las letras prominentes y los patrones rítmicos polirrítmicos/sincopados obligan al cerebro a bifurcar la atención, dificultando el mantenimiento del foco atencional sostenido.

---

## 📄 Documentación Formal

Para consultar el desarrollo matemático detallado, deducciones completas de Nyquist-Shannon, fórmulas de SQNR, tablas comparativas y análisis formal, consulte:
- [INFORME_TEORICO_DSP.md](INFORME_TEORICO_DSP.md)

---

## 👨‍💻 Autor y Créditos
- **Estudiante:** Harold Ordóñez ([@hordonez4328](https://github.com/hordonez4328))
- **Materia:** Comunicaciones 1
- **Facultad de Ingeniería Electrónica y Telecomunicaciones**
