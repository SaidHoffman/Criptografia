import sys
import numpy as np # Para cálculos con matrices y determinantes 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QGridLayout, QLineEdit, QPushButton, 
                           QLabel, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt

class CalculadoraMatricesModulares(QMainWindow):
    """
    Esta clase crea una interfaz gráfica para realizar operaciones con matrices modulares.
    Hereda de QMainWindow para crear una ventana principal.
    """
    def __init__(self):
        super().__init__()
        # Configuración básica de la ventana
        self.setWindowTitle("Calculadora de Matrices Modulares")
        self.setGeometry(100, 100, 800, 600)  # (x, y, ancho, alto)
        
        # Creamos el widget principal que contendrá todo
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)
        layout_principal = QVBoxLayout()  # Layout vertical principal
        widget_principal.setLayout(layout_principal)
        
        # Sección para ingresar el módulo (n)
        layout_modulo = QHBoxLayout()
        self.label_modulo = QLabel("Tamaño del módulo (n):")
        self.input_modulo = QLineEdit()
        self.input_modulo.setPlaceholderText("Ingrese n")
        self.input_modulo.setFixedWidth(100)
        layout_modulo.addWidget(self.label_modulo)
        layout_modulo.addWidget(self.input_modulo)
        layout_modulo.addStretch()
        layout_principal.addLayout(layout_modulo)
        
        # Configuración para las dimensiones de las matrices
        layout_config = QHBoxLayout()
        
        # Configuración matriz A
        layout_matriz_a = QVBoxLayout()
        self.label_a = QLabel("Matriz A:")
        layout_matriz_a.addWidget(self.label_a)
        
        # Inputs para dimensiones de matriz A
        layout_dim_a = QHBoxLayout()
        self.filas_a = QLineEdit()
        self.filas_a.setPlaceholderText("Filas")
        self.cols_a = QLineEdit()
        self.cols_a.setPlaceholderText("Columnas")
        layout_dim_a.addWidget(self.filas_a)
        layout_dim_a.addWidget(self.cols_a)
        layout_matriz_a.addLayout(layout_dim_a)
        
        # Configuración matriz B (similar a matriz A)
        layout_matriz_b = QVBoxLayout()
        self.label_b = QLabel("Matriz B:")
        layout_matriz_b.addWidget(self.label_b)
        
        layout_dim_b = QHBoxLayout()
        self.filas_b = QLineEdit()
        self.filas_b.setPlaceholderText("Filas")
        self.cols_b = QLineEdit()
        self.cols_b.setPlaceholderText("Columnas")
        layout_dim_b.addWidget(self.filas_b)
        layout_dim_b.addWidget(self.cols_b)
        layout_matriz_b.addLayout(layout_dim_b)
        
        # Añadir configuraciones al layout
        layout_config.addLayout(layout_matriz_a)
        layout_config.addLayout(layout_matriz_b)
        
        # Botón para crear las matrices
        self.btn_crear = QPushButton("Crear Matrices")
        self.btn_crear.clicked.connect(self.crear_matrices)  # Conecta con la función crear_matrices
        layout_config.addWidget(self.btn_crear)
        
        layout_principal.addLayout(layout_config)
        
        # Espacio para mostrar las matrices
        self.layout_matrices = QHBoxLayout()
        self.matriz_a_widget = QWidget()
        self.matriz_b_widget = QWidget()
        self.layout_matrices.addWidget(self.matriz_a_widget)
        self.layout_matrices.addWidget(self.matriz_b_widget)
        layout_principal.addLayout(self.layout_matrices)
        
        # Menú desplegable para seleccionar operaciones
        layout_operaciones = QHBoxLayout()
        self.combo_operaciones = QComboBox()
        self.combo_operaciones.addItems([
            "Suma Modular", "Resta Modular", "Multiplicación Modular", 
            "Determinante Modular A", "Determinante Modular B",
            "Transpuesta A", "Transpuesta B",
            "Inversa Modular A", "Inversa Modular B"
        ])
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.realizar_operacion)
        layout_operaciones.addWidget(self.combo_operaciones)
        layout_operaciones.addWidget(self.btn_calcular)
        layout_principal.addLayout(layout_operaciones)
        
        # Sección para mostrar resultados
        self.label_resultado = QLabel("Resultado:")
        layout_principal.addWidget(self.label_resultado)
        self.matriz_resultado = QWidget()
        layout_principal.addWidget(self.matriz_resultado)
        
        # Listas para almacenar los inputs de las matrices
        self.matriz_a_inputs = []
        self.matriz_b_inputs = []

        #Crear los layouts para las matrices A y B
        self.layout_a = QGridLayout()
        self.layout_b = QGridLayout()
        self.matriz_a_widget.setLayout(self.layout_a)
        self.matriz_b_widget.setLayout(self.layout_b)

        #Crear el layout para el resultado
        self.layout_resultado = QGridLayout()
        self.matriz_resultado.setLayout(self.layout_resultado)
    
    def mod_inverse(self, a, m):
        """
        Calcula el inverso multiplicativo modular usando el algoritmo extendido de Euclides
        """
        def extended_gcd(a, b): 
            # Implementación recursiva del algoritmo de Euclides extendido
            if a == 0:  # Caso base: cuando el residuo es 0
                return b, 0, 1  
            # Llamada recursiva
            gcd, x1, y1 = extended_gcd(b % a, a)
            # Calcula los coeficientes de la combinación lineal 
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        # Calcula el MCD y los coeficientes por lo que llama a la función extendida
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("El inverso modular no existe")
        # Ajusta el resultado para que sea positivo y menor que m
        return (x % m + m) % m
    
    def det_mod(self, matriz, n):
        """
        Calcula el determinante de la matriz en módulo n
        1. Calcula el determinante normal
        2. Aplica el módulo al resultado
        """
        det = int(round(np.linalg.det(matriz)))
        return det % n
    
    def matriz_inversa_mod(self, matriz, n):
        """
        Calcula la inversa modular de una matriz
        Pasos:
        1. Calcula el determinante modular
        2. Calcula el inverso del determinante
        3. Calcula la matriz adjunta
        4. Multiplica la adjunta por el inverso del determinante
        """
        det = self.det_mod(matriz, n)
        det_inv = self.mod_inverse(det, n)
        
        # Calcula la matriz adjunta
        adj = np.round(np.linalg.inv(matriz) * np.linalg.det(matriz)).astype(int)
        
        # Calcula la inversa modular
        inv_mod = (adj * det_inv) % n
        return inv_mod
    
    def crear_matrices(self):
        """
        Crea los campos de entrada para las matrices A y B
        basándose en las dimensiones especificadas
        """
        try:
            # Verifica que el módulo sea válido
            self.modulo = int(self.input_modulo.text())
            if self.modulo < 2:
                raise ValueError("El módulo debe ser mayor o igual a 2")
                
            # Obtiene las dimensiones de las matrices
            filas_a = int(self.filas_a.text())
            cols_a = int(self.cols_a.text())
            filas_b = int(self.filas_b.text())
            cols_b = int(self.cols_b.text())

            for i in reversed(range(self.layout_a.count())):
                self.layout_a.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.layout_b.count())):
                self.layout_b.itemAt(i).widget().setParent(None)
            
            self.matriz_a_inputs = []
            for i in range(filas_a):
                fila = []
                for j in range(cols_a):
                    input_celda = QLineEdit()
                    input_celda.setFixedWidth(50)
                    self.layout_a.addWidget(input_celda, i, j)
                    fila.append(input_celda)
                self.matriz_a_inputs.append(fila)
            
            self.matriz_b_inputs = []
            for i in range(filas_b):
                fila = []
                for j in range(cols_b):
                    input_celda = QLineEdit()
                    input_celda.setFixedWidth(50)
                    self.layout_b.addWidget(input_celda, i, j)
                    fila.append(input_celda)
                self.matriz_b_inputs.append(fila)
            
            # # Limpia las matrices existentes
            # for i in reversed(range(self.matriz_a_widget.layout().count() if self.matriz_a_widget.layout() else 0)): 
            #     self.matriz_a_widget.layout().itemAt(i).widget().setParent(None)
            # for i in reversed(range(self.matriz_b_widget.layout().count() if self.matriz_b_widget.layout() else 0)):
            #     self.matriz_b_widget.layout().itemAt(i).widget().setParent(None)
            
            # # Crea la matriz A con campos de entrada
            # layout_a = QGridLayout()
            # self.matriz_a_widget.setLayout(layout_a)
            # self.matriz_a_inputs = []
            # for i in range(filas_a):
            #     fila = []
            #     for j in range(cols_a):
            #         input_celda = QLineEdit()
            #         input_celda.setFixedWidth(50)
            #         layout_a.addWidget(input_celda, i, j)
            #         fila.append(input_celda)
            #     self.matriz_a_inputs.append(fila)
            
            # # Crea la matriz B con campos de entrada
            # layout_b = QGridLayout()
            # self.matriz_b_widget.setLayout(layout_b)
            # self.matriz_b_inputs = []
            # for i in range(filas_b):
            #     fila = []
            #     for j in range(cols_b):
            #         input_celda = QLineEdit()
            #         input_celda.setFixedWidth(50)
            #         layout_b.addWidget(input_celda, i, j)
            #         fila.append(input_celda)
            #     self.matriz_b_inputs.append(fila)
                
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def obtener_matriz(self, inputs):
        """
        Convierte los inputs de la interfaz en una matriz numpy
        y aplica el módulo a cada elemento
        """
        matriz = []
        for fila in inputs:
            fila_valores = []
            for celda in fila:
                try:
                    # Convierte el texto a número y aplica el módulo
                    valor = int(celda.text() or "0") % self.modulo 
                    fila_valores.append(valor)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Por favor ingrese solo números enteros")
                    return None
            matriz.append(fila_valores)
        return np.array(matriz)
    
    def mostrar_resultado(self, resultado):
        """
        Muestra el resultado en la interfaz, ya sea un número o una matriz
        """
        # Limpia el resultado anterior
        # for i in reversed(range(self.matriz_resultado.layout().count() if self.matriz_resultado.layout() else 0)):
        #     self.matriz_resultado.layout().itemAt(i).widget().setParent(None)

        for i in reversed(range(self.layout_resultado.count())):
            self.layout_resultado.itemAt(i).widget().setParent(None)
        
        # layout_resultado = QGridLayout()
        # self.matriz_resultado.setLayout(layout_resultado)
        
        # Si es un número, muestra un solo label
        if isinstance(resultado, (int, float)):
            label = QLabel(str(int(resultado)))
            self.layout_resultado.addWidget(label, 0, 0)
        else:
            # Si es una matriz, crea una grid de labels
            for i in range(len(resultado)):
                for j in range(len(resultado[0])):
                    label = QLabel(str(int(resultado[i][j])))
                    self.layout_resultado.addWidget(label, i, j)
    
    def realizar_operacion(self):
        """
        Realiza la operación seleccionada en el menú desplegable
        y muestra el resultado
        """
        try:
            # Obtiene las matrices de la interfaz
            matriz_a = self.obtener_matriz(self.matriz_a_inputs)
            matriz_b = self.obtener_matriz(self.matriz_b_inputs)
            
            if matriz_a is None or matriz_b is None:
                return
            
            # Obtiene la operación seleccionada
            operacion = self.combo_operaciones.currentText()
            
            # Realiza la operación correspondiente
            if operacion == "Suma Modular":
                resultado = (matriz_a + matriz_b) % self.modulo
            elif operacion == "Resta Modular":
                resultado = (matriz_a - matriz_b) % self.modulo
            elif operacion == "Multiplicación Modular":
                resultado = np.matmul(matriz_a, matriz_b) % self.modulo
            elif operacion == "Determinante Modular A":
                resultado = self.det_mod(matriz_a, self.modulo)
            elif operacion == "Determinante Modular B":
                resultado = self.det_mod(matriz_b, self.modulo)
            elif operacion == "Transpuesta A":
                resultado = matriz_a.T % self.modulo
            elif operacion == "Transpuesta B":
                resultado = matriz_b.T % self.modulo
            elif operacion == "Inversa Modular A":
                resultado = self.matriz_inversa_mod(matriz_a, self.modulo)
            elif operacion == "Inversa Modular B":
                resultado = self.matriz_inversa_mod(matriz_b, self.modulo)
                
            # Muestra el resultado
            self.mostrar_resultado(resultado)
            
        except np.linalg.LinAlgError:
            QMessageBox.warning(self, "Error", "Error en el cálculo. Verifique que las dimensiones sean correctas y la matriz sea invertible si aplica.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error en la operación: {str(e)}")

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculadora = CalculadoraMatricesModulares()
    calculadora.show()
    sys.exit(app.exec())