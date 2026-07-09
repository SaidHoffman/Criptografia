from sympy import randprime 
import Ejercicio1  
import Ejercicio2


p = randprime(3, 1000)


resultado1 = Ejercicio1.residuos_cuadraticos(p)
a, b, ecuacion = Ejercicio2.generar_ec_no_singular(p)

print(f"Residuos cuadráticos y raíces cuadradas para {p}: {resultado1}")
print(f"Curva elíptica no singular para {p}: {ecuacion}")
print(f"Valor de a: {a}")
print(f"Valor de b: {b}")


def find_points_on_curve(a, b, p):
    points = []  
    for x in range(p): 
        sus = (x ** 3 + a * x + b) % p  
        for y in resultado1.get(sus, []): 
            points.append((x, y))
    return points


def is_point_on_curve(a, b, p, P):
    x, y, z = P

    if (x, y, z) == (0, 1, 0):
        return True

    if z != 1: 
        return False
    
    else:
        lhs = (y ** 2) % p
        rhs = (x ** 3 + a * x + b) % p 

    return lhs == rhs 

puntos = find_points_on_curve(a, b, p)
print(f"Puntos en la curva: {puntos}")

if puntos:
    P = (puntos[0][0], puntos[0][1], 1)  
    print(f"El punto {P} está en la curva: {is_point_on_curve(a, b, p, P)}")
else:
    print("No se encontraron puntos en la curva.")
