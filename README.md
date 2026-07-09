# Portafolio de Criptografía — Said Hoffman

Este repositorio contiene una selección curada de prácticas y proyectos académicos sobre criptografía. Está pensado para mostrarse en un perfil profesional y demostrar competencias técnicas y prácticas en criptografía aplicada.

## Resumen

- Código, reportes y utilidades en Python y Java.
- Material organizado por práctica y por tema (simétrico, asimétrico, intercambio de claves, matemáticas).
- Copia saneada de la carpeta original `Practicas/` en `01-Practicas/PracticasCurso/` (llaves privadas y archivos muy grandes eliminados).

## Estructura principal

- `01-Practicas`
  - `01-Cifrado-Clasico` — Cifrado monoalfabético (Java).
  - `02-Cifrado-Simetrico` — AES y modos de operación (Python + PyQt UIs).
  - `03-Cifrado-Asimetrico` — RSA y ejemplos de firma.
  - `04-Intercambio-de-Claves` — DH clásico, DIHE, ejemplos ECDH.
  - `05-Matematicas-y-Utilidades` — Calculadora modular y utilidades matemáticas.
  - `PracticasCurso` — copia saneada de `Practicas/` con ejercicios y reportes.

- `02-Documentacion` — apuntes y guías (resúmenes y referencias).
- `03-Recursos` — bibliografía y archivos auxiliares.

---

## Temas cubiertos (detalle técnico)

A continuación se listan los temas principales y dónde encontrar ejemplos y reportes.

### Criptografía simétrica (AES)

- Archivos de referencia:
  - `02-Cifrado-Simetrico/AES.py`
  - `02-Cifrado-Simetrico/AESOperationModes.py`
- Modos implementados y analizados: ECB, CBC, CFB, OFB, CTR.
- Puntos prácticos incluidos:
  - Padding y unpadding para bloques de 128 bits.
  - Preservación de cabeceras BMP cuando procede (para cifrar solo el payload de imagen).
  - Uso de IV y nonce; diferencias entre modos y requisitos de longitud (16 bytes/8 bytes para CTR nonce).
  - Derivación simple de clave desde texto de usuario (comentarios sobre por qué usar KDF en producción).

### Criptografía asimétrica (RSA, ECDSA)

- Archivos de referencia:
  - `03-Cifrado-Asimetrico/practicaRSA.py`
  - Ejercicios ECDSA en `01-Practicas/PracticasCurso/Practica02` y `01-Practicas/PracticasCurso/Practica05`.
- Temas prácticos:
  - Cifrado y descifrado con RSA + PKCS1_OAEP.
  - Firmas con RSA y ECDSA, generación y verificación.
  - Hashing con SHA-256 para firmas y comprobaciones.
  - Discusión sobre tamaños de clave y recomendaciones.

### Intercambio de claves (DH, ECDH, DIHE)

- Archivos de referencia:
  - `04-Intercambio-de-Claves/dh1.py`
  - `04-Intercambio-de-Claves/dihe.py`
  - `01-Practicas/PracticasCurso/practica06/ECDH.py`
- Temas prácticos:
  - DH modular clásico (generación de p y g, validación primalidad).
  - ECDH: generar par de claves, exportar pública en Base64, acordar clave compartida.
  - DIHE: ejercicios del curso sobre parámetros públicos y flujo de intercambio.

### Criptografía clásica y fundamentos

- Archivos de referencia:
  - `01-Cifrado-Clasico/Practica0.java`
  - Ejercicios teóricos en `01-Practicas/PracticasCurso/Practica02` (residuos cuadráticos, curvas toy).
- Temas: cifrados monoalfabéticos, análisis básico, representaciones y transformaciones de texto.

### Matemáticas y utilidades

- `05-Matematicas-y-Utilidades/CalculadoraDeMatrices.py` — operaciones modulares y inversas de matrices.
- Implementaciones de suma de puntos y doble en curvas elípticas en `Practicas/Practica02/SumaDoblado.py`.

---

## Tecnologías y librerías

- Python 3.x (principal).
- PyQt6 (UI para AES y calculadora) — `pip install PyQt6`.
- PyCryptodome — `pip install pycryptodome`.
- cryptography — para algunos ejemplos ECDH (opcional).
- SymPy, NumPy — matemáticas (curvas, determinantes).

Se incluye `requirements.txt` con las dependencias más relevantes.

---

## Cómo ejecutar (ejemplos rápidos)

1) Crear entorno virtual e instalar dependencias:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

2) Ejecutar ejemplos GUI (si tienes entorno gráfico):

```bash
python 02-Cifrado-Simetrico/AES.py
python 05-Matematicas-y-Utilidades/CalculadoraDeMatrices.py
```

3) Ejecutar ejemplos de consola:

```bash
python 01-Practicas/PracticasCurso/practica06/ECDH.py
python 03-Cifrado-Asimetrico/practicaRSA.py
```
