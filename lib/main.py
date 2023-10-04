
import sys
import os
import json
import configparser

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.uic import loadUi

# Import all the classes from the lib folder
from PasswordEvaluation import *
from MessageDigest import *
from MalwareScanning import *
from VulnerabilityScanning import *
from HSTSTesting import *

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
        loadUi("./assets/ui/main.ui", self)

        # initialize Icon
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
        self.setWindowIcon(QIcon("./assets/icons/icons8-stan-marsh-96.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")
        self.label_logo = QPixmap("./assets/icons/icons8-stan-marsh-96.png")
        self.image_main = QPixmap("./assets/images/main.png")

        # Event Back Button
        #self.btn_backPassword.clicked.connect(self.openAdvancedUserHome)
        #self.btn_backDic.clicked.connect(self.PasswordEvaluationHome)
        #self.btn_backDigest.clicked.connect(self.openAdvancedUserHome)
        #self.btn_backMalware.clicked.connect(self.openAdvancedUserHome)
        #self.btn_backVulner.clicked.connect(self.openNetworkUserHome)
        #self.btn_backHttps.clicked.connect(self.openNetworkUserHome)

        # -------------------- Home ---------------------------------------
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.mainpage))
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)

        # -------------------- Advance User ---------------------------------
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        # ------------------------------------------------------------------
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)
        self.btn_malware.clicked.connect(self.openMalwareHome)
        self.btn_MSdigest.clicked.connect(self.openDigestHome)

        # --------------------- Network User --------------------------------
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)
        # ------------------------------------------------------------------
        self.btn_vulner.clicked.connect(self.openVulnerabilityHome)
        self.btn_hsts.clicked.connect(self.openHttpsHome)

        # --------------------- Password Evaluation -------------------------

        # Initialize the password field
        self.btn_showPassword.setIcon(self.hide_icon)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password']))

        # Check if the password field is empty
        if self.lineEdit_password.text() == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_numeric.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
            self.label_outputTimeToCrack.setText('no password')
            self.label_outputPasswordStrength.setText('no password')
            self.label_outputEntropy.setText('0 Bits')

        # Detect changes in the password field
        self.lineEdit_password.textChanged.connect(self.getPassword)
        
        # Event Button Page Password Evaluation
        self.btn_showPassword.clicked.connect(self.btn_hidePwd)
        self.btn_dictAttack.clicked.connect(self.Passowrd_Dictionary_Attack)

        ### --------------------- Dictionary Attack -------------------------

        # Event Button Page Dictionary Attack
        self.btn_browseDict.clicked.connect(lambda: PasswordEvaluation.open_file_wordlist(self))
        self.btn_clearDict.clicked.connect(lambda: PasswordEvaluation.clear(self))
        #self.btn_rockyou.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("rockyou.txt"))
        #self.btn_crackstation.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("crackstation.txt"))
        
        # --------------------- Message Digest ------------------------------

        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
    
        # Fetch API Key from config file
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'LineNotify' in config:
            line_api_key = config.get('LineNotify', 'LineAPIKEY')
            self.lineEdit_tokenMSDigest.setText(line_api_key)
            print(f'Line API Key: {line_api_key}')
        else:
            print('Section "LineNotify" does not exist in the config file.')
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description'])) 
        
        # Event Button Page Message Digest
        self.btn_browseMSDigest.clicked.connect(self.openFileDialog)
        self.btn_clearMSDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_saveQR.clicked.connect(lambda: MessageDigest.saveQRCode(self))
        self.btn_lineAPI.clicked.connect(self.showBtnLine)
        self.btn_sendMSDigest.clicked.connect(lambda: MessageDigest.processLineKey(self))
        self.btn_copy.clicked.connect(lambda: MessageDigest.copyOutput(self))

        # --------------------- Malware Scan --------------------------------

        # Initialize the image
        self.image_analysis.setPixmap(QPixmap("./assets/images/Defaultscan.png"))

        # Fetch API Key from config file
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

        # Event Button Page Malware Scan
        self.btn_scanMalware.clicked.connect(lambda: MalwareScanning.scanMalware(self))
        self.btn_browseMalware.clicked.connect(lambda: MalwareScanning.openFileScanning(self))
        self.btn_clearMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_createReport.clicked.connect(lambda: MalwareScanning.createReport(self))
        self.btn_sendEmail.clicked.connect(lambda: MalwareScanning.sendEmail(self))

        # --------------------- Vulnerability -------------------------------

        # Event Button Page Vulnerability
        self.btn_scanVulner.clicked.connect(lambda: VulnerabilityScanning.scanVulnerability(self))
        self.btn_clearVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))


        # --------------------- HTTPS Testing -------------------------------

        # Event Button Page HTTPS Testing
        self.btn_scanHsts.clicked.connect(lambda: HSTSTesting.scanHSTS(self))
        #self.btn_clearHttps.clicked.connect(lambda: HSTSTesting.clear(self))

    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advancedUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_passwordEvaluation)
        self.btn_dictAttack.setVisible(False)
        self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
    
    def Passowrd_Dictionary_Attack(self):
        self.lineEdit_passwordDic.setText(self.lineEdit_password.text())
        self.stackedWidget.setCurrentWidget(self.page_dictionary)

    def openMalwareHome(self):
        self.stackedWidget.setCurrentWidget(self.page_malware)

    def openDigestHome(self):
        self.stackedWidget.setCurrentWidget(self.page_messageDigest)
        self.label_lineAPIDigest.setVisible(False)
        self.lineEdit_tokenMSDigest.setVisible(False)
        self.btn_sendMSDigest.setVisible(False)
        self.lineEdit_MSdigest.textChanged.connect(lambda: self.checkFile_Text())
        
    def checkFile_Text(self):
        if os.path.exists(self.lineEdit_MSdigest.text()) == True: # check if file exists
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
        self.stackedWidget.setCurrentWidget(self.page_networkUser)

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

        # Check if password is in the list of weak passwords
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
        if self.lineEdit_outputTextMSDigest.text() != '':
            MessageDigest.qrCodeGenerator(self, self.lineEdit_outputTextMSDigest.text())
            MessageDigest.ShowImage_QR(self)

    def showBtnLine(self):
        self.label_lineAPIDigest.setVisible(True)
        self.lineEdit_tokenMSDigest.setVisible(True)
        self.btn_sendMSDigest.setVisible(True)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()

    try:
        sys.exit(app.exec())     
    except SystemExit:
        print('Closing Window...')