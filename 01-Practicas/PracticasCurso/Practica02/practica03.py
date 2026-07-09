import SumaDoblado
from sympy import isprime

def pedirDatos():
    print("Ingrese los valores de la curva eliptica")
    a = int(input("Ingrese a: "))
    b = int(input("Ingrese b: "))
    p = int(input("Ingrese p (primo): "))

    if p.bit_length() < 7 or  not isprime(p):
        raise ValueError("El número debe ser primo y mayor a 7 bits")
    
    if (4 * (a ** 3) + 27 * (b ** 2)) % p == 0:
        raise ValueError("La curva no es una curva singular")
    
    x = int(input("Ingresa x de P: "))
    y = int(input("Ingresa y de P: "))
    z = int(input("Ingresa z de P: "))

    P = (x % p, y% p, z % p)
    


    generador = SumaDoblado.show_generator(a, b, p, P, SumaDoblado.point_add, SumaDoblado.point_double)
    print(f"El punto P es generador: {generador}")
    if generador is False:
        print("El punto P no es generador")
    
    cardinalidad = len(SumaDoblado.find_points_on_curve(a, b, p))

    kp = int(input(f"Ingrese un valor entre 2 y {cardinalidad}: "))

    if kp < 2 or kp > cardinalidad:
        raise ValueError("El valor de k debe ser entre 2 y la cardinalidad de la curva")
    
    return a, b, p, P, kp


def  publickey(a, b, p, P, kp):
    Q = SumaDoblado.point_mul(a, b, p, kp, P, SumaDoblado.point_add, SumaDoblado.point_double)
    print(f"Clave pública: {Q}")
    return Q

#funcion para multiplicar llave publica de bob poe mi clave privada
def SecretoCompartido(a, b, p, kp):
    print("Ingrese la clave publica de Bob")
    x = int(input("Ingresa x de Q: "))
    y = int(input("Ingresa y de Q: "))
    z = int(input("Ingresa z de Q: "))
    Q = (x % p, y % p, z % p)

    P = SumaDoblado.point_mul(a, b, p, kp, Q, SumaDoblado.point_add, SumaDoblado.point_double)
    print(f"Secreto Compartido: {P}")
    return P

def main():
    a, b, p, P, kp = pedirDatos()
    publickey(a, b, p, P, kp)
    SecretoCompartido(a, b, p, kp)
    
if __name__ == "__main__":
    main()