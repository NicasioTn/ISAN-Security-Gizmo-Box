# Form implementation generated from reading ui file 'd:\ISAN Security Gizmo Box\backup\Message_Digest.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 700)
        Form.setStyleSheet("background-color: rgba(9,36,43,255)")
        self.name_Label1 = QtWidgets.QLabel(parent=Form)
        self.name_Label1.setGeometry(QtCore.QRect(170, 30, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.name_Label1.setFont(font)
        self.name_Label1.setStyleSheet("color:rgba(80,218,107,255);")
        self.name_Label1.setObjectName("name_Label1")
        self.input = QtWidgets.QLineEdit(parent=Form)
        self.input.setGeometry(QtCore.QRect(40, 210, 541, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(20)
        self.input.setFont(font)
        self.input.setStyleSheet("border: 5px solid rgba(80,218,107,255);\n"
"color: rgb(255, 255, 255);\n"
"text-align: center;\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.input.setText("")
        self.input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.input.setObjectName("input")
        self.browse_Button = QtWidgets.QPushButton(parent=Form)
        self.browse_Button.setGeometry(QtCore.QRect(40, 320, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.browse_Button.setFont(font)
        self.browse_Button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.browse_Button.setObjectName("browse_Button")
        self.clear_Button = QtWidgets.QPushButton(parent=Form)
        self.clear_Button.setGeometry(QtCore.QRect(320, 320, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.clear_Button.setFont(font)
        self.clear_Button.setStyleSheet("border: 2px solid white;\n"
"color: rgb(255, 255, 255);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"border-color: rgb(255, 255, 255);")
        self.clear_Button.setObjectName("clear_Button")
        self.MD5_Button = QtWidgets.QPushButton(parent=Form)
        self.MD5_Button.setGeometry(QtCore.QRect(40, 440, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.MD5_Button.setFont(font)
        self.MD5_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.MD5_Button.setObjectName("MD5_Button")
        self.SHA1_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA1_Button.setGeometry(QtCore.QRect(40, 520, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA1_Button.setFont(font)
        self.SHA1_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA1_Button.setObjectName("SHA1_Button")
        self.SHA2_224_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA2_224_Button.setGeometry(QtCore.QRect(150, 440, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA2_224_Button.setFont(font)
        self.SHA2_224_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA2_224_Button.setObjectName("SHA2_224_Button")
        self.SHA3_224_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA3_224_Button.setGeometry(QtCore.QRect(370, 440, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA3_224_Button.setFont(font)
        self.SHA3_224_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA3_224_Button.setObjectName("SHA3_224_Button")
        self.output_QR_Label = QtWidgets.QLabel(parent=Form)
        self.output_QR_Label.setGeometry(QtCore.QRect(620, 190, 551, 231))
        self.output_QR_Label.setStyleSheet("background-color: rgba(27,79,96,70%);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.output_QR_Label.setText("")
        self.output_QR_Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.output_QR_Label.setObjectName("output_QR_Label")
        self.output_hash_Label = QtWidgets.QLabel(parent=Form)
        self.output_hash_Label.setGeometry(QtCore.QRect(620, 490, 551, 91))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(17)
        font.setBold(False)
        font.setWeight(50)
        self.output_hash_Label.setFont(font)
        self.output_hash_Label.setStyleSheet("background-color: rgba(27,79,96,70%);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"color: white;")
        self.output_hash_Label.setText("")
        self.output_hash_Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.output_hash_Label.setObjectName("output_hash_Label")
        self.save_Button = QtWidgets.QPushButton(parent=Form)
        self.save_Button.setGeometry(QtCore.QRect(850, 610, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.save_Button.setFont(font)
        self.save_Button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"\n"
"")
        self.save_Button.setObjectName("save_Button")
        self.QR_Label = QtWidgets.QLabel(parent=Form)
        self.QR_Label.setGeometry(QtCore.QRect(620, 130, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.QR_Label.setFont(font)
        self.QR_Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.QR_Label.setObjectName("QR_Label")
        self.name_Label2 = QtWidgets.QLabel(parent=Form)
        self.name_Label2.setGeometry(QtCore.QRect(340, 30, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.name_Label2.setFont(font)
        self.name_Label2.setStyleSheet("color: rgb(255, 255, 255);")
        self.name_Label2.setObjectName("name_Label2")
        self.result_Label = QtWidgets.QLabel(parent=Form)
        self.result_Label.setGeometry(QtCore.QRect(630, 430, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.result_Label.setFont(font)
        self.result_Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.result_Label.setObjectName("result_Label")
        self.back_Button = QtWidgets.QPushButton(parent=Form)
        self.back_Button.setGeometry(QtCore.QRect(20, 640, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.back_Button.setFont(font)
        self.back_Button.setStyleSheet("border: 2px solid white;\n"
"color: rgb(255, 255, 255);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"border-color: rgb(255, 255, 255);\n"
"\n"
"")
        self.back_Button.setObjectName("back_Button")
        self.enter_text_Label = QtWidgets.QLabel(parent=Form)
        self.enter_text_Label.setGeometry(QtCore.QRect(230, 150, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.enter_text_Label.setFont(font)
        self.enter_text_Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.enter_text_Label.setObjectName("enter_text_Label")
        self.logo_Label = QtWidgets.QLabel(parent=Form)
        self.logo_Label.setGeometry(QtCore.QRect(40, 20, 91, 81))
        self.logo_Label.setText("")
        self.logo_Label.setPixmap(QtGui.QPixmap("d:\\ISAN Security Gizmo Box\\backup\\../../../Downloads/icons8-stan-marsh-96.png"))
        self.logo_Label.setScaledContents(True)
        self.logo_Label.setObjectName("logo_Label")
        self.SHA2_256_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA2_256_Button.setGeometry(QtCore.QRect(150, 520, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA2_256_Button.setFont(font)
        self.SHA2_256_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA2_256_Button.setObjectName("SHA2_256_Button")
        self.SHA2_384_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA2_384_Button.setGeometry(QtCore.QRect(260, 440, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA2_384_Button.setFont(font)
        self.SHA2_384_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA2_384_Button.setObjectName("SHA2_384_Button")
        self.SHA2_512_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA2_512_Button.setGeometry(QtCore.QRect(260, 520, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA2_512_Button.setFont(font)
        self.SHA2_512_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA2_512_Button.setObjectName("SHA2_512_Button")
        self.SHA3_256_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA3_256_Button.setGeometry(QtCore.QRect(370, 520, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA3_256_Button.setFont(font)
        self.SHA3_256_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA3_256_Button.setObjectName("SHA3_256_Button")
        self.SHA3_384_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA3_384_Button.setGeometry(QtCore.QRect(480, 440, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA3_384_Button.setFont(font)
        self.SHA3_384_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA3_384_Button.setObjectName("SHA3_384_Button")
        self.SHA3_512_Button = QtWidgets.QPushButton(parent=Form)
        self.SHA3_512_Button.setGeometry(QtCore.QRect(480, 520, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SHA3_512_Button.setFont(font)
        self.SHA3_512_Button.setStyleSheet("background-color: rgba(155,233,172,255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius :20px;\n"
"border-top-right-radius :20px; \n"
"border-bottom-left-radius : 20px; \n"
"border-bottom-right-radius : 20px;\n"
"\n"
"")
        self.SHA3_512_Button.setObjectName("SHA3_512_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_Label1.setText(_translate("Form", "MESSAGE "))
        self.browse_Button.setText(_translate("Form", "BROWSE"))
        self.clear_Button.setText(_translate("Form", "CLEAR"))
        self.MD5_Button.setText(_translate("Form", "MD5"))
        self.SHA1_Button.setText(_translate("Form", "SHA-1"))
        self.SHA2_224_Button.setText(_translate("Form", "SHA-2\n"
"224 bit"))
        self.SHA3_224_Button.setText(_translate("Form", "SHA-3\n"
"224 bit"))
        self.save_Button.setText(_translate("Form", "SAVE"))
        self.QR_Label.setText(_translate("Form", "QR CODE "))
        self.name_Label2.setText(_translate("Form", "DIGEST"))
        self.result_Label.setText(_translate("Form", "RESULT "))
        self.back_Button.setText(_translate("Form", "BACK"))
        self.enter_text_Label.setText(_translate("Form", "ENTER TEXT OR FILE "))
        self.SHA2_256_Button.setText(_translate("Form", "SHA-2\n"
"256 bit"))
        self.SHA2_384_Button.setText(_translate("Form", "SHA-2\n"
"384 bit"))
        self.SHA2_512_Button.setText(_translate("Form", "SHA-2\n"
"512 bit"))
        self.SHA3_256_Button.setText(_translate("Form", "SHA-3\n"
"256 bit"))
        self.SHA3_384_Button.setText(_translate("Form", "SHA-3\n"
"384 bit"))
        self.SHA3_512_Button.setText(_translate("Form", "SHA-3\n"
"512 bit"))