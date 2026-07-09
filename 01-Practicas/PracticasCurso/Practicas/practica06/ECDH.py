import os
import base64
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def listar_archivos(exclude_ext=None):
    """
    Lista todos los archivos en el directorio actual que NO terminen con alguna de las extensiones
    indicadas en exclude_ext (opcional).
    Devuelve la lista de esos archivos.
    """
    if exclude_ext is None:
        exclude_ext = []
    files = [f for f in os.listdir('.') 
             if os.path.isfile(f) and not any(f.endswith(ext) for ext in exclude_ext)]
    if files:
        print("\nArchivos en el directorio actual:")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}) {file}")
    else:
        print("No se encontraron archivos en el directorio actual.")
    return files

def listar_archivos_con_extension(extension):
    """
    Lista todos los archivos del directorio actual que terminen con la extensión indicada.
    Devuelve la lista de esos archivos.
    """
    files = [f for f in os.listdir('.') 
             if os.path.isfile(f) and f.endswith(extension)]
    if files:
        print(f"\nArchivos con extensión '{extension}' en el directorio actual:")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}) {file}")
    else:
        print(f"No se encontraron archivos con extensión '{extension}'.")
    return files

def seleccionar_archivo_de_lista(archivos):
    """
    Recibe una lista de 'archivos' y permite al usuario elegir uno por índice.
    Devuelve el nombre seleccionado o None si no es válido.
    """
    if not archivos:
        return None
    try:
        indice = int(input("\nElige el número del archivo que deseas usar: ").strip())
        if 1 <= indice <= len(archivos):
            return archivos[indice - 1]
        else:
            print("Índice fuera de rango.")
            return None
    except ValueError:
        print("Selección inválida (no es un número).")
        return None

########################################
# 1. ECDH: GENERAR PAR DE LLAVES
########################################

def seleccionar_curva():
    print("\nSeleccione la curva ECDH que desea usar:")
    print("1) secp224r1 (NIST P-224)")
    print("2) secp256r1 (NIST P-256)")
    print("3) secp384r1 (NIST P-384)")
    print("4) secp521r1 (NIST P-521)")
    opcion = input("Opción: ")
    
    if opcion == '1':
        return ec.SECP224R1()
    elif opcion == '2':
        return ec.SECP256R1()
    elif opcion == '3':
        return ec.SECP384R1()
    elif opcion == '4':
        return ec.SECP521R1()
    else:
        print("Opción no válida. Se usará P-256 por defecto.")
        return ec.SECP256R1()

def generar_par_llaves_priv_pub():
    curva = seleccionar_curva()
    private_key = ec.generate_private_key(curva, default_backend())
    public_key = private_key.public_key()
    
    # Serializar llave privada en PEM (PKCS8)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serializar llave pública en PEM (SubjectPublicKeyInfo)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Guardar en archivos
    with open("ecdh_priv.pem", 'wb') as f:
        f.write(private_pem)
    with open("ecdh_pub.pem", 'wb') as f:
        f.write(public_pem)
    
    print(f"\nPar de llaves ECDH generado y guardado:")
    print(" - ecdh_priv.pem (llave privada, PEM)")
    print(" - ecdh_pub.pem  (llave pública, PEM)")
    print(f"Curva utilizada: {curva.name}\n")

########################################
# 2. MOSTRAR / EXPORTAR LLAVE PÚBLICA EN BASE64
########################################

def mostrar_publica_base64():
    """
    Lee 'ecdh_pub.pem', la codifica en DER y luego la pasa a Base64 para imprimir/guardar.
    El usuario puede compartir esta Base64 con la otra entidad.
    """
    if not os.path.exists("ecdh_pub.pem"):
        print("\nERROR: No existe ecdh_pub.pem. Primero genera tu par de llaves.")
        return
    
    with open("ecdh_pub.pem", 'rb') as f:
        pub_pem = f.read()
    
    # Cargar la llave pública para luego extraer DER
    pub_key = serialization.load_pem_public_key(pub_pem, backend=default_backend())
    pub_der = pub_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    pub_b64 = base64.b64encode(pub_der).decode('utf-8')
    print("\n=== LLAVE PÚBLICA EN BASE64 ===")
    print(pub_b64)
    print("===============================")

    # Opcional: Guardarla en un archivo .txt
    opcion = input("\n¿Deseas guardar esta llave pública Base64 en un archivo? (s/n): ")
    if opcion.lower() == 's':
        nombre_archivo = input("Nombre del archivo (p. ej. 'ecdh_pub_b64.txt'): ").strip()
        if not nombre_archivo:
            nombre_archivo = "ecdh_pub_b64.txt"
        with open(nombre_archivo, 'w') as f:
            f.write(pub_b64)
        print(f"Archivo '{nombre_archivo}' creado con éxito.")

########################################
# 3. ECDH: GENERAR CLAVE COMPARTIDA (LEYENDO LA LLAVE PÚBLICA REMOTA DESDE UN ARCHIVO)
########################################

def ecdh_acordar_llave():
    """
    Lee la llave privada local (ecdh_priv.pem).
    Luego muestra archivos .txt, .key, .b64, etc. para que el usuario elija
    cuál contiene la llave pública remota (en DER Base64).
    """
    if not os.path.exists("ecdh_priv.pem"):
        print("\nERROR: No existe ecdh_priv.pem. Primero genera tu par de llaves.")
        return
    
    with open("ecdh_priv.pem", 'rb') as f:
        priv_pem = f.read()
    private_key = serialization.load_pem_private_key(
        priv_pem,
        password=None,
        backend=default_backend()
    )
    
    print("\nSelecciona el archivo que contenga la llave pública remota (DER en Base64).")
    # Listar archivos que puedan contener la llave (generalmente .txt, .key, .b64)
    archivos = [f for f in os.listdir('.') 
                if os.path.isfile(f) and (f.endswith('.txt') or f.endswith('.key') or f.endswith('.b64'))]
    if not archivos:
        print("No se encontraron archivos que terminen en .txt, .key o .b64.")
        return
    for i, file in enumerate(archivos, 1):
        print(f"{i}) {file}")
    try:
        idx = int(input("Ingresa el número del archivo: ").strip())
        if idx < 1 or idx > len(archivos):
            print("Selección inválida.")
            return
        archivo_remoto = archivos[idx - 1]
    except ValueError:
        print("Selección inválida (no es un número).")
        return

    # Leer contenido de la llave pública remota en Base64
    with open(archivo_remoto, 'r') as fr:
        remote_pub_b64 = fr.read().strip()  # lo que esté en el archivo
    
    # Decodificar Base64
    try:
        remote_pub_der = base64.b64decode(remote_pub_b64)
    except Exception:
        print("ERROR: No se pudo decodificar la Base64. Revisa el contenido del archivo.")
        return

    # Cargar la llave pública DER-
    try:
        remote_public_key = serialization.load_der_public_key(
            remote_pub_der,
            backend=default_backend()
        )
    except Exception:
        print("ERROR: No se pudo cargar la llave pública DER.")
        return
    
    # Generar la clave ECDH (clave compartida)
    shared_key = private_key.exchange(ec.ECDH(), remote_public_key)  # bytes
    
    # Mostrar en Base64
    shared_b64 = base64.b64encode(shared_key).decode('utf-8')
    
    print("\n=== CLAVE ECDH (COMPARTIDA) EN BASE64 ===")
    print(shared_b64)
    print("=========================================")
    
    # Opcional: Guardar en un archivo
    opcion = input("\n¿Deseas guardar esta clave ECDH en un archivo? (s/n): ")
    if opcion.lower() == 's':
        nombre_out = input("Nombre del archivo (p. ej. 'shared_ecdh.key'): ").strip()
        if not nombre_out:
            nombre_out = "shared_ecdh.key"
        with open(nombre_out, 'w') as f:
            f.write(shared_b64)
        print(f"Archivo '{nombre_out}' creado con éxito.")

########################################
# 4. Derivar CLAVE AES 256 USANDO SHA-256 DIRECTO
########################################

def derivar_clave_aes256():
    """
    Permite elegir un archivo que contenga la clave ECDH en Base64,
    luego deriva la clave AES-256 aplicando un SHA-256 directo.
    """
    print("\nSelecciona el archivo que contenga la CLAVE ECDH (Base64) para derivar AES-256:")
    archivos = [f for f in os.listdir('.') 
                if os.path.isfile(f) and (f.endswith('.txt') or f.endswith('.key') or f.endswith('.b64'))]
    if not archivos:
        print("No se encontraron archivos .txt/.key/.b64 para leer la ECDH.")
        return
    for i, file in enumerate(archivos, 1):
        print(f"{i}) {file}")
    
    try:
        idx = int(input("Número del archivo: ").strip())
        if idx < 1 or idx > len(archivos):
            print("Selección inválida.")
            return
        archivo_ecdh = archivos[idx - 1]
    except ValueError:
        print("Selección inválida (no es número).")
        return

    # Leer contenido de la ECDH
    with open(archivo_ecdh, 'r') as fe:
        ecdh_b64 = fe.read().strip()
    
    try:
        ecdh_bytes = base64.b64decode(ecdh_b64)
    except Exception:
        print("ERROR al decodificar Base64 de la clave ECDH.")
        return
    
    # Derivar la clave AES-256 aplicando SHA-256 al shared key directamente:
    aes_key = hashlib.sha256(ecdh_bytes).digest()  # 32 bytes (256 bits)
    
    aes_b64 = base64.b64encode(aes_key).decode('utf-8')
    
    print("\n=== CLAVE DERIVADA (AES-256) EN BASE64 (SHA-256 directo) ===")
    print(aes_b64)
    print("=============================================================")
    
    opcion = input("\n¿Deseas guardar esta clave derivada en un archivo (ej: aes_key.key)? (s/n): ")
    if opcion.lower() == 's':
        nombre_clave = input("Nombre del archivo: ").strip()
        if not nombre_clave:
            nombre_clave = "aes_key.key"
        with open(nombre_clave, 'w') as f:
            f.write(aes_b64)
        print(f"Archivo '{nombre_clave}' creado con éxito.")

########################################
# 5. CIFRAR ARCHIVO USANDO AES-GCM (LEYENDO CLAVE AES DESDE ARCHIVO)
########################################

def cifrar_archivo():
    """
    Pide al usuario que seleccione (1) el archivo que contiene la clave AES-256 en Base64
    y (2) el archivo que se desea cifrar. 
    Luego cifra con AES-GCM y guarda el resultado en un .enc.b64 (por defecto).
    """
    print("\n=== CIFRAR ARCHIVO CON AES-GCM ===")
    
    # 1) Seleccionar archivo con clave AES-256 (Base64)
    print("Selecciona el archivo que contiene la clave AES-256 (Base64):")
    archivos_clave = [f for f in os.listdir('.') 
                      if os.path.isfile(f) and (f.endswith('.txt') or f.endswith('.key') or f.endswith('.b64'))]
    if not archivos_clave:
        print("No se encontraron archivos con la clave AES (en .txt/.key/.b64).")
        return
    for i, file in enumerate(archivos_clave, 1):
        print(f"{i}) {file}")
    try:
        idx_aes = int(input("Número del archivo con la clave: ").strip())
        if idx_aes < 1 or idx_aes > len(archivos_clave):
            print("Selección inválida.")
            return
        archivo_aes = archivos_clave[idx_aes - 1]
    except ValueError:
        print("Selección inválida (no es número).")
        return
    
    # Leer la clave AES
    with open(archivo_aes, 'r') as fa:
        aes_b64 = fa.read().strip()
    try:
        aes_key = base64.b64decode(aes_b64)
    except Exception:
        print("ERROR al decodificar la clave AES en Base64.")
        return
    
    if len(aes_key) != 32:
        print("ERROR: la clave no es de 256 bits.")
        return

    # 2) Seleccionar archivo a cifrar
    print("\nSelecciona el archivo que deseas cifrar:")
    archivos_disp = listar_archivos(exclude_ext=[".pem", ".enc.b64", ".py", ".key"])
    # (Puedes ajustar exclude_ext según quieras)
    
    if not archivos_disp:
        print("No hay archivos disponibles para cifrar.")
        return

    nombre_in = seleccionar_archivo_de_lista(archivos_disp)
    if not nombre_in:
        return
    
    if not os.path.exists(nombre_in):
        print(f"ERROR: el archivo '{nombre_in}' no existe.")
        return
    
    # Leer contenido completo
    with open(nombre_in, 'rb') as f:
        plaintext = f.read()
    
    # Crear AESGCM
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)  # GCM típicamente usa 12 bytes de nonce
    
    # Cifrar
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    
    # Extraer tag (últimos 16 bytes) y separar el cifrado real
    tag = ciphertext[-16:]
    real_cipher = ciphertext[:-16]
    
    # Convertir a Base64 (con padding normal)
    nonce_b64 = base64.b64encode(nonce).decode('utf-8')
    tag_b64 = base64.b64encode(tag).decode('utf-8')
    real_cipher_b64 = base64.b64encode(real_cipher).decode('utf-8')
    
    # Preguntar el nombre del archivo de salida
    nombre_out = input("Nombre del archivo de salida (por defecto 'cifrado.enc.b64'): ").strip()
    if not nombre_out:
        nombre_out = "cifrado.enc.b64"
    
    with open(nombre_out, 'w') as f_out:
        f_out.write(nonce_b64 + "\n")
        f_out.write(tag_b64 + "\n")
        f_out.write(real_cipher_b64 + "\n")
    
    print(f"\nArchivo cifrado creado: {nombre_out}")
    print("Contiene 3 líneas en Base64: nonce, tag, ciphertext.\n")

########################################
# 6. DESCIFRAR ARCHIVO CON AES-GCM (LEYENDO CLAVE AES DESDE ARCHIVO)
########################################

def descifrar_archivo():
    """
    1) Pide al usuario que seleccione el archivo con la clave AES-256 (Base64)
    2) Lista archivos .enc.b64 para descifrar
    3) Reconstruye ciphertext y descifra con AES-GCM
    4) Guarda el plaintext
    """
    print("\n=== DESCIFRAR ARCHIVO CON AES-GCM ===")
    
    # 1) Seleccionar archivo con la clave AES-256
    print("Selecciona el archivo que contiene la clave AES-256 (Base64):")
    archivos_clave = [f for f in os.listdir('.') 
                      if os.path.isfile(f) and (f.endswith('.txt') or f.endswith('.key') or f.endswith('.b64'))]
    if not archivos_clave:
        print("No se encontraron archivos .txt/.key/.b64 para la clave AES.")
        return
    for i, file in enumerate(archivos_clave, 1):
        print(f"{i}) {file}")
    try:
        idx_aes = int(input("Número del archivo con la clave: ").strip())
        if idx_aes < 1 or idx_aes > len(archivos_clave):
            print("Selección inválida.")
            return
        archivo_aes = archivos_clave[idx_aes - 1]
    except ValueError:
        print("Selección inválida (no es número).")
        return
    
    # Leer la clave AES
    with open(archivo_aes, 'r') as fa:
        aes_b64 = fa.read().strip()
    try:
        aes_key = base64.b64decode(aes_b64)
    except Exception:
        print("ERROR al decodificar la clave AES en Base64.")
        return
    if len(aes_key) != 32:
        print("ERROR: la clave no es de 256 bits.")
        return
    
    # 2) Listar archivos con extensión .enc.b64
    archivos_cifrados = listar_archivos_con_extension(".enc.b64")
    if not archivos_cifrados:
        return
    
    nombre_in = seleccionar_archivo_de_lista(archivos_cifrados)
    if not nombre_in:
        return
    
    if not os.path.exists(nombre_in):
        print(f"ERROR: el archivo '{nombre_in}' no existe.")
        return
    
    # Leer las 3 líneas: nonce, tag, ciphertext
    with open(nombre_in, 'r') as f_in:
        lines = f_in.read().splitlines()
    
    if len(lines) < 3:
        print("ERROR: el archivo no tiene el formato correcto (3 líneas).")
        return
    
    nonce_b64, tag_b64, cipher_b64 = lines[0], lines[1], lines[2]
    
    try:
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)
        real_cipher = base64.b64decode(cipher_b64)
    except Exception:
        print("ERROR: No se pudo decodificar Base64 en el archivo cifrado.")
        return
    
    # Reconstruir el ciphertext concatenando: real_cipher + tag
    ciphertext = real_cipher + tag
    
    aesgcm = AESGCM(aes_key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except Exception as e:
        print(f"ERROR al descifrar: {e}")
        return
    
    # Guardar el plaintext
    nombre_out = input("Nombre para el archivo descifrado (ej: 'salida_dec.txt'): ").strip()
    if not nombre_out:
        nombre_out = "salida_dec.txt"
    
    with open(nombre_out, 'wb') as f_dec:
        f_dec.write(plaintext)
    
    print(f"\nArchivo descifrado guardado como: {nombre_out}\n")

########################################
# MENÚ PRINCIPAL
########################################

def main():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Generar par de llaves ECDH (ecdh_priv.pem / ecdh_pub.pem)")
        print("2) Mostrar (o guardar) llave pública local en Base64 (para compartir)")
        print("3) Acordar clave ECDH leyendo la llave pública remota desde un archivo (Base64)")
        print("4) Derivar clave AES-256 (SHA-256 directo) leyendo la clave ECDH desde un archivo (Base64)")
        print("5) Cifrar archivo con AES-GCM (usando clave AES-256 leída de un archivo Base64)")
        print("6) Descifrar archivo con AES-GCM (usando clave AES-256 leída de un archivo Base64)")
        print("7) Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            generar_par_llaves_priv_pub()
        elif opcion == '2':
            mostrar_publica_base64()
        elif opcion == '3':
            ecdh_acordar_llave()
        elif opcion == '4':
            derivar_clave_aes256()
        elif opcion == '5':
            cifrar_archivo()
        elif opcion == '6':
            descifrar_archivo()
        elif opcion == '7':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
