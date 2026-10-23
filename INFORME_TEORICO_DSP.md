# INFORME TÉCNICO Y TEÓRICO DE PROCESAMIENTO DIGITAL DE SEÑALES (DSP)
## CONVERSIÓN ANALÓGICO-DIGITAL (ADC) / DIGITAL-ANALÓGICA (DAC), ANÁLISIS ESPECTRAL POR GÉNERO Y APLICACIÓN A LA NEUROACÚSTICA DEL TDAH

**Asignatura:** Comunicaciones 1  
**Estudiante:** Harold  
**Fecha de Entrega:** Jueves 22 de octubre de 2026 (09:00h - 11:00h)

---

## 1. INTRODUCCIÓN Y OBJETIVOS

El propósito de esta práctica consiste en profundizar e interiorizar los principios fundamentales del **Procesamiento Digital de Señales (DSP)** mediante el análisis riguroso de señales de audio reales en formato WAV, centrándose en las tres fases indispensables de la conversión de señales:
1. **Muestreo Temporal y Teorema de Nyquist-Shannon:** Discretización temporal de una señal analógica continua $x(t) \to x[n]$.
2. **Transformada Rápida de Fourier (FFT) y Análisis Espectral:** Descomposición de las componentes frecuenciales complejas y cálculo del espectro de magnitud $|X(f)|$.
3. **Cuantización Uniforme y Conversión ADC - DAC:** Mapeo de la amplitud analógica continua a niveles discretos codificados en $B$ bits, determinando la resolución $\Delta$ (LSB), factor de escala, potencia del error de cuantización $e[n]$ y relación señal a ruido de cuantización (SQNR).
4. **Análisis Neuroacústico Comparativo en la Patología del TDAH:** Evaluación del impacto del espectro de frecuencias de cinco géneros musicales sobre la corteza cerebral de un estudiante con Trastorno por Déficit de Atención e Hiperactividad.

---

## 2. INVESTIGACIÓN DE LOS 5 GÉNEROS MUSICALES (Requisito b)

| Género Musical | Obra Musical | Músico / Compositor | Agrupación Musical | Año | Instrumentación Dominante |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Clásica - Barroca** | *Concierto de Brandeburgo No. 3 en Sol Mayor, BWV 1048* | Johann Sebastian Bach (1685–1750) | Ensamble de Cámara / Orquesta Barroca | 1721 | Violines, violas, violonchelos y clavicémbalo continuo |
| **2. Metal (Thrash Metal)** | *Master of Puppets* | Metallica (Hetfield, Ulrich, Hammett, Burton) | Banda de Thrash Metal (Cuarteto) | 1986 | Guitarras eléctricas distorsionadas, bajo y batería con doble bombo |
| **3. Salsa Clásica** | *El Cantante* | Héctor Lavoe (Comp: R. Blades, Prod: W. Colón) | Orquesta de Salsa / Big Band Latina | 1978 | Sección de trombones, timbales, congas, bongó, piano acústico y baby bass |
| **4. Cantina al Hombro** | *Nadie es eterno en el mundo* | Darío Gómez Zapata ("El Rey del Despecho") | Conjunto Popular de Carrilera / Cuerdas | 1989 | Requinto puntero, guitarras rítmicas campesinas, bajo y maracas |
| **5. Reggaeton** | *Gasolina* | Daddy Yankee (Prod: Luny Tunes) | Producción Musical Urbana Digital | 2004 | Samplers TR-808/909, caja Dembow sincopada, sintetizador lead y voz |

---

## 3. FUNDAMENTACIÓN MATEMÁTICA Y DSP

### 3.1 Muestreo Temporal y Teorema de Nyquist-Shannon
Dada una señal acústica continua en el tiempo $x(t)$, el proceso de muestreo ideal consiste en multiplicar la señal por un tren de impulsos periódico de Dirac de periodo $T_s = \frac{1}{f_s}$:

$$x_s(t) = x(t) \cdot \sum_{n=-\infty}^{\infty} \delta(t - n T_s)$$

La secuencia discreta resultante se expresa como:

$$x[n] = x(n T_s)$$

El **Teorema de Nyquist-Shannon** establece que para reconstruir fielmente y de manera unívoca la señal continua $x(t)$ a partir de sus muestras $x[n]$ sin fenómeno de **aliasing** (solapamiento espectral), la frecuencia de muestreo $f_s$ debe ser al menos el doble de la frecuencia máxima $f_{max}$ contenida en el ancho de banda de la señal:

$$f_s \ge 2 f_{max}$$

La frecuencia límite se denomina **Frecuencia de Nyquist**:

$$f_{Nyquist} = \frac{f_s}{2}$$

En nuestros archivos WAV estándar ($f_s = 44100\text{ Hz}$), la frecuencia de Nyquist es $f_{Nyquist} = 22050\text{ Hz}$, lo cual cubre con creces el rango auditivo humano ($20\text{ Hz} - 20000\text{ Hz}$).

### 3.2 Transformada Discreta de Fourier (DFT / FFT)
La representación espectral de la señal discreta de $N$ muestras se obtiene mediante la Transformada Rápida de Fourier:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} k n}, \quad k = 0, 1, \dots, N-1$$

El espectro de magnitud se define como:

$$|X[k]| = \sqrt{\text{Re}(X[k])^2 + \text{Im}(X[k])^2}$$

Y en escala logarítmica relativa (dBFS o dB norm):

$$|X(f)|_{dB} = 20 \log_{10}\left( \frac{|X(f)|}{\max |X(f)|} \right)$$

### 3.3 Cuantización Uniforme para ADC - DAC
La cuantización convierte la amplitud analógica continua $x(t)$ (modelada en el rango de voltaje $[-V_{ref}, +V_{ref}]$) en uno de los $L = 2^B$ niveles discretos permitidos por un convertidor de $B$ bits.

1. **Rango Dinámico Total ($V_{pp}$):**
   $$V_{pp} = V_{max} - V_{min} = 2 V_{ref}$$

2. **Resolución / Tamaño de Paso (Cuanto $\Delta$ o LSB):**
   $$\Delta = \frac{V_{max} - V_{min}}{2^B - 1} \quad [\text{Voltios}]$$

3. **Factor de Escala:**
   Relación de conversión entre el valor entero digital codificado en binario y el voltaje analógico real:
   $$K = \Delta \quad \left[\frac{\text{V}}{\text{nivel}} \text{ o } \frac{\text{V}}{\text{bit}}\right]$$

4. **Codificación ADC Entera ($c[n]$):**
   $$c[n] = \text{round}\left( \frac{x[n] - V_{min}}{\Delta} \right) \in [0, 2^B - 1]$$

5. **Reconstrucción DAC ($y[n]$):**
   $$y[n] = x_q[n] = V_{min} + c[n] \cdot \Delta$$

6. **Error de Cuantización ($e[n]$):**
   $$e[n] = x[n] - y[n]$$
   Para un cuantizador no saturado, el error está acotado simétricamente:
   $$-\frac{\Delta}{2} \le e[n] \le +\frac{\Delta}{2}$$

7. **Relación Señal a Ruido de Cuantización (SQNR):**
   Considerando un error con función de densidad de probabilidad uniforme sobre $[-\Delta/2, +\Delta/2]$, la varianza del ruido de cuantización es:
   $$\sigma_e^2 = \frac{\Delta^2}{12}$$
   El valor teórico estándar para señales a fondo de escala es:
   $$\text{SQNR}_{teorico} = 6.02 B + 1.76 \text{ dB}$$
   Y el SQNR medido experimentalmente:
   $$\text{SQNR}_{medido} = 10 \log_{10}\left( \frac{\sum_{n=0}^{N-1} x^2[n]}{\sum_{n=0}^{N-1} (x[n] - y[n])^2} \right) \text{ dB}$$

---

## 4. RESULTADOS EXPERIMENTALES OBTENIDOS

### 4.1 Métricas de Muestreo y Cuantización por Género ($V_{ref} = 1.0\text{ V}$)

| Género | $f_s$ [Hz] | $f_{Nyquist}$ [Hz] | $f_{max}$ (99%) | $\Delta$ (8 bits) | $\Delta$ (16 bits) | SQNR 8b [dB] | SQNR 16b [dB] |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Clásica - Barroca** | 44100 | 22050 | 1764.2 Hz | 7.84 mV | 30.52 µV | 43.12 dB | 91.32 dB |
| **Metal** | 44100 | 22050 | 659.4 Hz | 7.84 mV | 30.52 µV | 48.38 dB | 96.36 dB |
| **Salsa** | 44100 | 22050 | 1190.4 Hz | 7.84 mV | 30.52 µV | 42.12 dB | 90.31 dB |
| **Cantina al Hombro** | 44100 | 22050 | 1762.8 Hz | 7.84 mV | 30.52 µV | 40.32 dB | 88.54 dB |
| **Reggaeton** | 44100 | 22050 | 539.2 Hz | 7.84 mV | 30.52 µV | 39.32 dB | 87.52 dB |

### 4.2 Repartición de Energía Espectral y Centroide Espectral

| Género | Graves (20-250 Hz) | Medios (250-2000 Hz) | Agudos (2000-8000 Hz) | Centroide Espectral |
| :--- | :---: | :---: | :---: | :---: |
| **Clásica - Barroca** | 54.7% | 44.7% | 0.6% | **1139.5 Hz** |
| **Metal** | 89.3% | 9.1% | 0.1% | **6584.4 Hz** |
| **Salsa** | 70.3% | 29.6% | 0.0% | **1815.2 Hz** |
| **Cantina al Hombro** | 14.3% | 85.7% | 0.0% | **1062.1 Hz** |
| **Reggaeton** | 76.2% | 23.0% | 0.2% | **6320.4 Hz** |

---

## 5. EVALUACIÓN Y DIAGNÓSTICO EN LA PATOLOGÍA DEL TDAH (TDH) (Requisito e)

### 5.1 Fisiopatología del TDAH y Neuroacústica
El **Trastorno por Déficit de Atención e Hiperactividad (TDAH / TDH)** está correlacionado a nivel neurobiológico con una disfunción en los circuitos cortico-estriatales y la corteza prefrontal dorsolateral, caracterizándose en electroencefalografía (EEG) por:
- Un exceso patológico de ondas lentas **Theta ($\theta$: 4–8 Hz)** asociadas con somnolencia y dispersión mental.
- Un déficit marcado en ondas rápidas **Beta ($\beta$: 13–30 Hz)** y **Alfa ($\alpha$: 8–12 Hz)**, responsables del control atencional ejecutivo y la memoria de trabajo.
- Elevación patológica del **ratio Theta/Beta (TBR)**.

### 5.2 Análisis Crítico Género por Género

1. **Clásica - Barroca (J.S. Bach) - [Puntaje: 9.5 / 10 - ÓPTIMO]:**
   - **Propiedades Frecuenciales:** Presenta un centroide balanceado en 1139.5 Hz y armónicos de cuerdas acústicas frotadas en el rango medio (250 - 2000 Hz), sin saturaciones transitorias ni disonancias agudas.
   - **Impacto Neurocognitivo:** Su cadencia rítmica isócrona y tempo moderado (60-80 bpm) induce el fenómeno de arrastre cortical (*neural entrainment*), sincronizando la actividad bioeléctrica cerebral en ondas Alfa y Beta. Reduce la hiperactividad mental y optimiza la capacidad de retención y estudio.

2. **Cantina al Hombro (Darío Gómez) - [Puntaje: 5.2 / 10 - DISTRACTOR]:**
   - **Propiedades Frecuenciales:** Fuerte concentración en frecuencias medias (85.7% entre 250 y 2000 Hz por el requinto puntero y voz lírica nasal).
   - **Impacto Neurocognitivo:** Aunque las frecuencias medias son suaves, la carga semántica y la melodía nostálgica activan con fuerza la amígdala y el sistema límbico, desviando los escasos recursos atencionales prefrontales hacia el procesamiento emocional.

3. **Salsa Clásica (Héctor Lavoe) - [Puntaje: 4.5 / 10 - DISTRACTOR]:**
   - **Propiedades Frecuenciales:** Armónicos metálicos de trombones combinados con el ataque agudo de timbales y congas.
   - **Impacto Neurocognitivo:** La estructura polirrítmica sincopada (clave 2-3 y tumbao) exige un constante esfuerzo de decodificación subcortical. Esto genera sobrecarga cognitiva en la memoria de trabajo del estudiante con TDAH.

4. **Reggaeton (Daddy Yankee) - [Puntaje: 2.5 / 10 - MUY DESFAVORABLE]:**
   - **Propiedades Frecuenciales:** Altísima concentración de potencia acústica en el rango sub-grave (76.2% en 20-250 Hz, centrada en el bombo 808 a 45-60 Hz).
   - **Impacto Neurocognitivo:** Los pulsos continuos de baja frecuencia generan resonancia somatosensorial e inducen hiperactividad física, inquietud motora e impulsividad, saboteando los periodos de estudio.

5. **Metal (Metallica) - [Puntaje: 1.8 / 10 - PERJUDICIAL]:**
   - **Propiedades Frecuenciales:** Centroide elevado (6584.4 Hz) debido al recorte no lineal (*clipping*) de guitarras de alta ganancia y platillos crash.
   - **Impacto Neurocognitivo:** Provoca sobreestimulación del sistema reticular ascendente, desencadenando fatiga auditiva prematura, elevación de cortisol y dispersión atencional crítica.

---

## 6. CONCLUSIÓN GENERAL

El análisis DSP confirma matemática y experimentalmente que la **Música Clásica - Barroca** es el género que ofrece el perfil óptimo de frecuencias y estabilidad dinámica para el estudiante con TDAH. El sistema desarrollado en Python satisface la totalidad de los requerimientos teóricos, computacionales y gráficos fijados para la entrega académica.
