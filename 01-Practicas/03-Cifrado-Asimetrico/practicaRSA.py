#Código para cifrar y descifrar archivos con RSA
import sys
from Crypto.PublicKey import RSA #Para la importación de llaves
from Crypto.Cipher import PKCS1_OAEP #Para el cifrado y descifrado
from Crypto.Signature import pkcs1_15 #Para la firma y verificación
from Crypto.Hash import SHA256 #Para el hash del mensaje
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QFileDialog,
    QTextEdit
)
from PyQt6.QtWidgets import QMessageBox

import base64

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cifrado RSA")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowState(Qt.WindowState.WindowMaximized)

        #Layout principal
        mainLayout = QHBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        #Layout de la izquierda
        self.leftLayout = self.crearLeftLayout()
        self.rightLayout = self.crearRightLayout()

        mainLayout.addWidget(self.leftLayout, 1)
        mainLayout.addWidget(self.rightLayout, 2)

    def crearLeftLayout(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        self.operacionLabel = QLabel("Selecciona la acción a realizar:")
        self.operacionLabel.setFixedWidth(250)
        self.operacionLabel.setFixedHeight(20)
        self.operacionLabel.setStyleSheet("font-size: 16px; font-weight: bold; border: 0px;")
        layout.addWidget(self.operacionLabel)

        #ComboBox para seleccionar la acción
        self.comboAccion = QComboBox()
        self.comboAccion.addItems(["Seleccionar", "Cifrar", "Descifrar", "Firmar", "Verificar"])
        self.comboAccion.setFixedWidth(200)
        self.comboAccion.setStyleSheet("font-size: 16px;")
        #Lo centramos horizontalmente metiendolo en un layout
        operacionLayout = QHBoxLayout()
        operacionLayout.addStretch()
        operacionLayout.addWidget(self.comboAccion)
        operacionLayout.addStretch()

        layout.addLayout(operacionLayout)

        self.keyLabelBtn = QLabel("Selecciona la llave:")
        self.keyLabelBtn.setFixedWidth(200)
        self.keyLabelBtn.setFixedHeight(20)
        self.keyLabelBtn.setStyleSheet("font-size: 16px; font-weight: bold; border: 0px;")
        layout.addWidget(self.keyLabelBtn)

        #Botón para cargar la llave
        self.keyBtn = QPushButton("Cargar llave")
        self.keyBtn.clicked.connect(self.cargarLlave)
        self.keyBtn.setFixedWidth(150)
        self.keyBtn.setStyleSheet("font-size: 16px; background-color: #333;")
        #Lo centramos horizontalmente metiendolo en un layout
        keyLayout = QHBoxLayout()
        keyLayout.addStretch()
        keyLayout.addWidget(self.keyBtn)
        keyLayout.addStretch()

        layout.addLayout(keyLayout)

        #Label para mostrar el archivo de la llave
        self.keyLabel = QLabel("Llave no cargada")
        self.keyLabel.setFixedWidth(150)
        self.keyLabel.setFixedHeight(20)
        self.keyLabel.setStyleSheet("font-size: 12px; border: 0px; text-align: center;")

        #Lo centramos horizontalmente metiendolo en un layout
        keyLabelLayout = QHBoxLayout()
        keyLabelLayout.addStretch()
        keyLabelLayout.addWidget(self.keyLabel)
        keyLabelLayout.addStretch()

        layout.addLayout(keyLabelLayout)

        self.fileLabelBtn = QLabel("Selecciona el archivo a procesar:")
        self.fileLabelBtn.setFixedWidth(250)
        self.fileLabelBtn.setFixedHeight(20)
        self.fileLabelBtn.setStyleSheet("font-size: 16px; font-weight: bold; border: 0px;")
        layout.addWidget(self.fileLabelBtn)

        #Botón para cargar el archivo
        self.fileBtn = QPushButton("Cargar archivo")
        self.fileBtn.clicked.connect(self.cargarArchivo)
        self.fileBtn.setFixedWidth(150)
        self.fileBtn.setStyleSheet("font-size: 16px; background-color: #333;")

        #Lo centramos horizontalmente metiendolo en un layout
        fileLayout = QHBoxLayout()
        fileLayout.addStretch()
        fileLayout.addWidget(self.fileBtn)
        fileLayout.addStretch()

        layout.addLayout(fileLayout)

        #Label para mostrar el archivo seleccionado
        self.fileLabel = QLabel("Archivo no cargado")
        self.fileLabel.setFixedWidth(150)
        self.fileLabel.setFixedHeight(20)
        self.fileLabel.setStyleSheet("font-size: 12px; border: 0px;")

        #Lo centramos horizontalmente metiendolo en un layout
        fileLabelLayout = QHBoxLayout()
        fileLabelLayout.addStretch()
        fileLabelLayout.addWidget(self.fileLabel)
        fileLabelLayout.addStretch()

        layout.addLayout(fileLabelLayout)

        #Botón para ejecutar la acción
        self.execBtn = QPushButton("Ejecutar")
        self.execBtn.clicked.connect(self.ejecutar)
        self.execBtn.setFixedWidth(150)
        self.execBtn.setStyleSheet("font-size: 16px; background-color: #333;")
        #Lo centramos horizontalmente metiendolo en un layout
        execLayout = QHBoxLayout()
        execLayout.addStretch()
        execLayout.addWidget(self.execBtn)
        execLayout.addStretch()

        layout.addLayout(execLayout)

        return panel
    
    def crearRightLayout(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        #Text area para mostrar el archivo cargado
        self.archivoEntrada = QTextEdit()
        self.archivoEntrada.setPlaceholderText("Contenido del archivo cargado")
        self.archivoEntrada.setReadOnly(True)
        self.archivoEntrada.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.archivoEntrada, 1)

        #Text area para mostrar el archivo procesado
        self.archivoSalida = QTextEdit()
        self.archivoSalida.setPlaceholderText("Resultado de la acción")
        self.archivoSalida.setReadOnly(True)
        self.archivoSalida.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.archivoSalida, 1)

        return panel
    
    def cargarLlave(self):
        keyFile, _ = QFileDialog.getOpenFileName(self, "Seleccionar Llave", "", "Archivos de Llave (*.pem)")
        self.keyFile = keyFile
        fileName = keyFile.split("/")[-1]

        if keyFile:
            self.keyLabel.setText(fileName)
            #Limpiamos el contenido del archivo
            self.archivoEntrada.setText("")
            self.archivoSalida.setText("")
            self.fileLabel.setText("Archivo no cargado")
            self.fileName = None
            self.archivoSalida.setStyleSheet("font-weight: normal; font-size: 16px;")
        else:
            self.keyLabel.setText("Llave no cargada")

    def cargarArchivo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Archivos de Texto (*.txt)")
        self.fileName = file
        fileName = file.split("/")[-1]

        if file:
            self.fileLabel.setText(fileName)
            with open(file, "rb") as f:
                contenido = f.read()
                #Colocamos el contenido del archivo en el text area en formato ascii
                try:
                    self.archivoEntrada.setText(contenido.decode())
                except UnicodeDecodeError:
                    self.archivoEntrada.setText(base64.b64encode(contenido).decode('utf-8'))
        else:
            self.fileLabel.setText("Archivo no cargado")

    def ejecutar(self):
        #Checamos primero que haya una llave cargada
        if not hasattr(self, "keyFile"):
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una llave.")
            return
        
        #Checamos que haya un archivo cargado
        if self.fileLabel.text() == "Archivo no cargado":
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un archivo.")
            return

        #Checamos que haya una acción seleccionada
        accion = self.comboAccion.currentText()
        if accion == "Seleccionar":
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una acción.")
            return

        #Cargamos la llave
        with open(self.keyFile, "r") as f1:
            data = f1.read()

        if accion == "Cifrar":
            #Checamos que la llave sea publica
            if "PUBLIC" not in data:
                QMessageBox.warning(self, "Advertencia", "La llave seleccionada no es pública.")
                return
            
            #Cargamos la llave
            key = RSA.import_key(data)
            cipher = PKCS1_OAEP.new(key)

            #Ciframos el archivo
            with open(self.fileName, "rb") as f:
                contenido = f.read()
                try:
                    cifrado = cipher.encrypt(contenido)
                except ValueError:
                    QMessageBox.warning(self, "Advertencia", "El archivo es demasiado grande para cifrarlo.")
                    return

            #Guardamos el archivo cifrado
            #Los nombres de los archivo cambiaran dependiendo de la acción, para el cifrado será: nombreOriginal_RSAc.txt
            file = self.fileName.split("/")[-1]
            file = file.split(".")[0] + "_RSAc.txt"
            with open(file, "wb") as f:
                f.write(cifrado)

            #Mostramos el contenido del archivo cifrado
            self.archivoSalida.setText(base64.b64encode(cifrado).decode('utf-8'))

            #Cerramos el archivo con el mensaje original
            f.close()
        
        elif accion == "Descifrar":
            #Checamos que la llave sea privada
            if "PRIVATE" not in data:
                QMessageBox.warning(self, "Advertencia", "La llave seleccionada no es privada.")
                return
            
            #Cargamos la llave
            key = RSA.import_key(data)
            cipher = PKCS1_OAEP.new(key)

            #Desciframos el archivo
            with open(self.fileName, "rb") as f:
                contenido = f.read()
                try:
                    descifrado = cipher.decrypt(contenido)
                except ValueError:
                    QMessageBox.warning(self, "Advertencia", "El archivo no se puede descifrar.")
                    return

            #Guardamos el archivo descifrado
            #Los nombres de los archivo cambiaran dependiendo de la acción, para el descifrado será: nombreOriginal_RSAd.txt
            file = self.fileName.split("/")[-1]
            file = file.split(".")[0] + "_RSAd.txt"
            with open(file, "wb") as f:
                f.write(descifrado)

            #Mostramos el contenido del archivo descifrado
            try:
                self.archivoSalida.setText(descifrado.decode())
            except UnicodeDecodeError:
                self.archivoSalida.setText(base64.b64encode(descifrado).decode('utf-8'))

            #Cerramos el archivo con el mensaje cifrado
            f.close()
            
        elif accion == "Firmar":
            #Checamos que la llave sea privada
            if "PRIVATE" not in data:
                QMessageBox.warning(self, "Advertencia", "La llave seleccionada no es privada.")
                return
            
            #Obtenemos los datos del archivo
            with open(self.fileName, "rb") as f:
                contenido = f.read()

            #Cargamos la llave
            key = RSA.import_key(data)

            #Hasheamos el contenido del archivo
            h = SHA256.new(contenido)

            #Firmamos el hash
            firma = pkcs1_15.new(key).sign(h)

            #Guardamos la firma
            #Los nombres de los archivo cambiaran dependiendo de la acción, para la firma será: nombreOriginal_RSAf.txt
            file = self.fileName.split("/")[-1]
            file = file.split(".")[0] + "_RSAf.txt"
            with open(file, "wb") as f:
                f.write(firma)

            #Mostramos la firma
            self.archivoSalida.setText(base64.b64encode(firma).decode('utf-8'))

            #Cerramos el archivo con el mensaje original
            f.close()

        elif accion == "Verificar":
            #Checamos que la llave sea pública
            if "PUBLIC" not in data:
                QMessageBox.warning(self, "Advertencia", "La llave seleccionada no es pública.")
                return
            
            #Abrimos un dialogo para que el usuario seleccione el archivo con el mensaje original
            file, _ = QFileDialog.getOpenFileName(self, "Selecciona la Firma", "", "Archivos de Texto (*.txt)")
            if not file:
                QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un archivo.")
                return
            
            #Obtenemos la firma
            with open(file, "rb") as f:
                firma = f.read()

            #Obtenemos los datos del archivo
            with open(self.fileName, "rb") as f:
                contenido = f.read()

            #Cargamos la llave
            key = RSA.import_key(data)

            #Hasheamos el contenido del archivo
            h = SHA256.new(contenido)

            #Verificamos la firma
            try:
                pkcs1_15.new(key).verify(h, firma)
                self.archivoSalida.setStyleSheet("font-weight: bold; font-size: 16px;")
                self.archivoSalida.setText("La firma es válida.")
                QMessageBox.information(self, "Resultado", "La firma es válida.")
            except (ValueError, TypeError):
                self.archivoSalida.setText("La firma no es válida.")

            #Cerramos el archivo con el mensaje original
            f.close()
                
        #Limpiamos la llave y el archivo seleccionado
        # self.keyFile = None
        # self.keyLabel.setText("Llave no cargada")
        # self.fileName = None
        # self.fileLabel.setText("Archivo no cargado")

        #Cerramos el archivo con la llave
        f1.close()

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()