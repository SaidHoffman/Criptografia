from sympy import isprime

def residuos_cuadraticos(p):

    if p < 2 or not isprime(p):
        raise ValueError("El número debe ser primo y mayor a 2")
    residuos = {}
    for x in range(p):
        residuo = (x * x) % p
        if residuo not in residuos:
            residuos[residuo] = []
        residuos[residuo].append(x)
        
    return residuos
