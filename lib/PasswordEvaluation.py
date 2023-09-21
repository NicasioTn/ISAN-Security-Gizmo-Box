import os
from PyQt6.QtCore import QFileInfo
from PyQt6.QtWidgets import QDialog, QFileDialog, QLineEdit
from PyQt6.QtGui import QIcon
from pathlib import Path
from math import log2


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
    
    # real time password detection
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
        # check if password is empty
        if password == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_digits.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            return 0
    
        # Sum the number of possible characters
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

            # Convert seconds to years, months, weeks, days, hours, minutes, seconds
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            weeks, days = divmod(days, 7)
            months, weeks = divmod(weeks, 4)
            years, months = divmod(months, 12)
            
            time_parts = []
            # Show time to crack all units
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
            os.getcwd(),
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