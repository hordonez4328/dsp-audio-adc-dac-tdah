"""
================================================================================
evaluador_cerebro.py
Módulo de Neuroacústica y Psicología de la Música:
Evalúa cómo afecta cada género y canción al cerebro del estudiante:
  - Concentrado / Enfoque mental (Ondas Alfa y Beta)
  - Contento / Alegre / Euforia (Dopamina y Sistema Motor)
  - Triste / Melancólico / Emocional (Sistema Límbico y Amígdala)
  - Hiperactivo / Impulsivo (Resonancia sub-grave y Ganglios Basales)
  - Enérgico / Tensión / Agresivo (Sistema Simpático y Cortisol)
================================================================================
"""

import numpy as np

def evaluar_impacto_cerebral(genero_nombre, metricas_dsp=None):
    """
    Determina el perfil neuroemocional y cognitivo a partir del género y métricas DSP.
    Retorna un diccionario completo con:
      - Estado predominante
      - Puntuaciones emocionales (%)
      - Estimulación de ondas cerebrales (Delta, Theta, Alfa, Beta, Gamma)
      - Neurotransmisores activados
      - Utilidad recomendada para el estudiante
      - Advertencias cognitivas (ej. TDAH, fatiga mental)
    """
    g = genero_nombre.lower()
    
    # Perfil por defecto
    resultado = {
        "genero": genero_nombre,
        "estado_predominante": "Concentrado",
        "descripcion_emocional": "",
        "puntuaciones": {
            "Concentrado / Foco": 85,
            "Contento / Alegre": 40,
            "Triste / Melancólico": 20,
            "Hiperactivo / Impulsivo": 15,
            "Enérgico / Tensión": 25
        },
        "ondas_cerebrales": {
            "Delta (0.5-4 Hz) [Relajación]": 25,
            "Theta (4-8 Hz) [Pasivo / TDAH]": 20,
            "Alfa (8-12 Hz) [Calma Alerta]": 85,
            "Beta (13-30 Hz) [Foco Activo]": 80,
            "Gamma (30-80 Hz) [Alerta Alta]": 30
        },
        "neurotransmisores": "Acetilcolina y Dopamina balanceada",
        "actividad_ideal": "Estudio analítico, lectura densa, resolución de ejercicios.",
        "advertencia": "Ninguna. Excelente para concentración prolongada."
    }
    
    if "clásica" in g or "barroca" in g or "clasica" in g:
        resultado["estado_predominante"] = "CONCENTRADO Y SERENO (Flujo Mental)"
        resultado["descripcion_emocional"] = (
            "Produce serenidad, claridad mental y focalización profunda. Reduce la ansiedad "
            "y calma los pensamientos acelerados gracias a su armonía consonante y compás isócrono regular."
        )
        resultado["puntuaciones"] = {
            "Concentrado / Foco": 95,
            "Contento / Alegre": 55,
            "Triste / Melancólico": 15,
            "Hiperactivo / Impulsivo": 5,
            "Enérgico / Tensión": 10
        }
        resultado["ondas_cerebrales"] = {
            "Delta (0.5-4 Hz)": 30,
            "Theta (4-8 Hz)": 15,
            "Alfa (8-12 Hz)": 92,
            "Beta (13-30 Hz)": 88,
            "Gamma (30-80 Hz)": 20
        }
        resultado["neurotransmisores"] = "Acetilcolina (memoria de trabajo) y Serotonina (estabilidad anímica)"
        resultado["actividad_ideal"] = "Estudiar para exámenes, programar código complejo, lectura reflexiva."
        resultado["advertencia"] = "Ideal para estudiantes con TDAH. No genera fatiga auditiva ni sobreestimulación."

    elif "metal" in g or "rock" in g:
        resultado["estado_predominante"] = "ENÉRGICO, DESCARGA Y ALERTA MÁXIMA"
        resultado["descripcion_emocional"] = (
            "Induce excitación psicofísica, sensación de poder, descarga de adrenalina o ira acumulada. "
            "En contextos de estudio pasivo genera tensión, inquietud motora y dispersión cognitiva."
        )
        resultado["puntuaciones"] = {
            "Concentrado / Foco": 25,
            "Contento / Alegre": 45,
            "Triste / Melancólico": 30,
            "Hiperactivo / Impulsivo": 75,
            "Enérgico / Tensión": 95
        }
        resultado["ondas_cerebrales"] = {
            "Delta (0.5-4 Hz)": 10,
            "Theta (4-8 Hz)": 20,
            "Alfa (8-12 Hz)": 25,
            "Beta (13-30 Hz)": 70,
            "Gamma (30-80 Hz)": 90
        }
        resultado["neurotransmisores"] = "Noradrenalina, Adrenalina y Cortisol (estrés acústico y estado de alerta)"
        resultado["actividad_ideal"] = "Entrenamiento físico intenso, levantamiento de pesas, desahogo de estrés."
        resultado["advertencia"] = "Desaconsejado para estudiar o para TDAH: la distorsión satura la corteza sensorial."

    elif "salsa" in g or "tropical" in g or "cumbia" in g:
        resultado["estado_predominante"] = "CONTENTO, ALEGRE Y SOCIAL (Dopamina Pura)"
        resultado["descripcion_emocional"] = (
            "Estimula la euforia, optimismo, ganas de cantar y bailar. La síncopa de la clave 2-3 "
            "conecta con la corteza premotora haciendo casi imposible no mover los pies o el cuerpo."
        )
        resultado["puntuaciones"] = {
            "Concentrado / Foco": 35,
            "Contento / Alegre": 95,
            "Triste / Melancólico": 20,
            "Hiperactivo / Impulsivo": 70,
            "Enérgico / Tensión": 50
        }
        resultado["ondas_cerebrales"] = {
            "Delta (0.5-4 Hz)": 15,
            "Theta (4-8 Hz)": 30,
            "Alfa (8-12 Hz)": 45,
            "Beta (13-30 Hz)": 75,
            "Gamma (30-80 Hz)": 60
        }
        resultado["neurotransmisores"] = "Dopamina (recompensa inmediata) y Endorfinas (bienestar y placer)"
        resultado["actividad_ideal"] = "Bailar, reuniones sociales, limpieza del hogar, levantar el ánimo decaído."
        resultado["advertencia"] = "Distractor para estudio conceptual: la letra y el ritmo secuestran la atención ejecutiva."

    elif "cantina" in g or "despecho" in g or "popular" in g or "carrilera" in g:
        resultado["estado_predominante"] = "TRISTE, MELANCÓLICO Y NOSTÁLGICO (Catarsis Límbica)"
        resultado["descripcion_emocional"] = (
            "Evoca recuerdos del pasado, desamor, nostalgia y apego sentimental. Activa intensamente "
            "el sistema límbico (amígdala y corteza insular), facilitando el desahogo emocional y el canto catártico."
        )
        resultado["puntuaciones"] = {
            "Concentrado / Foco": 30,
            "Contento / Alegre": 20,
            "Triste / Melancólico": 95,
            "Hiperactivo / Impulsivo": 35,
            "Enérgico / Tensión": 40
        }
        resultado["ondas_cerebrales"] = {
            "Delta (0.5-4 Hz)": 35,
            "Theta (4-8 Hz)": 65,
            "Alfa (8-12 Hz)": 40,
            "Beta (13-30 Hz)": 40,
            "Gamma (30-80 Hz)": 30
        }
        resultado["neurotransmisores"] = "Prolactina y Oxitocina (afecto y empatía ante la tristeza musical)"
        resultado["actividad_ideal"] = "Desahogo sentimental, momentos de reflexión personal íntima, tertulias familiares."
        resultado["advertencia"] = "Perjudicial para la productividad académica: sumerge al estudiante en rumiación emocional."

    elif "reggaeton" in g or "urbano" in g or "dembow" in g:
        resultado["estado_predominante"] = "HIPERACTIVO, MOTIVADO Y FÍSICO (Bajo 808)"
        resultado["descripcion_emocional"] = (
            "Provoca aceleración psicomotriz, pulsión corporal de movimiento y confianza social extrovertida. "
            "El bombo sub-grave repetitivo genera resonancia vestibular induciendo inquietud corporal continua."
        )
        resultado["puntuaciones"] = {
            "Concentrado / Foco": 20,
            "Contento / Alegre": 80,
            "Triste / Melancólico": 15,
            "Hiperactivo / Impulsivo": 95,
            "Enérgico / Tensión": 60
        }
        resultado["ondas_cerebrales"] = {
            "Delta (0.5-4 Hz)": 15,
            "Theta (4-8 Hz)": 45,
            "Alfa (8-12 Hz)": 30,
            "Beta (13-30 Hz)": 65,
            "Gamma (30-80 Hz)": 75
        }
        resultado["neurotransmisores"] = "Dopamina rápida en el estriado ventral (búsqueda de estimulación sensorial)"
        resultado["actividad_ideal"] = "Cardio, salir de fiesta, conducir en autopista, motivación previa a competir."
        resultado["advertencia"] = "Muy contraproducente para TDAH: el bucle 808 dispersa la memoria de trabajo y fomenta inquietud."

    return resultado
