from Crypto.Util.number import getPrime
from Crypto.Random.random import randrange, getrandbits
from sympy.ntheory.residue_ntheory import primitive_root, is_primitive_root
from sympy import isprime
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main():
    #Preguntamos si desea iniciar con el intercambio de llaves
    op = input("¿Deseas iniciar con el intercambio de llaves? (s/n): ")
    if op == 's':
        #Generamos un p de 2048 bits
        p = getPrime(2048)
        print("\nEl valor de p es:", p)
        #Calculamos un g primitivo de p
        #OPCIÓN 4, GENERAMOS UN PRIMO ALEATORIO QUE ESTÉ ENTRE 2 Y P-1
        g = randrange(2, p-1)
        #Checamos que sea primo
        while not isprime(g):
            g = randrange(2, p-1)

        print("\nEl valor de g es:", g)

        #Los guardamos en un archivo de texto
        with open("ParametrosPublicos.txt", 'w') as f:
            f.write(str(p) + '\n')
            f.write(str(g) + '\n')
            f.close()

        print("\nLos valores de g y p se han guardado en el archivo ParametrosPublicos.txt\n")
    else:

        #Abrimos un choose file dialog, solo permitimos archivos de texto y que verdaremente seleccione uno
        Tk().withdraw()
        filename = askopenfilename(filetypes=[("Text files", "*.txt")])

        #Leemos el archivo
        while True:
            try:
                with open(filename, 'r') as f:
                    p = int(f.readline())
                    g = int(f.readline())
                    f.close()
                    #Verificamos que p sea primo
                    if not isprime(p):
                        print("El valor de p no es primo")
                        filename = askopenfilename(filetypes=[("Text files", "*.txt")])
                        continue
                    #Checamos que g sea primo
                    if not isprime(g):
                        print("El valor de g no es primo")
                        filename = askopenfilename(filetypes=[("Text files", "*.txt")])
                        continue
                    # else:
                    #     print("\ng si es generador de p")
                    
                    print("\n")
                    break
            except FileNotFoundError:
                print("El archivo no existe")
                filename = askopenfilename(filetypes=[("Text files", "*.txt")])
            except ValueError:
                print("El archivo no tiene el formato correcto")
                filename = askopenfilename(filetypes=[("Text files", "*.txt")])

        print("El valor de p es:", p)
        print("\nEl valor de g es:", g)

    #Pedimos al usuario que ingrese su valor secreto
    while True:
        try:
            a = int(input("\nIngresa tu valor secreto: "))
            #Checamos que el valor sea menor que p-1 y mayor que 1
            if a <= 1 or a >= p-1:
                print("El valor debe ser menor que p-1 y mayor que 1")
                continue
            break
        except ValueError:
            print("Ingresa un valor entero")

    #Generamos la llave parcial
    Ka = pow(g, a, p)

    kaCaracteres = ''.join(chr((Ka >> (8 * i)) & 0xFF) for i in range((Ka.bit_length() + 7) // 8))

    #Guardamos la clave en caracteres en un archivo de texto
    with open("LlaveParcial.txt", 'w') as f:
        f.write("-----KEY-----\n")
        f.write(str(Ka) + '\n')
        f.write("-----END KEY-----\n")

    # print("\nTu llave parcial es: ", Ka)
    print("Tu llave parcial es:\n", kaCaracteres)
    # print("El tamaño de la llave parcial es de: ", Ka.bit_length(), "bits")

    print("\nSelecciona el archivo con la llave parcial de la otra persona")
    #Pedimos que seleccione el archivo con la llave parcial de la otra persona, mediante un choose file dialog
    filename = askopenfilename(filetypes=[("Text files", "*.txt")])

    BetoKeyCaracteres = ""
    BetoKey = 0

    #Leemos el archivo
    while True:
        try:
            with open(filename, 'r') as f:
                #Leemos el archivo
                line = f.readline()
                #Checamos que sea la llave
                if line != "-----KEY-----\n":
                    print("El archivo no tiene el formato correcto")
                    filename = askopenfilename(filetypes=[("Text files", "*.txt")])
                    continue
                #Leemos la llave
                BetoKey = int(f.readline())
                #Leemos la siguiente línea
                line = f.readline()
                #Checamos que sea el final de la llave
                if line != "-----END KEY-----\n":
                    print("El archivo no tiene el formato correcto")
                    filename = askopenfilename(filetypes=[("Text files", "*.txt")])
                    continue
                f.close()
                break
        except FileNotFoundError:
            print("El archivo no existe")
            filename = askopenfilename(filetypes=[("Text files", "*.txt")])
        except ValueError:
            print("El archivo no tiene el formato correcto.")
            filename = askopenfilename(filetypes=[("Text files", "*.txt")])

    BetoKeyCaracteres = ''.join(chr((BetoKey >> (8 * i)) & 0xFF) for i in range((BetoKey.bit_length() + 7) // 8))

    print("\nLa llave parcial de la otra persona es:\n", BetoKeyCaracteres)

    #Generamos la llave compartida
    print(BetoKey)
    K = pow(BetoKey, a, p)

    kCaracteres = ''.join(chr((K >> (8 * i)) & 0xFF) for i in range((K.bit_length() + 7) // 8))

    #Guardamos la clave en caracteres en un archivo de texto
    with open("LlaveCompartida.txt", 'w', encoding='utf-8') as f:
        f.write("-----KEY-----\n")
        f.write(str(K) + '\n')
        f.write("-----END KEY-----\n")

    print("\nLa llave compartida es:\n", kCaracteres)
    # print("El tamaño de la llave compartida es de: ", K.bit_length(), "bits")

if __name__ == '__main__':
    main()
