#Para la interfaz gráfica se usa PyQt6, instalar con pip install PyQt6
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QGridLayout   
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox

#Para el cifrado/descifrado de la imagen se usa la librería PyCryptodome, instalar con pip install pycryptodome
#Para esta práctica tocó utilizar AES, importamos el módulo AES
from Crypto.Cipher import AES

#Para utilizar cualquier longitud de clave (1-16 bytes) usaremos un hash como MD5 o SHAKE128 para generar una clave de 16 bytes (128 bites)
from Crypto.Hash import SHAKE128, MD5

#Los modos vienen incluidos en la librería, no es necesario importarlos

#Para los bloques que no sean de 128 bits, se rellenará usando pad, de la librería Padding
from Crypto.Util.Padding import pad, unpad #unpad es para quitar el relleno de un bloque


#Para el espacio de la imagen que aceptara arrastrar y soltar, y mostrará la imagen seleccionada
class LabelImagen(QLabel):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imagen = None

    #Para arrastrar y soltar la imagen
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile() and url.toLocalFile().endswith(".bmp"):
                self.setImage(url.toLocalFile())

    #Para mostrar la imagen seleccionada
    def setImage(self, imagePath):
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.imagen = imagePath
        
    #Para limpiar la imagen
    def limpiarImagen(self):
        self.clear()
        self.imagen = None

#Para la ventana principal
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES - Modos de Operación")
        self.setGeometry(100, 100, 700, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(QGridLayout())

        #Dividimos la ventana en 4 cuadrantes del mismo tamaño
        #Cuadrante 1 - Para las opciones de cifrado/descifrado y las opciones de los modos de operación
        self.cuadrante1 = QWidget()
        self.initCuadrante1()

        #Cuadrante 2 - Para la imagen seleccionada
        self.cuadrante2 = LabelImagen()

        #Cuadrante 3 - Para los campos de texto de la clave y el vector de inicialización
        self.cuadrante3 = QWidget()
        self.initCuadrante3()

        #Cuadrante 4 - Para la imagen cifrada/descifrada
        self.cuadrante4 = QLabel()
        self.cuadrante4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Añadimos los cuadrantes al grid layout
        self.central_widget.layout().addWidget(self.cuadrante1, 0, 0)
        self.central_widget.layout().addWidget(self.cuadrante2, 0, 1)
        self.central_widget.layout().addWidget(self.cuadrante3, 1, 0)
        self.central_widget.layout().addWidget(self.cuadrante4, 1, 1)

        #Estiramiento para que todos los cuadrantes se distribuyan equitativamente
        self.central_widget.layout().setColumnStretch(0, 1)
        self.central_widget.layout().setColumnStretch(1, 1)
        self.central_widget.layout().setRowStretch(0, 1)
        self.central_widget.layout().setRowStretch(1, 1)

        #Colocamos un borde alrededor de los cuadrantes
        self.cuadrante1.setStyleSheet("border: 1px solid black;")
        self.cuadrante2.setStyleSheet("border: 1px solid black;")
        self.cuadrante3.setStyleSheet("border: 1px solid black;")
        self.cuadrante4.setStyleSheet("border: 1px solid black;")

    #Para el cuadrante 1
    def initCuadrante1(self):
        layout = QVBoxLayout()

        #Opciones de cifrado/descifrado
        self.comboOperacion = QComboBox()
        self.comboOperacion.addItems(["Seleccionar", "Cifrar", "Descifrar"])
        self.comboOperacion.setFixedWidth(200)
        self.comboOperacion.setStyleSheet("font-size: 16px;")
        #Lo centramos horizontalmente metiendolo en un layout
        operacionLayout = QHBoxLayout()
        operacionLayout.addStretch()
        operacionLayout.addWidget(self.comboOperacion)
        operacionLayout.addStretch()

        #Opciones de los modos de operación
        self.comboModo = QComboBox()
        self.comboModo.addItems(["Seleccionar", "ECB", "CBC", "CFB", "OFB", "CTR"])
        self.comboModo.setFixedWidth(200)
        self.comboModo.setStyleSheet("font-size: 16px;")
        #Lo centramos horizontalmente metiendolo en un layout
        self.comboModo.currentTextChanged.connect(self.habilitarmodo)
        modoLayout = QHBoxLayout()
        modoLayout.addStretch()
        modoLayout.addWidget(self.comboModo)
        modoLayout.addStretch()

        #Labels
        self.lblOperacion = QLabel("Operación")
        self.lblOperacion.setFixedWidth(150)
        self.lblOperacion.setFixedHeight(20)
        self.lblOperacion.setStyleSheet("border: 0px; font-size: 16px;")
        self.lblModo = QLabel("Modo de Operación")
        self.lblModo.setFixedWidth(150)
        self.lblModo.setFixedHeight(20)
        self.lblModo.setStyleSheet("border: 0px; font-size: 16px;")

        #Añadimos los elementos al layout
        layout.addWidget(self.lblOperacion)
        layout.addLayout(operacionLayout)
        layout.addWidget(self.lblModo)
        layout.addLayout(modoLayout)
        
        #Lo añadios al cuadrante 1
        self.cuadrante1.setLayout(layout)

    #Para el cuadrante 3
    def initCuadrante3(self):
        layout = QVBoxLayout()

        #Botón para seleccionar la imagen
        self.btnCargarImagen = QPushButton("Cargar Imagen")
        self.btnCargarImagen.clicked.connect(self.cargarImagen)
        self.btnCargarImagen.setFixedWidth(150)
        self.btnCargarImagen.setStyleSheet("font-size: 16px; background-color: #333;")
        #Lo centramos horizontalmente metiendolo en un layout
        btnLayout1 = QHBoxLayout()
        btnLayout1.addStretch()
        btnLayout1.addWidget(self.btnCargarImagen)
        btnLayout1.addStretch()

        #Campo de texto para la clave
        self.txtClave = QLineEdit()
        self.txtClave.setPlaceholderText("1-16 caracteres")
        self.txtClave.setMaxLength(16)
        self.txtClave.setFixedWidth(250)
        self.txtClave.setStyleSheet("font-size: 16px;")
        #Lo centramos horizontalmente metiendolo en un layout
        self.txtClave.setEchoMode(QLineEdit.EchoMode.Password)
        claveLayout = QHBoxLayout()
        claveLayout.addStretch()
        claveLayout.addWidget(self.txtClave)
        claveLayout.addStretch()

        #Campo de texto para el vector de inicialización
        self.txtIV = QLineEdit()
        self.txtIV.setPlaceholderText("16 caracteres")
        self.txtIV.setMaxLength(16)
        self.txtIV.setFixedWidth(250)
        self.txtIV.setStyleSheet("font-size: 16px;")
        #Lo centramos horizontalmente metiendolo en un layout
        ivLayout = QHBoxLayout()
        ivLayout.addStretch()
        ivLayout.addWidget(self.txtIV)
        ivLayout.addStretch()

        #Botón para validar y realizar operación
        self.btnRealizar = QPushButton("Realizar Operación")
        self.btnRealizar.clicked.connect(self.realizarOperacion)
        self.btnRealizar.setFixedWidth(150)
        self.btnRealizar.setStyleSheet("font-size: 16px; background-color: #333;")
        #Lo centramos horizontalmente metiendolo en un layout
        btnLayout2 = QHBoxLayout()
        btnLayout2.addStretch()
        btnLayout2.addWidget(self.btnRealizar)
        btnLayout2.addStretch()

        #Labels
        self.lblClave = QLabel("Clave")
        self.lblClave.setFixedWidth(150)
        self.lblClave.setFixedHeight(20)
        self.lblClave.setStyleSheet("border: 0px; font-size: 16px;")
        self.lblIV = QLabel("Vector de Inicialización (C0)")
        self.lblIV.setFixedWidth(200)
        self.lblIV.setFixedHeight(20)
        self.lblIV.setStyleSheet("border: 0px; font-size: 16px;")

        #Añadimos los elementos al layout
        layout.addLayout(btnLayout1)
        layout.addWidget(self.lblClave)
        layout.addLayout(claveLayout)
        layout.addWidget(self.lblIV)
        layout.addLayout(ivLayout)
        layout.addLayout(btnLayout2)

        #Lo añadimos al cuadrante 3
        self.cuadrante3.setLayout(layout)
    

    #Para manejar el cambio de operación

    def habilitarmodo(self, modo):
        if modo == "ECB":
            self.txtIV.setEnabled(False)
            self.txtIV.setText("")
            self.txtIV.setPlaceholderText("No se requiere vector para modo ECB")
        elif modo == "CTR":
            self.txtIV.setEnabled(True)
            self.txtIV.setPlaceholderText("8 caracteres")
        else:
            self.txtIV.setEnabled(True)
            self.txtIV.setPlaceholderText("16 caracteres")

    #Para cargar la imagen
    def cargarImagen(self):
        #Abrimos el cuadro de diálogo para seleccionar la imagen
        fileDialog = QFileDialog()
        filePath = fileDialog.getOpenFileName(self, "Seleccionar Imagen BMP", "", "Imagen BMP (*.bmp)")

        if filePath[0]:
            self.cuadrante2.setImage(filePath[0])

        #Limpiamos la imagen cifrada/descifrada
        self.cuadrante4.clear()

    #Para realizar la operación de cifrado/descifrado
    def realizarOperacion(self):
        #checamos que la operación y el modo de operación hayan sido seleccionados
        if self.comboOperacion.currentIndex() == 0 or self.comboModo.currentIndex() == 0:
            #Soltamos una alerta en un messagebox
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Icon.Warning)
            alerta.setWindowTitle("Operación y/o Modo de Operación no seleccionados")
            alerta.setText("Por favor selecciona una operación y un modo de operación.")
            alerta.exec()
            return
        
        #checamos que haya una imagen seleccionada
        if not self.cuadrante2.imagen:
            #Soltamos una alerta en un messagebox
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Icon.Warning)
            alerta.setWindowTitle("Imagen no seleccionada")
            alerta.setText("Por favor selecciona una imagen.")
            alerta.exec()
            return
        
        #Checamos que, si el modo es diferente de ECB, se haya ingresado un vector de inicialización
        if self.comboModo.currentText() != "ECB" and not self.txtIV.text():
            #Soltamos una alerta en un messagebox
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Icon.Warning)
            alerta.setWindowTitle("Vector de Inicialización no ingresado")
            alerta.setText("Por favor ingresa un vector de inicialización.")
            alerta.exec()
            return

        #checamos que se haya ingresado una clave
        if not self.txtClave.text():
            #Soltamos una alerta en un messagebox
            alerta = QMessageBox()
            alerta.setIcon(QMessageBox.Icon.Warning)
            alerta.setWindowTitle("Clave no ingresada")
            alerta.setText("Por favor ingresa una clave.")
            alerta.exec()
            return
        
        #Obtenemos la operación a realizar
        operacion = self.comboOperacion.currentText()
        print("Operación:", operacion)

        #Obtenemos el modo de operación
        modo = self.comboModo.currentText()
        print("Modo de Operación:", modo)

        #Obtenemos la clave
        clave = self.txtClave.text()
        print("Clave:", clave)

        #Checamos si la clave es de 16 bytes, si no, la convertimos a 16 bytes
        if len(clave) < 16:
            #Usamos MD5 para generar una clave de 16 bytes
            hash = MD5.new()
            hash.update(clave.encode()) #Tanto MD5 como SHAKE128 requieren que la entrada sea en bytes, por eso el encode
            clave = hash.digest()
            print("Clave generada:", clave)
            #imprimimos la clave generada en string
            print("Clave generada en string:", clave.hex())
            # #Podemos usar SHAKE128 para generar una clave de 16 bytes
            #SHAKE128 es un hash que genera una salida de longitud variable, la que queramos
            # hash = SHAKE128.new()
            # hash.update(clave.encode())
            # clave = hash.read(16)
            # print("Clave generada:", clave)
        else:
            clave = clave.encode()
    
        #Obtenemos el vector de inicialización
        if modo != "ECB":
            if modo == "CBC" or modo == "CFB" or modo == "OFB":
                if len(self.txtIV.text()) != 16:
                    #Soltamos una alerta en un messagebox
                    alerta = QMessageBox()
                    alerta.setIcon(QMessageBox.Icon.Warning)
                    alerta.setWindowTitle("Vector de Inicialización incorrecto")
                    alerta.setText("El vector de inicialización debe ser de 16 caracteres.")
                    alerta.exec()
                    return
            # if modo == "CTR":
            #     if len(self.txtIV.text()) >= 16:
            #         #Soltamos una alerta en un messagebox
            #         alerta = QMessageBox()
            #         alerta.setIcon(QMessageBox.Icon.Warning)
            #         alerta.setWindowTitle("Vector de Inicialización incorrecto")
            #         alerta.setText("El vector de inicialización debe ser menor a 16 caracteres.")
            #         alerta.exec()
            #         return
            iv = self.txtIV.text()
            print("Vector de Inicialización:", iv)
            iv = iv.encode()
        else:
            iv = None

        #Obtenemos la ruta de la imagen
        imagen = self.cuadrante2.imagen
        print("Imagen:", imagen)

        #Mandamos a llamar a la función de cifrado/descifrado
        imagenNueva = self.encryptDecrypt(imagen, clave, iv, modo, operacion)

        #Colocamos la imagen cifrada/descifrada en el cuadrante 4
        pixmap = QPixmap(imagenNueva)
        self.cuadrante4.setPixmap(pixmap.scaled(self.cuadrante4.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    #Para cifrar la imagen
    def encryptDecrypt(self, imagen, clave, iv, modo, operacion):
        inicialModo = ""

        #Checamos el modo de cifrado
        if modo == "ECB":
            print("Modo ECB...")
            cipher = AES.new(clave, AES.MODE_ECB)
            inicialModo = "ECB"
        elif modo == "CBC":
            print("Modo CBC...")
            cipher = AES.new(clave, AES.MODE_CBC, iv)
            inicialModo = "CBC"
        elif modo == "CFB":
            print("Modo CFB...")
            cipher = AES.new(clave, AES.MODE_CFB, iv)
            inicialModo = "CFB"
        elif modo == "OFB":
            print("Modo OFB...")
            cipher = AES.new(clave, AES.MODE_OFB, iv)
            inicialModo = "OFB"
        else:
            print("Modo CTR...")
            #En el modo CTR no se usa un vector de inicialización, se usa un nonce, el cual, debe de ser de longitud 0 - 15 bytes, de preferencia se deja de 8 bytes
            #Además, se le puede pasar el valor inicial del contador, que si no se pasa, se toma como 0
            #También, puede recibir un parametro más "counter" creado con Crypto.Util.Counter.new() que es un objeto más complejo
            #Tomamos como nonce los primeros 8 bytes del vector de inicialización
            nonce = iv[:8]
            cipher = AES.new(clave, AES.MODE_CTR, nonce=nonce)
            inicialModo = "CTR"

        #Para leer los datos de la imagen
        with open(imagen, "rb") as file:
            datosImagen = file.read()
            
        #Separamos los datos de la cabecera de la imagen
        cabecera = datosImagen[:54] #La cabecera de la imagen BMP es de 54 bytes, los primeros 54 bytes
        datosSinCabecera = datosImagen[54:] #Los datos de la imagen a cifrar, a partir del byte 54

        #Checamos que operación se va a realizar
        if operacion == "Cifrar":
            #Ciframos los datos de la imagen
            datosProcesar = cipher.encrypt(pad(datosSinCabecera, AES.block_size))
        else:
            #Desciframos los datos de la imagen
            #datosProcesar = unpad(cipher.decrypt(datosSinCabecera), AES.block_size)
            datosProcesar = cipher.decrypt(datosSinCabecera)

        #Juntamos los datos cifrados con la cabecera
        datosCompletos = cabecera + datosProcesar

        #Guardamos la nueva imagen siguiendo la nomenclatura: nombreOriginal_eMODO.bmp, la e es de encrypt y se colocan las siglas del modo, la d es de decrypt
        if operacion == "Cifrar":
            imagenNueva = imagen.replace(".bmp", f"_e{inicialModo}.bmp")
        else:
            imagenNueva = imagen.replace(".bmp", f"_d{inicialModo}.bmp")
        
        #Guardamos la imagen cifrada/descifrada
        with open(imagenNueva, "wb") as file:
            file.write(datosCompletos)

        return imagenNueva

def main():
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()