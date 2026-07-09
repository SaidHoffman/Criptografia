# Portafolio de Criptografía — Said Hoffman

Este repositorio contiene una selección curada de prácticas y proyectos académicos sobre criptografía realizados durante el curso. Está preparado para mostrarse como evidencia técnica en un perfil profesional de ciberseguridad.

## Qué encontrarás aquí

- Implementaciones prácticas de algoritmos clásicos y modernos (AES, RSA, ECDH/ECDSA).
- Ejercicios y utilidades en Python y Java con documentación y reportes (PDF/DOCX).
- Código organizado por práctica y con ejemplos ejecutables cuando es posible.

## Estructura resumida

- `01-Practicas`: Código y documentación de las prácticas agrupadas por tema.
	- `PracticasCurso/`: copia saneada de la carpeta original `Practicas/` (ver nota de seguridad).
- `02-Documentacion`: apuntes y materiales relevantes (resúmenes, guías).
- `03-Recursos`: bibliografía y archivos auxiliares (no sensibles).

## Requisitos (Python)

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Las pruebas gráficas requieren `PyQt6` y `pycryptodome`; las utilidades matemáticas usan `numpy` y `sympy`.

## Cómo usar (ejemplos rápidos)

- Ejecutar la calculadora modular (interfaz PyQt):

```bash
python 05-Matematicas-y-Utilidades/CalculadoraDeMatrices.py
```

- Ejecutar ejemplo AES (línea de comandos / UI según el archivo):

```bash
python 02-Cifrado-Simetrico/AES.py
```

## Material importado desde `Practicas/`

He añadido una copia saneada de la carpeta original `Practicas/` dentro de:

- `01-Practicas/PracticasCurso/`

Contenido incluido (selección relevante):
- Códigos de las prácticas (`*.py`) organizados por práctica.
- Documentos y reportes (`*.pdf`, `*.docx`) con la explicación de cada ejercicio.
- Archivos públicos de ejemplo (por ejemplo, llaves públicas en `*.txt`).

Qué se excluyó o limpió antes de copiar:
- Archivos de llave privada y secretos (`*.pem`, `*private*`, `secretocompartido.key`, `derivacionclave.key`, etc.) fueron eliminados para evitar subir material sensible.
- Archivos binarios muy grandes (>100 MB) fueron eliminados para mantener el repositorio GitHub-friendly.

Si necesitas que incluya o excluya algo más específico dentro de `Practicas/`, dime exactamente qué carpetas o tipos de archivos deseas mantener y lo ajusto.

## Nota de seguridad

Antes de publicar, verifica que no queden credenciales o material sensible. Yo ya eliminé llaves privadas conocidas, pero la verificación final la haces tú.

## Licencia y atribuciones

El material es principalmente trabajo académico. Si quieres que añada una licencia explícita (por ejemplo MIT), dímelo y la incorporo.

---

Si todo está bien, procedo a subirlo al repositorio remoto que me indicaste.

## Material adicional importado desde `Practicas/`

He añadido una copia saneada de la carpeta original `Practicas/` dentro de:

- `01-Practicas/PracticasCurso/`

Contenido incluido (selección relevante):
- Códigos de las prácticas (`*.py`) organizados por práctica.
- Documentos y reportes (`*.pdf`, `*.docx`) con la explicación de cada ejercicio.
- Archivos públicos de ejemplo (p. ej. llaves públicas en `*.txt`).

Qué se excluyó o limpió antes de copiar:
- Archivos de llave privada y secretos (`*.pem`, `*private*`, `secretocompartido.key`, `derivacionclave.key`, etc.) fueron eliminados para evitar subir material sensible.
- Archivos binarios muy grandes (>100 MB) fueron eliminados para mantener el repositorio GitHub-friendly.

Si quieres que incluya o excluya algo más específico dentro de `Practicas/`, dime exactamente qué carpetas o tipos de archivos deseas mantener y lo ajusto.
