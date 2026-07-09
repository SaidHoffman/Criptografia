import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature
)
from cryptography.hazmat.backends import default_backend

def generar_llaves():
    print("\n=== GENERAR LLAVES ECDSA ===")
    print("Seleccione la curva ECDSA que desea utilizar:")
    print("1) NIST P-256")
    print("2) NIST P-384")
    print("3) NIST P-521")
    opcion = input("Opción: ")

    if opcion == '1':
        curva = ec.SECP256R1()
    elif opcion == '2':
        curva = ec.SECP384R1()
    elif opcion == '3':
        curva = ec.SECP521R1()
    else:
        print("Opción no válida. Se utilizará SECP256R1 por defecto.")
        curva = ec.SECP256R1()

    private_key = ec.generate_private_key(curva, default_backend())
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("privB.pem", 'wb') as f:
        f.write(private_pem)

    public_pem_b64 = base64.b64encode(public_pem)
    with open("pubB.key", 'wb') as f:
        f.write(public_pem_b64)

    print(f"\nPar de llaves ECDSA generado con la curva {curva.name}.")
    print("Archivos creados:")
    print("  - privB.pem (llave privada)")
    print("  - pubB.key  (llave pública codificada en Base64)\n")

def firmar_archivo():
    print("\n=== FIRMAR ARCHIVO (solo r y s en signB.key) ===")

    if not os.path.exists("privB.pem"):
        print("ERROR: No se encontró privB.pem. Primero genera tus llaves (opción 1).")
        return

    with open("privB.pem", 'rb') as f:
        private_pem = f.read()

    private_key = serialization.load_pem_private_key( #deserializar la llave privada 
        private_pem,
        password=None,
        backend=default_backend()
    )

    archivo_nombre = input("Ingrese el nombre del archivo a firmar: ")

    if not os.path.exists(archivo_nombre):
        print(f"ERROR: No se encontró el archivo '{archivo_nombre}'.")
        return

    with open(archivo_nombre, 'rb') as f:
        contenido_bytes = f.read()

    firma_bin = private_key.sign(
        contenido_bytes,
        ec.ECDSA(hashes.SHA256())
    )

    r, s = decode_dss_signature(firma_bin)

    with open("signB.key", 'w') as f:
        f.write(str(r) + "\n")
        f.write(str(s) + "\n")

    print("\nFirma creada exitosamente en 'signB.key':")
    print("  - Línea 1: r como entero")
    print("  - Línea 2: s como entero\n")
    print("Recuerda enviar también el archivo original junto con 'signB.key'.\n")

def verificar_firma():
    print("\n=== VERIFICAR FIRMA DE ARCHIVO ===")

    if not os.path.exists("pubB.key"):
        print("ERROR: No se encontró pubB.key. Primero genera las llaves (opción 1).")
        return

    with open("pubB.key", 'rb') as f:
        public_pem_b64 = f.read()

    try:
        public_pem = base64.b64decode(public_pem_b64)
    except Exception:
        print("ERROR: No se pudo decodificar base64 en 'pubB.key'.")
        return

    public_key = serialization.load_pem_public_key(
        public_pem,
        backend=default_backend()
    )

    if not os.path.exists("signB.key"):
        print("ERROR: No se encontró signB.key. Primero firma un archivo (opción 2).")
        return

    with open("signB.key", 'r') as f:
        lines = f.read().splitlines()

    if len(lines) < 2:
        print("ERROR: 'signB.key' no contiene 2 líneas. Formato inválido.")
        return

    try:
        r = int(lines[0])
        s = int(lines[1])
    except Exception:
        print("ERROR: No se pudo convertir r o s a enteros.")
        return

    archivo_nombre = input("Ingrese el nombre del archivo a verificar: ")

    if not os.path.exists(archivo_nombre):
        print(f"ERROR: No se encontró el archivo '{archivo_nombre}'.")
        return

    with open(archivo_nombre, 'rb') as f:
        contenido_bytes = f.read()

    firma_bin = encode_dss_signature(r, s)

    try:
        public_key.verify(
            firma_bin,
            contenido_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        print("La firma ES válida (True).")
    except Exception:
        print("La firma NO es válida (False).")

def main():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Generar llaves (privB.pem / pubB.key)")
        print("2) Firmar un archivo -> signB.key (r y s)")
        print("3) Verificar firma de un archivo")
        print("4) Salir")

        opcion = input("Seleccione una opción (1-4): ")

        if opcion == '1':
            generar_llaves()
        elif opcion == '2':
            firmar_archivo()
        elif opcion == '3':
            verificar_firma()
        elif opcion == '4':
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
