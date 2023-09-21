import datetime
import sys
import os
import time
from math import log2
import json
import configparser
import requests

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

import hashlib
import qrcode
import pyperclip
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi

# Set DPI Awareness
# os.environ["QT_FONT_DPI"] = "96"

class Main(QDialog):

    algorithm = ''
    nordpass_common_passwords = []
    hint_btn = []
    state_detect = 0
    path = ''

    api_url_scan = ''
    api_vt_key = ''
    api_file_scan = ''
    api_file_analysis = ''

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/mainUI.ui", self)

        # initialize 
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
        self.setWindowIcon(QIcon("./assets/icons/icons8-stan-marsh-96.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")
        self.label_logo = QPixmap("./assets/icons/icons8-stan-marsh-96.png")
        self.image_main = QPixmap("./assets/images/main.png")

        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_iconEye.setIcon(self.hide_icon)

        # -------------------- Home ---------------------------------------
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_home))
        self.btn_advanceUser.clicked.connect(self.openAdvancedUserHome)
        self.btn_networkUser.clicked.connect(self.openNetworkUserHome)

        # -------------------- Advance User ---------------------------------
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        # ------------------------------------------------------------------
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)
        self.btn_malware.clicked.connect(self.openMalwareHome)
        self.btn_digest.clicked.connect(self.openDigestHome)

        # --------------------- Network User --------------------------------
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)
        # ------------------------------------------------------------------
        self.btn_vulner.clicked.connect(self.openVulnerabilityHome)
        self.btn_https.clicked.connect(self.openHttpsHome)

        # --------------------- Password Evaluation -------------------------
        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password']))

        if self.lineEdit_password.text() == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_digits.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
            self.label_outputTimeToCrack.setText('no password')
            self.label_outputPasswordStrength.setText('no password')
            self.label_outputEntropy.setText('0 Bits')

        # Back button
        self.btn_backPassword.clicked.connect(self.openAdvancedUserHome)
        self.btn_backDic.clicked.connect(self.PasswordEvaluationHome)
        self.btn_backDigest.clicked.connect(self.openAdvancedUserHome)
        self.btn_backMalware.clicked.connect(self.openAdvancedUserHome)
        self.btn_backVulner.clicked.connect(self.openNetworkUserHome)
        self.btn_backHttps.clicked.connect(self.openNetworkUserHome)

        self.btn_iconEye.clicked.connect(self.btn_hidePwd)
        self.lineEdit_password.textChanged.connect(self.getPassword)
        self.btn_dicAttack.clicked.connect(self.Passowrd_Dictionary_Attack)
        ### --------------------- Dictionary Attack -------------------------
        self.btn_openDic.clicked.connect(lambda: PasswordEvaluation.open_file_wordlist(self))
        self.btn_clearDic.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_rockyou.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("rockyou.txt"))
        self.btn_crackstation.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("crackstation.txt"))
        
        # --------------------- Message Digest ------------------------------
        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        # Load the API key from the config file and display it in the textbox
        # with open('./data/init.conf', 'r') as config_file:
        #     self.lineAPIKey = config_file.read()
        #     if self.lineAPIKey != '':
        #         self.lineEdit_digest_2.setText(self.lineAPIKey)
        #     config_file.close()
        
        # Fetch API Key from config file
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'LineNotify' in config:
            line_api_key = config.get('LineNotify', 'LineAPIKEY')
            self.lineEdit_digest_2.setText(line_api_key)
            print(f'Line API Key: {line_api_key}')
        else:
            print('Section "LineNotify" does not exist in the config file.')
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description'])) 
        
        self.btn_openDigest.clicked.connect(self.openFileDialog)
        self.btn_clearDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_saveQR.clicked.connect(lambda: MessageDigest.saveQRCode(self))
        self.btn_lineAPI.clicked.connect(self.showBtnLine)
        self.btn_sendDigest.clicked.connect(lambda: MessageDigest.processLineKey(self))
        self.btn_copy.clicked.connect(lambda: MessageDigest.copyOutput(self))

        # --------------------- Malware Scan --------------------------------
        self.label_imagemalware.setPixmap(QPixmap("./assets/images/Defaultscan.png"))

        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'Malware' in config:
            self.api_vt_key = config.get('Malware', 'virustotal_api_key')
            self.api_url_scan = config.get('Malware', 'api_url_scan')
            self.api_file_scan = config.get('Malware', 'api_file_scan')
            self.api_file_analysis = config.get('Malware', 'api_file_analysis')
            print(f'VT API Key: {self.api_vt_key}')
            print(f'VT API URL: {self.api_url_scan}')
            print(f'VT API File: {self.api_file_scan}')
            print(f'VT API Analysis: {self.api_file_analysis}')
        else:
            print('Section "Malware" does not exist in the config file.')

        self.btn_scanMalware.clicked.connect(lambda: MalwareScanning.scanMalware(self))
        self.btn_openMalware.clicked.connect(lambda: MalwareScanning.openFileScanning(self))
        self.btn_clearMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_createReport.clicked.connect(lambda: MalwareScanning.createReport(self))
        self.btn_sendEmail.clicked.connect(lambda: MalwareScanning.sendEmail(self))

        # --------------------- Vulnerability -------------------------------
        self.btn_scanVulner.clicked.connect(lambda: VulnerabilityScanning.scanVulnerability(self))
        self.btn_clearVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        # --------------------- HTTPS Testing -------------------------------


    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advanceUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_password)
        self.btn_dicAttack.setVisible(False)
        self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
    
    def Passowrd_Dictionary_Attack(self):
        self.lineEdit_passwordDic.setText(self.lineEdit_password.text())
        self.stackedWidget.setCurrentWidget(self.page_dictionary)

    def openMalwareHome(self):
        self.stackedWidget.setCurrentWidget(self.page_malware)

    def openDigestHome(self):
        self.stackedWidget.setCurrentWidget(self.page_messageDigest)
        self.label_lineAPIDigest.setVisible(False)
        self.lineEdit_digest_2.setVisible(False)
        self.btn_sendDigest.setVisible(False)
        self.lineEdit_digest.textChanged.connect(lambda: self.checkFile_Text())
        
    def checkFile_Text(self):
        if os.path.exists(self.lineEdit_digest.text()) == True: # check if file exists
            print("File")
            self.state_detect = 1
            self.btn_md5.clicked.connect(lambda: MessageDigest.fileExtract(self, "md5", self.getPath()))
            self.btn_sha1.clicked.connect(lambda: MessageDigest.fileExtract(self, "sha1", self.getPath()))
            self.dropdown_sha2.activated.connect(lambda: MessageDigest.fileExtract(self, "sha2_" + self.dropdown_sha2.currentText(), self.getPath()))
            self.dropdown_sha3.activated.connect(lambda: MessageDigest.fileExtract(self, "sha3_" + self.dropdown_sha3.currentText(), self.getPath()))
        else:
            self.state_detect = 0
            print("Plaintext")
            self.btn_md5.clicked.connect(lambda: MessageDigest.hash(self, "md5"))
            self.btn_sha1.clicked.connect(lambda: MessageDigest.hash(self, "sha1"))
            self.dropdown_sha2.activated.connect(lambda: self.getdropdown_sha2())
            self.dropdown_sha3.activated.connect(lambda: self.getdropdown_sha3())

        # show Image QR Code
        self.btn_md5.clicked.connect(self.ShowImage_QR)
        self.btn_sha1.clicked.connect(self.ShowImage_QR)
        self.dropdown_sha2.activated.connect(self.ShowImage_QR)
        self.dropdown_sha3.activated.connect(self.ShowImage_QR)

    def openNetworkUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_networklUser)

    def openVulnerabilityHome(self):
        self.stackedWidget.setCurrentWidget(self.page_vulnerability)
    
    def openHttpsHome(self):
        self.stackedWidget.setCurrentWidget(self.page_https)
    
    def btn_hidePwd(self):
        PasswordEvaluation.show_hide_password(self)

    def getPassword(self):
        password = PasswordEvaluation.update(self)
        entropy = PasswordEvaluation.calculate_entropy(self, password)

        self.label_outputEntropy.setText(f'{entropy:.0f} bits')

        if entropy == 0:
            self.label_outputEntropy.setText(f'-- Bits')
            self.label_outputPasswordStrength.setText('')
        elif entropy > 999:
            self.label_outputEntropy.setText(f'~NaN Bits')
        else:
            self.label_outputEntropy.setText(f'~{entropy:.0f} Bits')
        
        length = len(password)        
        if length < 8:
            self.label_outputPasswordStrength.setText('So very, very bad Password')
            if length == 0:
                self.label_outputPasswordStrength.setText('')
        else : 
            if entropy < 50 :
                self.label_outputPasswordStrength.setText('Weak password')
            elif entropy < 80 :
                self.label_outputPasswordStrength.setText('Medium strength')
            else:
                self.label_outputPasswordStrength.setText('Good password')
        
        # Show length of password
        self.label_lengthOfPassword.setText(f'{length} Chars')

        # Show time to crack
        self.label_outputTimeToCrack.setText(f'{PasswordEvaluation.time_to_Crack(self, password)}')

        # Check if password is in the list of weak passwords
        PasswordEvaluation.check_common_password(self, password, self.nordpass_common_passwords)
    
    def getdropdown_sha2(self):
        MessageDigest.hash(self, "sha2_" + self.dropdown_sha2.currentText())
        self.algorithm = 'SHA2-' + self.dropdown_sha2.currentText()
        self.dropdown_sha3.setCurrentIndex(0) 

    def getdropdown_sha3(self):
        MessageDigest.hash(self, "sha3_" + self.dropdown_sha3.currentText())
        self.algorithm = 'SHA3-' + self.dropdown_sha3.currentText()
        self.dropdown_sha2.setCurrentIndex(0)

    def openFileDialog(self):
        path = MessageDigest.open_file_dialog(self)
        #print(type(path)) # <class 'pathlib.WindowsPath'>

        # try except to check if file exists
        try:
            if path.exists() == True: # check if file exists
                print(f"File exists at: {path.exists()}" + " ++")
        except AttributeError as e:
            print(f"Empty file or Not found")

        self.setPath(path)
    
    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path

    def ShowImage_QR(self):
        if self.lineEdit_outputTextDigest.text() != '':
            MessageDigest.qrCodeGenerator(self, self.lineEdit_outputTextDigest.text())
            MessageDigest.ShowImage_QR(self)

    def showBtnLine(self):
        self.label_lineAPIDigest.setVisible(True)
        self.lineEdit_digest_2.setVisible(True)
        self.btn_sendDigest.setVisible(True)


from PyQt6.QtCore import QFileInfo

class PasswordEvaluation(QDialog):

    hide = True
    
    def __init__(self):
        super(PasswordEvaluation, self).__init__()

    def clear(self):
        self.lineEdit_inputFileDic.setText('')

    def show_hide_password(self):
        if self.hide == True:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password) 
            self.hide = False
            self.btn_iconEye.setIcon(self.hide_icon)
            
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Normal) 
            self.hide = True
            self.btn_iconEye.setIcon(self.unhide_icon)

    def check_common_password(self, password, nordpass_common_passwords):
        if password == '':
            self.label_outputEntropy.setText('')
            self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
            self.label_outputSearchNordPass.setStyleSheet("color: rgba(0, 143, 255, 255);")
            self.label_outputPasswordStrength.setText('')
            self.btn_dicAttack.setVisible(False)
        else:
            if password in self.nordpass_common_passwords:
                print(self.nordpass_common_passwords.index(password))
                self.label_outputSearchNordPass.setText('Found in the top 200 most common passwords by NordPass')
                self.label_outputSearchNordPass.setStyleSheet("color: red;")
                self.btn_dicAttack.setVisible(False)
            else:
                self.label_outputSearchNordPass.setText('Not found in the list')
                self.label_outputSearchNordPass.setStyleSheet("color: rgba(0, 255, 143, 255);")
                self.btn_dicAttack.setVisible(True) if self.label_outputSearchNordPass.text() == '' \
                    or self.label_outputSearchNordPass.text() == 'Not found in the list' else self.btn_dicAttack.setVisible(False)

    def update(self):

        self.chk_length.setChecked(False)
        self.chk_digits.setChecked(False)
        self.chk_upper.setChecked(False)
        self.chk_lower.setChecked(False)
        self.chk_special.setChecked(False)
        
        # Get password real time
        password = self.lineEdit_password.text()

        for char in password:
            if char.isdigit():
                self.chk_digits.setChecked(True)
                self.chk_digits.setIcon(self.check_icon)
            elif char.isupper():
                self.chk_upper.setChecked(True)
                self.chk_upper.setIcon(self.check_icon)
            elif char.islower():
                self.chk_lower.setChecked(True)
                self.chk_lower.setIcon(self.check_icon)
            else:
                self.chk_special.setChecked(True)
                self.chk_special.setIcon(self.check_icon)
                
            if len(self.lineEdit_password.text()) >= 8:
                self.chk_length.setChecked(True)
                self.chk_length.setIcon(self.check_icon)
        return password

    def calculate_entropy(self, password):
        
        if password == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_digits.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            return 0
    
        possible_characters = 0
        if self.chk_digits.isChecked(): # 0-9
            possible_characters += 10
        if self.chk_upper.isChecked(): # A-Z
            possible_characters += 26
        if self.chk_lower.isChecked(): # a-z
            possible_characters += 26
        if self.chk_special.isChecked(): # !@#$%^&*()_+-=
            possible_characters += 32
        # Calculate the entropy using the formula log2(possible_characters^password_length)
        entropy = log2(possible_characters**len(password))
        return entropy
    
    def time_to_Crack(self, password):
        try:
            if password == '':
                self.chk_length.setIcon(self.warning_icon)
                self.chk_digits.setIcon(self.warning_icon)
                self.chk_upper.setIcon(self.warning_icon)
                self.chk_lower.setIcon(self.warning_icon)
                self.chk_special.setIcon(self.warning_icon)
                return 0
        
            possible_characters = 0
            if self.chk_digits.isChecked(): # 0-9
                possible_characters += 10
            if self.chk_upper.isChecked(): # A-Z
                possible_characters += 26
            if self.chk_lower.isChecked(): # a-z
                possible_characters += 26
            if self.chk_special.isChecked(): # !@#$%^&*()_+-=
                possible_characters += 32

            combinations = possible_characters ** len(password)
            KPS_2020 = 17042497.3 # 17 Million
            
            seconds = combinations / KPS_2020
            seconds = f'{seconds:.0f}'
            seconds = int(seconds)

            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            weeks, days = divmod(days, 7)
            months, weeks = divmod(weeks, 4)
            years, months = divmod(months, 12)
            
            time_parts = []
            if years > 0:
                time_parts.append(f"{years} year{'s' if years != 1 else ''}")
            if months > 0:
                time_parts.append(f"{months} month{'s' if months != 1 else ''}")
            if weeks > 0:
                time_parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
            if days > 0:
                time_parts.append(f"{days} day{'s' if days != 1 else ''}")
            if hours > 0:
                time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if seconds > 0:
                time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
            if years > 10:
                time_parts = ['more than 10 years']
            if time_parts == []:
                time_parts = ['less than a second']

            # Show time to crack 2 largest units
            if len(time_parts) <= 2:
                return " ".join(time_parts)
            
            largest_units = time_parts[:2]
            return " ".join(largest_units)
        
        except OverflowError as e:
            print(f"Error: {e}")
        except UnboundLocalError as e:
            print(f"Error: {e}")
    
    def open_file_wordlist(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
           "Open Wordlist File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt)",
        )
        file_name = QFileInfo(filepath).fileName()
        if filepath:
            # Process the selected filename
            print("Selected file:", filepath)
            
            if filepath:
                path = Path(filepath)
                #self.lineEdit_inputFileDic.setText(str(path)) # show path file
                self.lineEdit_inputFileDic.setText(file_name) # show file name
                if path.exists() != True: # check if file exists 
                    print(f"File exists at: {path.exists()}")
                print(f"Get file at: {path}") 

                return path

class MessageDigest(QDialog):

    def __init__(self):
        super(MessageDigest, self).__init__()
        
    def saveAPIKey(self):
        self.lineAPIKey = self.lineEdit_digest_2.text()
        print(self.lineAPIKey)
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)

        if 'LineNotify' in config:
            config.set('LineNotify', 'LineAPIKEY', str(self.lineAPIKey))
            print(f'Set API KEY: {self.lineAPIKey}')
        else:
            print('Section "LineNotify" does not exist in the config file.')

        with open(configFilePath, 'w') as configfile:
            config.write(configfile)

    def clear (self):
        self.lineEdit_digest.setText('')
        self.label_QRCode.clear()
        self.dropdown_sha2.setCurrentIndex(0)
        self.dropdown_sha3.setCurrentIndex(0)
        self.label_lineAPIDigest.setVisible(False)
        self.lineEdit_digest_2.setVisible(False)
        self.btn_sendDigest.setVisible(False)
        self.lineEdit_digest_2.setText('')
        self.lineEdit_outputTextDigest.setText('')
        self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid black;")
        self.lineEdit_outputTextDigest.setPlaceholderText('')
        self.label_type.setText('Type')
        #fetch API Key from config file
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'LineNotify' in config:
            line_api_key = config.get('LineNotify', 'LineAPIKEY')
            self.lineEdit_digest_2.setText(line_api_key)
            print(f'Line API Key: {line_api_key}')
        else:
            print('Section "LineNotify" does not exist in the config file.')

    def hash(self, type):
        #print(self.dropdown_sha2.currentText())
        if type == "md5":
            self.lineEdit_outputTextDigest.setText(MessageDigest.md5(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'MD5'
            
        elif type == "sha1":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha1(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA-1'
            
        elif type == "sha2_224 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha224(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-224'
            
        elif type == "sha2_256 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha256(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-256'
            
        elif type == "sha2_384 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha384(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-384'
            
        elif type == "sha2_512 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha512(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-512'
            
        elif type == "sha3_224 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_224(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-224'
            
        elif type == "sha3_256 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_256(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-256'
            
        elif type == "sha3_384 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_384(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-384'
            
        elif type == "sha3_512 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_512(self, self.lineEdit_digest.text())) \
                if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-512'
            

        self.label_type.setText(self.algorithm) if self.lineEdit_digest.text() != '' else self.label_type.setText('Type')
        # reset copy button
        self.btn_copy.setText('Copy')

    def qrCodeGenerator(self, hash):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(hash)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("./data/MessageDigest-QRCode.png")
        return img
        
    def ShowImage_QR(self):
        imagePath = "./data/MessageDigest-QRCode.png"
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(200)
        self.label_QRCode.setPixmap(pixmap)
        
    def fileExtract(self, type, path):
        print(type)
        if type == "md5":
            MessageDigest.fileHash(self, "md5", path)
        elif type == "sha1":
            MessageDigest.fileHash(self, "sha1", path)
        elif type == "sha2_224 BIT":
            MessageDigest.fileHash(self, "sha224", path)
        elif type == "sha2_256 BIT":
            MessageDigest.fileHash(self, "sha256", path)
        elif type == "sha2_384 BIT":
            MessageDigest.fileHash(self, "sha384", path)
        elif type == "sha2_512 BIT":
            MessageDigest.fileHash(self, "sha512", path)
        elif type == "sha3_224 BIT":
            MessageDigest.fileHash(self, "sha3_224", path)
        elif type == "sha3_256 BIT":
            MessageDigest.fileHash(self, "sha3_256", path)
        elif type == "sha3_384 BIT":
            MessageDigest.fileHash(self, "sha3_384", path)
        elif type == "sha3_512 BIT":
            MessageDigest.fileHash(self, "sha3_512", path)

        # Show Image QR Code
        self.btn_md5.clicked.connect(self.ShowImage_QR)
        self.btn_sha1.clicked.connect(self.ShowImage_QR)
        self.dropdown_sha2.activated.connect(self.ShowImage_QR)
        self.dropdown_sha3.activated.connect(self.ShowImage_QR)

    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            # self,
            # "Select a File", 
            # "D:\\icons\\avatar\\", 
            # "Images (*.png *.jpg)"
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt);;All Files (*)" # filter file type text but can select all file
        )
        if filename:
            path = Path(filename)
            self.lineEdit_digest.setText(str(path))
            if path.exists() != True: # check if file exists 
                print(f"File exists at: {path.exists()}")
            print(f"Get file at: {path}") 

            return path
    
    # File Hashing -----------------------------------------------
    def fileHash(self, type, path):
        text_type = type
        if "_" in type:
            text_type = text_type.replace("_", " ")
        self.label_type.setText(text_type.upper())

        if type == "md5":
            init_hash = hashlib.md5()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha1":
            init_hash = hashlib.sha1()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha224":
            init_hash = hashlib.sha224()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha256":
            init_hash = hashlib.sha256()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha384":
            init_hash = hashlib.sha384()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha512":
            init_hash = hashlib.sha512()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_224":
            init_hash = hashlib.sha3_224()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_256":
            init_hash = hashlib.sha3_256()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_384":
            init_hash = hashlib.sha3_384()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_512":
            init_hash = hashlib.sha3_512()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')
        
        

    def saveQRCode(self):
        pathfile, ok = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Images (*.png *.jpg)")
        
        # Check if a filename was provided
        if pathfile: # show place to save
            print("Save at: ", pathfile)
            # Save QR-Code with pixmap at pathfile
            if not self.label_QRCode.pixmap().isNull():
                # Save the pixmap to the specified file path
                self.label_QRCode.pixmap().save(pathfile, 'PNG')
                # Set the text of the save button to "SAVED!" to indicate successful save
                self.btn_saveQR.setText("SAVED!")
            else:
                print("Error: QR-Code is Not Generated")
        else:
            print("Error: No file name specified")
    
    # Type of Hashing ------------------------------------------
    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def sha1(self, data):
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    def sha224(self, data):
        return hashlib.sha224(data.encode('utf-8')).hexdigest()

    def sha256(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def sha384(self, data):
        return hashlib.sha384(data.encode('utf-8')).hexdigest()

    def sha512(self, data):
        return hashlib.sha512(data.encode('utf-8')).hexdigest()

    def sha3_224(self, data):
        return hashlib.sha3_224(data.encode('utf-8')).hexdigest()

    def sha3_256(self, data):
        return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

    def sha3_384(self, data):
        return hashlib.sha3_384(data.encode('utf-8')).hexdigest()

    def sha3_512(self, data):
        return hashlib.sha3_512(data.encode('utf-8')).hexdigest()
    
    def processLineKey(self):
        if self.lineEdit_digest.text() == '':
            print("Data to send Empty")
            self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid red;")
            self.lineEdit_outputTextDigest.setPlaceholderText("Empty")
            return 
        type = self.label_type.text()
        api_key = '6tA0qnCW3qp6jtAMEVyL2T3CIINiEusqZ3nJH5kuzKL'
        message = self.lineEdit_outputTextDigest.text() + "\nHash Algorithms: " + type
        token = self.lineEdit_digest_2.text()
        try:
            if token != '':
                getQR = "./data/MessageDigest-QRCode.png"
                url = "https://notify-api.line.me/api/notify"

                headers = {"Authorization": "Bearer " + token}
                payload = {"message": message}

                with open(getQR, "rb") as image_file:
                    files = {"imageFile": image_file}
                    response = requests.post(url, headers=headers, params=payload, files=files)
                
                if response.status_code == 200:
                    MessageDigest.saveAPIKey(self) # save api key to file init.conf
                    print("Image sent successfully!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid green;")
                elif response.status_code == 400:
                    print("Bad request!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid red;")
                elif response.status_code == 401:
                    print("Invalid access token!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid orange;")
                elif response.status_code == 500:
                    print("Server error!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid yellow;")
                else:
                    print("Process over time.")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid grey;")
            else:
                self.lineEdit_digest_2.setStyleSheet("border: 1px solid red;")
        except UnicodeEncodeError as e:
            print("Cannot send message to LINE")
            
    def copyOutput(self):
        clipboard = self.lineEdit_outputTextDigest.text()
        if clipboard == '':
            self.lineEdit_outputTextDigest.setPlaceholderText("Empty")
            self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid red;")
        else:
            self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid green;")
            self.btn_copy.setText("Copied!")
            pyperclip.copy(clipboard)

class MalwareScanning():

    def __init__(self):
        super(MalwareScanning, self).__init__()
    
    def clear(self):
        print("Clear")
        self.lineEdit_malware.setText('')
        self.lineEdit_malware.setStyleSheet("border: 1px solid black;")
        self.lineEdit_malware.setPlaceholderText('ex. https:// or file')
        self.label_maliciousResult.setText('0')
        self.label_suspiciousResult.setText('0')
        self.label_undetectedResult.setText('0')
        self.label_finalURLResurlt.setText('-')
        self.label_tidResult.setText('-')
        self.label_typeMalwareResult.setText('-')
        self.label_sha256Result.setText('-')
        self.label_sizeResult.setText('-')
        self.label_malicious.setStyleSheet("background-color: white;")
        self.label_suspicious.setStyleSheet("background-color: white;")
        self.label_undetected.setStyleSheet("background-color: white;")
        self.label_imagemalware.setPixmap(QPixmap("./assets/images/Defaultscan.png"))
        self.btn_createReport.setText('Create Report')
        self.btn_sendEmail.setText('Send Email')



    def scanMalware(self):
        print("Scan Malware")
        if self.lineEdit_malware.text() == '':
            print("Data to send Empty")
            self.lineEdit_malware.setStyleSheet("border: 1px solid red;")
            self.lineEdit_malware.setPlaceholderText("Empty")
            return
        
        if os.path.exists(self.lineEdit_malware.text()) == True:
            print("File Scan")
            MalwareScanning.FileScan(self)
        elif self.lineEdit_malware.text().startswith('https://') or self.lineEdit_malware.text().startswith('http://'):
            print("URL Scan")
            MalwareScanning.URLScan(self)
        else:
            print("Invalid File or URL")
            self.lineEdit_malware.setStyleSheet("border: 1px solid red;")
            self.lineEdit_malware.setText("")
            self.lineEdit_malware.setPlaceholderText("Invalid URL or File")
    
    def FileScan(self):
        print("File Scan")
        input = self.lineEdit_malware.text()
        url = self.api_file_scan
        files = { "file": open(input, "rb") }
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_vt_key,
        }

        response = requests.post(url, files=files, headers=headers)

        print(response.text)
        # response code detect
        if response.status_code == 200:
            print("File Scan Success")
            self.lineEdit_malware.setStyleSheet("border: 1px solid green;")
            self.lineEdit_malware.setPlaceholderText("File Scan Success")
        elif response.status_code == 400:
            print("Bad request!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid red;")
            self.lineEdit_malware.setPlaceholderText("Bad request!")
        elif response.status_code == 401:
            print("Invalid access token!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid orange;")
            self.lineEdit_malware.setPlaceholderText("Invalid access token!")
        elif response.status_code == 500:
            print("Server error!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid yellow;")
            self.lineEdit_malware.setPlaceholderText("Server error!")
        
        id = response.json()['data']['id']
        print(id)
        MalwareScanning.fileAnalyses(self, id)

    def fileAnalyses(self, id):
        url = self.api_file_analysis + "/" + id

        headers = {
            "accept": "application/json",
            "x-apikey": self.api_vt_key
        }

        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            print("File Analyses Success")
        elif response.status_code == 400:
            print("Bad request!")
        elif response.status_code == 401:
            print("Invalid access token!")
        elif response.status_code == 500:
            print("Server error!")
        id = response.json()['meta']['file_info']['sha256']
        print(id)
        MalwareScanning.fileReport(self, id)
    
    def fileReport(self, id):
        url = self.api_file_scan + "/" + id

        headers = {
            "accept": "application/json",
            "x-apikey": self.api_vt_key
        }

        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            print("File Report Success")
        elif response.status_code == 400:
            print("Bad request!")
        elif response.status_code == 401:
            print("Invalid access token!")
        elif response.status_code == 500:
            print("Server error!")

        MalwareScanning.showData(self, response, type='file')
        
    def URLScan(self):
        print("URL Scan")
        input = self.lineEdit_malware.text()
        url = self.api_url_scan

        payload = { "url": input }
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_vt_key,
            "content-type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)
        print(response.text)

        # response code detect
        if response.status_code == 200:
            print("URL Scan Success")
            self.lineEdit_malware.setStyleSheet("border: 1px solid green;")
            self.lineEdit_malware.setPlaceholderText("URL Scan Success")
        elif response.status_code == 400:
            print("Bad request!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid red;")
            self.lineEdit_malware.setPlaceholderText("Bad request!")
        elif response.status_code == 401:
            print("Invalid access token!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid orange;")
            self.lineEdit_malware.setPlaceholderText("Invalid access token!")
        elif response.status_code == 500:
            print("Server error!")
            self.lineEdit_malware.setStyleSheet("border: 1px solid yellow;")
            self.lineEdit_malware.setPlaceholderText("Server error!")

        id = response.json()['data']['id'].split('-')[1]
        print(id)
        MalwareScanning.URLReport(self, id)

    def URLReport(self, id):
        url = self.api_url_scan + "/" + id
        print(url)
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_vt_key
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            print("URL Report Success")
        elif response.status_code == 400:
            print("Bad request!")
        elif response.status_code == 401:
            print("Invalid access token!")
        elif response.status_code == 500:
            print("Server error!")
        
        MalwareScanning.showData(self, response, type='url')

    def showData(self, response, type):
        if type == 'file':
            # rename label
            self.label_finalURL.setText('File Name')
            self.label_tid.setText('File Type')
            self.label_typeMalware.setText('Scan Type')
            self.label_sha256.setText('SHA-256')
            self.label_size.setText('File Size')
            # show data
            
            try:
                
                maliciouse = response.json()['data']['attributes']['last_analysis_stats']['malicious']
                suspicious = response.json()['data']['attributes']['last_analysis_stats']['suspicious']
                undetected = response.json()['data']['attributes']['last_analysis_stats']['undetected']

                self.label_maliciousResult.setText(str(maliciouse))
                self.label_suspiciousResult.setText(str(suspicious))
                self.label_undetectedResult.setText(str(undetected))

                size = response.json()['data']['attributes']['size']
                if size < 1024:
                    size = str(size) + " Bytes"
                elif size < 1048576:
                    size = str(round(size/1024, 2)) + " KB"
                elif size < 1073741824:
                    size = str(round(size/1048576, 2)) + " MB"
                elif size < 1099511627776:
                    size = str(round(size/1073741824, 2)) + " GB"
                else:
                    size = str(round(size/1099511627776, 2)) + " TB"
                
                self.label_sizeResult.setText(size)\
                    if response.json()['data']['attributes']['size'] != 0 else self.label_sizeResult.setText('-')

                self.label_finalURLResurlt.setText(response.json()['data']['attributes']['names'][0] ) \
                    if response.json()['data']['attributes']['names'][0] != [] else self.label_finalURLResurlt.setText('-')
                
                
                filetype = response.json()['data']['attributes']['type_description']
                self.label_tidResult.setText(filetype) \
                    if filetype != '' else self.label_tidResult.setText('-')
                
                scantype = response.json()['data']['type']
                self.label_typeMalwareResult.setText(scantype) \
                    if scantype != '' else self.label_typeMalwareResult.setText('-')
                
                hashfile =  response.json()['data']['attributes']['sha256']
                self.label_sha256Result.setText(hashfile) \
                    if hashfile != '' else self.label_sha256Result.setText('-')
                
            except KeyError as e:
                print("Key Error" + str(e))

            if int(self.label_maliciousResult.text()) > 0:
                print("Malware")
                self.label_imagemalware.setPixmap(QPixmap("./assets/images/FileMalware.png"))
                
            else:
                print("No Malware")
                self.label_imagemalware.setPixmap(QPixmap("./assets/images/FileCheck.png"))
                
                
        
        if type == 'url':
            # rename label
            self.label_finalURL.setText('URL')
            self.label_tid.setText('TLD')
            self.label_typeMalware.setText('Scan Type')
            self.label_sha256.setText('SHA-256')
            self.label_size.setText('Site Name')
            # show data
            try:

                maliciouse = response.json()['data']['attributes']['last_analysis_stats']['malicious']
                suspicious = response.json()['data']['attributes']['last_analysis_stats']['suspicious']
                undetected = response.json()['data']['attributes']['last_analysis_stats']['undetected']

                self.label_maliciousResult.setText(str(maliciouse))
                self.label_suspiciousResult.setText(str(suspicious))
                self.label_undetectedResult.setText(str(undetected))
                
                destination_url = response.json()['data']['attributes']['last_final_url']
                self.label_finalURLResurlt.setText(destination_url) \
                    if destination_url != '' else self.label_finalURLResurlt.setText('-')
                
                tld_url = response.json()['data']['attributes']['tld']
                self.label_tidResult.setText(tld_url) \
                    if tld_url != '' else self.label_tidResult.setText('-')

                scan_type = response.json()['data']['type'].upper()
                self.label_typeMalwareResult.setText(scan_type) \
                    if scan_type != '' else self.label_typeMalwareResult.setText('-')
                
                hash_url = response.json()['data']['attributes']['last_http_response_content_sha256']
                self.label_sha256Result.setText(hash_url) \
                    if hash_url != '' else self.label_sha256Result.setText('-')
                
                #self.label_sizeResult.setText(response.json()['data']['attributes']['title'])
                site_name = response.json()['data']['attributes']['html_meta']['title'][0] 
                self.label_sizeResult.setText(site_name) \
                    if site_name != [] else self.label_sizeResult.setText('-')
                
            except KeyError as e:
                print("Key Error" + str(e))
                try:
                    site_name = response.json()['data']['attributes']['last_final_url'].split('/')[2] 
                except KeyError as e:
                    site_name = "-"
                print(site_name)
                self.label_sizeResult.setText(site_name) \
                    if site_name != [] else self.label_sizeResult.setText('-')

            if int(self.label_maliciousResult.text()) > 0:
                print("Malware")
                malware_logo = QPixmap("./assets/images/URLMalware.png")
                self.label_imagemalware.setPixmap(malware_logo)
                #self.label_malicious.setStyleSheet("background-color: red;")
                # if int(self.label_suspiciousResult.text()) > 0:
                #     self.label_suspicious.setStyleSheet("background-color: orange;")
                # if int(self.label_undetectedResult.text()) > 0:
                #     self.label_undetected.setStyleSheet("background-color: gray;")
            else:
                print("No Malware")
                urlcheck_logo = QPixmap("./assets/images/URLCheck.png")
                self.label_imagemalware.setPixmap(urlcheck_logo)
                # self.label_malicious.setStyleSheet("background-color: green;")
                # self.label_suspicious.setStyleSheet("background-color: green;")
                # self.label_undetected.setStyleSheet("background-color: green;")


    def createReport(self):
        print("Create Report")
        pdf_file = "./data/MalwareReport.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        c.setLineWidth(.3)
        c.setFont('Helvetica', 12)
        c.setTitle('Malware Report')
        c.setAuthor("SecGizmo")
        c.setSubject("Malware Analysis")
        c.setKeywords("Python, PDF, Malware Analysis, VirusTotal, SecGizmo")
        c.setCreator("SecGizmo")
        c.pageHasData()
        c.drawImage("./assets/images/ISAN.png", 175, 650, width=255, height=145)
        c.drawString(30, 750, 'Malware Report')
        c.drawString(30, 735, 'SecGizmo')
        c.drawString(480, 750, "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d")))
        c.line(480,747,580,747)
        c.setFont('Helvetica', 20)
        c.drawString(245, 725, 'Malware Analysis')
        c.setFont('Helvetica', 12)
        c.drawString(30, 703, 'Malicious: ' + self.label_maliciousResult.text())
        c.drawString(30, 683, 'Suspicious: ' + self.label_suspiciousResult.text())
        c.drawString(30, 663, 'Undetected: ' + self.label_undetectedResult.text())
        c.drawString(30, 643, 'Final URL: ' + self.label_finalURLResurlt.text())
        c.drawString(30, 623, 'TLD: ' + self.label_tidResult.text())
        c.drawString(30, 603, 'Scan Type: ' + self.label_typeMalwareResult.text())
        c.drawString(30, 583, 'SHA-256: ' + self.label_sha256Result.text())
        c.drawString(30, 563, 'Size: ' + self.label_sizeResult.text())
        c.showPage()
        c.save()
        print(f"PDF created: {pdf_file.split('/')[-1]}")
        self.btn_createReport.setText("Created!")

        # prepare send email
        self.lineEdit_malware.setText('')
        self.lineEdit_malware.setPlaceholderText('ex. enter your email')
        self.lineEdit_malware.setStyleSheet("border: 2px solid Green;")
        self.lineEdit_malware.textChanged.connect(lambda: MalwareScanning.update(self))

    def sendEmail(self):
        print("Send Email")
        email = self.lineEdit_malware.text()
        if email == '':
            print("Email Empty")
            self.lineEdit_malware.setStyleSheet("border: 2px solid red;")
            self.lineEdit_malware.setPlaceholderText("Empty")
            return
        print("final email = " + email)
        self.btn_sendEmail.setText("Sent!")

    def openFileScanning(self):
        print("Open File")
        #pass
        filepath, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            os.getcwd(), 
            "All files (*.*)"
        )
        if filepath:
            path = Path(filepath)
            self.lineEdit_malware.setText(str(path))
            if path.exists() != True: # check if file exists 
                print(f"File exists at: {path.exists()}")
            print(f"Get file at: {path}")

            return path
        
    def update(self):
        input_email = self.lineEdit_malware.text()
        if '@' not in input_email:
            print("Invalid Email")
            self.lineEdit_malware.setStyleSheet("border: 2px solid orange;")
            self.lineEdit_malware.setPlaceholderText("Invalid Email")
            return
        else:
            print("Email Correct")
            self.lineEdit_malware.setStyleSheet("border: 2px solid green;")
            self.lineEdit_malware.setPlaceholderText("Email Correct")

        print(input_email)

class VulnerabilityScanning():
    def __init__(self):
        super(MalwareScanning, self).__init__()
    
    def clear(self):
        self.lineEdit_vulner.setText('')
        
    def PrepareInput(self):
        input = self.lineEdit_vulner.text()
        stmt_nmap = ("nmap %s" %input).split(" ")

        # Remove any leading `https://` or `http://` from the target URL.
        if stmt_nmap[1].startswith("https://"):
            stmt_nmap[1] = stmt_nmap[1].replace("https://", "")
        elif stmt_nmap[1].startswith("http://"):
            stmt_nmap[1] = stmt_nmap[1].replace("http://", "")
            
        print(stmt_nmap[:2])
        craft_command = " ".join(stmt_nmap[:2])
        self.lineEdit_vulner.setPlaceholderText(craft_command)
        return craft_command

    def scanVulnerability(self):
        if self.lineEdit_vulner.text() == '':
            print("Data to send Empty")
            self.lineEdit_vulner.setStyleSheet("border: 1px solid red;")
            self.lineEdit_vulner.setPlaceholderText("Empty")
            return
        else:
            self.lineEdit_vulner.setStyleSheet("border: 2px solid green;")
            self.lineEdit_vulner.setPlaceholderText("Correct")
        stmt_nmap = VulnerabilityScanning.PrepareInput(self)
        #print("nmap " + input)
        if stmt_nmap.startswith('nmap'):
            execute_command = stmt_nmap 
            os.system(execute_command)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    #window.setFixedHeight(700)
    #window.setFixedWidth(1200)
    #window.setMinimumSize(1200, 700)
    #window.setMaximumSize(1200, 700)
    window.show()

    try:
        sys.exit(app.exec())     
    except SystemExit:
        print('Closing Window...')