
import argparse
import Ejercicio1

def mod_inverse(a, p):
    try:
        return pow(a, -1, p)  
    
    except ValueError:
        return None

def mod_neg(value, p):
    return (-value) % p


def negate_point(a, b, p, P):
    (x, y, z) = P
    if z == 0:
        return (0, 1, 0)  
    if((y*y % p) == a*x*x + b):
        return (x, (-y) % p, z)
    else: 
        print("El punto no pertenece a la curva")

def point_add(a, b, p, P, Q):

    if P[2] == 0:
        return Q
    if Q[2] == 0:
        return P
 
    (x1, y1, z1) = P
    (x2, y2, z2) = Q

    if x1 == x2 and y1 == y2:
        return point_double(a, b, p, P)

    denom = (x2 - x1) % p
    inv_denom = mod_inverse(denom, p)
    if inv_denom is None:
        return (0, 1, 0)

    num = (y2 - y1) % p
    lamb = (num * inv_denom) % p
    x3 = (lamb * lamb - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p
    return (x3, y3, 1)

def point_double(a, b, p, P):

    (x1, y1, z1) = P

    if z1 == 0:
        return (0, 1, 0)

    if y1 % p == 0:
        return (0, 1, 0)

    denom = (2 * y1) % p
    inv_denom = mod_inverse(denom, p)
    if inv_denom is None:
        return (0, 1, 0)

    num = (3 * x1 * x1 + a) % p
    lamb = (num * inv_denom) % p


    x3 = (lamb*lamb - 2*x1) % p
    y3 = (lamb*(x1 - x3) - y1) % p
    return (x3, y3, 1)


def point_mul(a, b, p, k, G, point_add, point_double):

    O = (0, 1, 0)
    R = O
    Q = G

    while k > 0:
        
        if (k & 1) == 1:
            R = point_add(a, b, p, R, Q)
        
        Q = point_double(a, b, p, Q)
        
        k >>= 1

    return R
 


def find_points_on_curve(a, b, p):
    points = []  
    resultado1 = Ejercicio1.residuos_cuadraticos(p)
    point_number = 1
    for x in range(p): 
        sus = (x ** 3 + a * x + b) % p  
        for y in resultado1.get(sus, []):
            #print(f"Punto {point_number}: ({x}, {y})")
            point_number += 1
            points.append((x, y))
    return points

def show_generator(a, b, p, G, point_add, point_double):
    O = (0, 1, 0)
 
    i = 1
 
    puntos_en_curva = find_points_on_curve(a, b, p)
    
    cardinalidad = len(puntos_en_curva)+1 
    
    #print(f"Cardinalidad de la curva: {cardinalidad}")

    while True:
        R = point_mul(a, b, p, i, G, point_add, point_double) 
        #print(f"{i}*G = {R}")

        if R == O and i == cardinalidad: 
            return True,i
        elif R == O:
            print(f"El orden del punto es: {i}")
            return False, i

        else : pass

        i += 1
        
def pedir_valores():
    a = int(input("Ingresa a: "))
    b = int(input("Ingresa b: "))
    p = int(input("Ingresa p (primo): "))

  
    x = int(input("Ingresa x de P: "))
    y = int(input("Ingresa y de P: "))
    z = int(input("Ingresa z de P: "))

    P = (x % p, y% p, z % p)

    return a, b, p, P
# ------------------------------------------------------------------------------
# 3. Lógica main para no modificar el fuente al cambiar parámetros
# ------------------------------------------------------------------------------
def main():
    print("¿Qué operación deseas realizar?")
    print("1) Negación (neg)")
    print("2) Suma de puntos (add)")
    print("3) Duplicar punto (dbl)")
    print("4) Mostrar generador(generator)")
    opcion = input("Selecciona 1, 2, 3 o 4: ")


    if opcion == "1":
        
        a,b,p,P = pedir_valores()
        result = negate_point(a,b,p,P)
        print(f"-P = {result}")

    elif opcion == "2":
        a,b,p,P = pedir_valores()
        # Pedimos Q
        x2 = int(input("Ingresa x de Q: "))
        y2 = int(input("Ingresa y de Q: "))
        z2 = int(input("Ingresa z de Q: "))
        Q = (x2 % p, y2 % p, z2 % p)
        result = point_add(a,b,p,P, Q)
        print(f"P + Q = {result}")

    elif opcion == "3":  # dbl
        a,b,p,P = pedir_valores()
        result = point_double(a,b,p,P)
        print(f"2P = {result}")

    elif opcion == "4":  # generador
        a, b, p, P = pedir_valores()
        G = P
        show_generator(a, b, p, G, point_add, point_double)
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()