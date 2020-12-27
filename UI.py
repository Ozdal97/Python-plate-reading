
import mainsection
from PyQt5 import QtCore, QtGui, QtWidgets
import filer
from threading import Thread

class Ui_Dialog(object):
    def __init__(self):
        self.api=mainsection
        self.api2=filer
        self.arananplakalar=["61AY20","31ADC826","20K8481"]
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.pushButton.clicked.connect(self.plaka)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.pushButton.setText(_translate("Dialog", "PLAKAYI GETİR"))
    def add(self,path):
        if len(path):
            plaka = [1];
            text = self.api.main(path)
            for aranan in self.arananplakalar:
                if aranan == text:
                    text = text + " ------BU PLAKA ARANMAKTADIR-------"
            plaka[0] = text
            if len(plaka) != 0:

                self.listWidget.addItems(plaka)
                self.listWidget.scrollToBottom()
            else:
                self.listWidget.addItem("Plaka Bulunamadı.Insan kontrolü gerekli.")
                self.listWidget.scrollToBottom()
        else:
            self.lineEdit.setText("Yol Girin")
    def plaka(self):
        path = self.lineEdit.text()
        import os
        import glob
        for i in glob.iglob(os.path.join(path, "*")):
            path=i
            try:
                thread = Thread(target=self.add, args=(path,))
                thread.start()
                if len(path) < 10:
                    path = self.api2.al()
                    self.lineEdit.setText(path)
                else:
                    pass

            except Exception as e:
                print(e)
                pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
