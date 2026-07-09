from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QRadioButton, QComboBox, 
                           QLineEdit, QPushButton, QFileDialog, QMessageBox,
                           QButtonGroup)
from PyQt6.QtCore import Qt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5
import sys
import os

class AESCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cifrador AES")
        self.setMinimumSize(600, 300)  # Aumentado para acomodar el nuevo campo
        
        # Widget y layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        
        # Operación (Cifrar/Descifrar)
        operation_group = QButtonGroup(self)
        operation_layout = QHBoxLayout()
        operation_label = QLabel("Operación:")
        self.radio_encrypt = QRadioButton("Cifrar")
        self.radio_decrypt = QRadioButton("Descifrar")
        self.radio_encrypt.setChecked(True)
        operation_group.addButton(self.radio_encrypt)
        operation_group.addButton(self.radio_decrypt)
        
        operation_layout.addWidget(operation_label)
        operation_layout.addWidget(self.radio_encrypt)
        operation_layout.addWidget(self.radio_decrypt)
        operation_layout.addStretch()
        layout.addLayout(operation_layout)
        
        # Modo de operación
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Modo:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ECB", "CBC", "CFB", "OFB", "CTR"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Selección de archivo
        file_layout = QHBoxLayout()
        file_label = QLabel("Archivo:")
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        browse_button = QPushButton("Examinar")
        browse_button.clicked.connect(self.select_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)
        
        # Entrada de llave
        key_layout = QHBoxLayout()
        key_label = QLabel("Llave:")
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)
        
        # Vector de Inicialización (IV)
        iv_layout = QHBoxLayout()
        iv_label = QLabel("Vector de Inicialización (16 bytes):")
        self.iv_input = QLineEdit()
        self.iv_input.setPlaceholderText("Ingrese 16 caracteres para el IV")
        iv_layout.addWidget(iv_label)
        iv_layout.addWidget(self.iv_input)
        layout.addLayout(iv_layout)
        
        # Botón de proceso
        process_layout = QHBoxLayout()
        process_button = QPushButton("Procesar")
        process_button.clicked.connect(self.process)
        process_button.setFixedWidth(200)
        process_layout.addWidget(process_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(process_layout)
        
        # Agregar espacio al final
        layout.addStretch()
        
        # Inicializar visibilidad del IV
        self.on_mode_changed(self.mode_combo.currentText())

    def on_mode_changed(self, mode):
        """Maneja el cambio de modo de operación"""
        self.iv_input.setEnabled(mode != "ECB")
        if mode == "ECB":
            self.iv_input.setPlaceholderText("No se requiere IV para modo ECB")
        elif mode == "CTR":
            self.iv_input.setPlaceholderText("Ingrese 8 caracteres para el nonce")
        else:
            self.iv_input.setPlaceholderText("Ingrese 16 caracteres para el IV")

    def select_file(self):
        """Maneja la selección de archivo"""
        file_filter = "Archivos BMP (*.bmp);;Todos los archivos (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "", file_filter
        )
        if filename:
            self.file_path.setText(filename)

    def derive_key(self, user_key):
        """Deriva una llave de 128 bits usando MD5"""
        md5_hash = MD5.new()
        md5_hash.update(user_key.encode())
        return md5_hash.digest()

    def get_iv(self, mode):
        """Obtiene el IV del usuario y lo valida"""
        if mode == "ECB":
            return None
        
        iv_text = self.iv_input.text()
        if mode == "CTR":
            if len(iv_text.encode()) != 8:
                raise ValueError("El nonce debe ser de 8 bytes para modo CTR")
            return iv_text.encode()
        else:
            if len(iv_text.encode()) != 16:
                raise ValueError("El IV debe ser de 16 bytes")
            return iv_text.encode()

    def generate_output_filename(self, input_file, operation, mode):
        """Genera el nombre del archivo de salida según las convenciones"""
        base, ext = os.path.splitext(input_file)
        if operation == "cifrar":
            return f"{base}_e{mode}{ext}"
        else:  # descifrar
            if "_e" in base:
                base = base.split("_e")[0]
                return f"{base}_d{mode}{ext}"
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "El nombre del archivo no sigue el formato esperado para descifrado"
                )
                return None

    def process(self):
        """Procesa el archivo según la operación seleccionada"""
        if not self.validate_inputs():
            return
        
        try:
            # Obtener parámetros
            operation = "cifrar" if self.radio_encrypt.isChecked() else "descifrar"
            mode = self.mode_combo.currentText()
            
            # Derivar llave de 128 bits
            key = self.derive_key(self.key_input.text())
            
            # Obtener IV del usuario
            try:
                iv = self.get_iv(mode)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
                return
            
            # Leer archivo
            with open(self.file_path.text(), 'rb') as file:
                data = file.read()
            
            # Procesar datos
            if operation == "cifrar":
                processed_data = self.encrypt_data(data, key, iv, mode)
            else:
                processed_data = self.decrypt_data(data, key, iv, mode)
            
            # Guardar resultado
            output_file = self.generate_output_filename(
                self.file_path.text(), 
                operation,
                mode
            )
            
            if output_file:
                with open(output_file, 'wb') as file:
                    file.write(processed_data)
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Operación completada correctamente"
                )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error durante el proceso: {str(e)}"
            )

    def encrypt_data(self, data, key, iv, mode):
        """Cifra los datos según el modo seleccionado, preservando la cabecera BMP"""
        # Preservar los primeros 54 bytes (cabecera BMP)
        bmp_header = data[:54]
        image_data = data[54:]
        
        # Cifrar solo los datos de la imagen
        if mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))
            return bmp_header + encrypted_data
        elif mode == "CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))
            return bmp_header + iv + encrypted_data
        elif mode == "CFB":
            cipher = AES.new(key, AES.MODE_CFB, iv)
            encrypted_data = cipher.encrypt(image_data)
            return bmp_header + iv + encrypted_data
        elif mode == "OFB":
            cipher = AES.new(key, AES.MODE_OFB, iv)
            encrypted_data = cipher.encrypt(image_data)
            return bmp_header + iv + encrypted_data
        elif mode == "CTR":
            cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
            encrypted_data = cipher.encrypt(image_data)
            return bmp_header + iv + encrypted_data

    def decrypt_data(self, data, key, iv, mode):
        """Descifra los datos según el modo seleccionado, preservando la cabecera BMP"""
        # Extraer la cabecera BMP
        bmp_header = data[:54]
        encrypted_data = data[54:]
        
        if mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            return bmp_header + decrypted_data
        elif mode in ["CBC", "CFB", "OFB"]:
            iv = encrypted_data[:16]
            actual_encrypted_data = encrypted_data[16:]
            if mode == "CBC":
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_data = unpad(cipher.decrypt(actual_encrypted_data), AES.block_size)
            elif mode == "CFB":
                cipher = AES.new(key, AES.MODE_CFB, iv)
                decrypted_data = cipher.decrypt(actual_encrypted_data)
            else:  # OFB
                cipher = AES.new(key, AES.MODE_OFB, iv)
                decrypted_data = cipher.decrypt(actual_encrypted_data)
            return bmp_header + decrypted_data
        elif mode == "CTR":
            nonce = encrypted_data[:8]
            actual_encrypted_data = encrypted_data[8:]
            cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
            decrypted_data = cipher.decrypt(actual_encrypted_data)
            return bmp_header + decrypted_data

    def validate_inputs(self):
        """Valida las entradas del usuario"""
        if not self.file_path.text():
            QMessageBox.critical(
                self,
                "Error",
                "Por favor seleccione un archivo"
            )
            return False
        
        if not self.key_input.text():
            QMessageBox.critical(
                self,
                "Error",
                "Por favor ingrese una llave"
            )
            return False
        
        if not os.path.exists(self.file_path.text()):
            QMessageBox.critical(
                self,
                "Error",
                "El archivo seleccionado no existe"
            )
            return False
        
        mode = self.mode_combo.currentText()
        if mode != "ECB" and not self.iv_input.text():
            QMessageBox.critical(
                self,
                "Error",
                "Por favor ingrese un vector de inicialización"
            )
            return False
        
        return True

def main():
    app = QApplication(sys.argv)
    window = AESCipherApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()