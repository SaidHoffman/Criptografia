import os
from sympy import isprime
import random
import SumaDoblado
import math


def leer_parametros(nombre_archivo):
    parametros = {}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or '=' not in linea:
                continue
            clave, valor = linea.split('=', 1)
            clave = clave.strip()
            valor = valor.strip()
            if ',' in valor:
                parametros[clave] = tuple(map(eval, valor.split(',')))
            else:
                parametros[clave] = eval(valor)

    p = parametros.get('p')
    if p is None or p <= 255 or not isprime(p):
        raise ValueError("p debe ser primo y mayor a 255")

    a, b, d = parametros.get('a'), parametros.get('b'), parametros.get('d')
    if a is None or b is None or d is None:
        raise ValueError("Faltan parámetros a, b o d")
    a %= p
    b %= p
    d %= p
    #if (4 * (a ** 3) + 27 * (b ** 2)) % p != 0:
    #    raise ValueError("Curva no válida")

    g = parametros.get('g')
    if g is None:
        raise ValueError("Falta el parámetro g")
    return a, b, p, d, g



def toy_hash(mensaje: bytes, salt: bytes) -> int:
    if len(mensaje) != len(salt):
        raise ValueError("Mensaje y salt deben tener la misma longitud")
    xor_result = bytearray(x ^ s for x, s in zip(mensaje, salt))
    return sum((b + i) % 256 for i, b in enumerate(xor_result))



def generate_k(orden):
    while True:
        k = random.randint(1, orden - 1)
        if math.gcd(k, orden) == 1:
            return k

def generate_key(a, b, p, d, g):

    G = tuple(x % p for x in g)
    generador, orden = SumaDoblado.show_generator(a, b, p, G,SumaDoblado.point_add, SumaDoblado.point_double)
    if not (1 <= d <= orden):
        raise ValueError(f"d debe estar entre 1 y {orden}")
    B = SumaDoblado.point_mul(a, b, p, d, G,SumaDoblado.point_add,SumaDoblado.point_double)
    Kpub = (p, a, b, orden, G, B)
    _guardar_archivo("practica04/public_key.txt", str(Kpub))
    _guardar_archivo("practica04/private_key.txt", str(d))
    return Kpub, d



def signature(mensaje: bytes, Kpub: tuple, Kpriv: int, salt: bytes) -> tuple:
    p, a, b, orden, G, B = Kpub
    h = toy_hash(mensaje, salt)
    k = generate_k(orden)
    R = SumaDoblado.point_mul(a, b, p, k, G,SumaDoblado.point_add,SumaDoblado.point_double)
    r = R[0] % orden
    if r == 0:
        raise ValueError("r no puede ser 0")
    k_inv = pow(k, -1, orden)
    s = (h + Kpriv * r) * k_inv % orden
    if s == 0:
        raise ValueError("s no puede ser 0")
    return r, s, h



def verify_from_data(r: int, s: int, h: int, Kpub: tuple) -> bool:
    """Verifica una firma ECDSA."""
    p, a, b, orden, G, B = Kpub
    if s == 0 or r == 0:
        return False
    try:
        w = pow(s, -1, orden)
    except ValueError:
        return False
    u1 = h * w % orden
    u2 = r * w % orden
    P1 = SumaDoblado.point_mul(a, b, p, u1, G,SumaDoblado.point_add,SumaDoblado.point_double) 
    P2 = SumaDoblado.point_mul(a, b, p, u2, B,SumaDoblado.point_add,SumaDoblado.point_double)
    P = SumaDoblado.point_add(a, b, p, P1, P2)
    return (P[0] % orden) == r



def _cargar_archivo(nombre_archivo):
    """Carga el contenido de un archivo."""
    with open(nombre_archivo, "r") as f:
        return f.read().strip()

def _guardar_archivo(nombre_archivo, contenido):
    directorio = os.path.dirname(nombre_archivo)
    if directorio:  
        os.makedirs(directorio, exist_ok=True)
    with open(nombre_archivo, "w") as f:
        f.write(contenido)


def main():
    """Función principal del programa."""
    directorio_base = "practica04"
    os.makedirs(directorio_base, exist_ok=True)

    while True:
        print("\n--- MENÚ ---")
        print("1. Generar claves")
        print("2. Firmar mensaje")
        print("3. Verificar firma")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                a, b, p, d, g = leer_parametros("practica04/parametros.txt")
                Kpub, Kpriv = generate_key(a, b, p, d, g)
                print("Claves generadas y guardadas.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "2":
            try:
                Kpub = eval(_cargar_archivo("practica04/public_key.txt"))
                Kpriv = int(_cargar_archivo("practica04/private_key.txt"))
                mensaje = input("Mensaje a firmar: ").encode()
                salt = os.urandom(len(mensaje))
                r, s, h = signature(mensaje, Kpub, Kpriv, salt)
                print("Firma generada (r, s):", (r, s))
                print("Hash (h):", h)
                _guardar_archivo("practica04/signature.txt", f"{r}\n{s}\n{h}")
                print("Firma guardada.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "3":
            try:
                Kpub = eval(_cargar_archivo("practica04/public_key.txt"))
                r, s, h = map(int, _cargar_archivo("practica04/signature.txt").split('\n'))
                if verify_from_data(r, s, h, Kpub):
                    print("Firma válida.")
                else:
                    print("Firma inválida.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "4":
            print("Saliendo.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
