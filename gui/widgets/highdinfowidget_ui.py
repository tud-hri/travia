# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'highdinfowidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VehicleInfo(object):
    def setupUi(self, VehicleInfo):
        VehicleInfo.setObjectName("VehicleInfo")
        VehicleInfo.resize(1262, 167)
        self.gridLayout = QtWidgets.QGridLayout(VehicleInfo)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(VehicleInfo)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.selectedIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedIDLineEdit.setReadOnly(True)
        self.selectedIDLineEdit.setObjectName("selectedIDLineEdit")
        self.gridLayout.addWidget(self.selectedIDLineEdit, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(VehicleInfo)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.selectedTypeLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedTypeLineEdit.setReadOnly(True)
        self.selectedTypeLineEdit.setObjectName("selectedTypeLineEdit")
        self.gridLayout.addWidget(self.selectedTypeLineEdit, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(VehicleInfo)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 4, 1, 1)
        self.selectedLengthLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedLengthLineEdit.setReadOnly(True)
        self.selectedLengthLineEdit.setObjectName("selectedLengthLineEdit")
        self.gridLayout.addWidget(self.selectedLengthLineEdit, 0, 5, 1, 1)
        self.label_8 = QtWidgets.QLabel(VehicleInfo)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 6, 1, 1)
        self.selectedWidthLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedWidthLineEdit.setReadOnly(True)
        self.selectedWidthLineEdit.setObjectName("selectedWidthLineEdit")
        self.gridLayout.addWidget(self.selectedWidthLineEdit, 0, 7, 1, 1)
        self.label_9 = QtWidgets.QLabel(VehicleInfo)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 8, 1, 1)
        self.selectedNumLCLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedNumLCLineEdit.setReadOnly(True)
        self.selectedNumLCLineEdit.setObjectName("selectedNumLCLineEdit")
        self.gridLayout.addWidget(self.selectedNumLCLineEdit, 0, 9, 1, 1)
        self.label_10 = QtWidgets.QLabel(VehicleInfo)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.selectedXPosLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedXPosLineEdit.setReadOnly(True)
        self.selectedXPosLineEdit.setObjectName("selectedXPosLineEdit")
        self.gridLayout.addWidget(self.selectedXPosLineEdit, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(VehicleInfo)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 2, 1, 1)
        self.selectedYPosLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedYPosLineEdit.setReadOnly(True)
        self.selectedYPosLineEdit.setObjectName("selectedYPosLineEdit")
        self.gridLayout.addWidget(self.selectedYPosLineEdit, 1, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(VehicleInfo)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 4, 1, 1)
        self.selectedXVeLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedXVeLineEdit.setReadOnly(True)
        self.selectedXVeLineEdit.setObjectName("selectedXVeLineEdit")
        self.gridLayout.addWidget(self.selectedXVeLineEdit, 1, 5, 1, 1)
        self.label_13 = QtWidgets.QLabel(VehicleInfo)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 6, 1, 1)
        self.selectedYVelLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedYVelLineEdit.setReadOnly(True)
        self.selectedYVelLineEdit.setObjectName("selectedYVelLineEdit")
        self.gridLayout.addWidget(self.selectedYVelLineEdit, 1, 7, 1, 1)
        self.label_14 = QtWidgets.QLabel(VehicleInfo)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 1, 8, 1, 1)
        self.selectedXAccLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedXAccLineEdit.setReadOnly(True)
        self.selectedXAccLineEdit.setObjectName("selectedXAccLineEdit")
        self.gridLayout.addWidget(self.selectedXAccLineEdit, 1, 9, 1, 1)
        self.label_15 = QtWidgets.QLabel(VehicleInfo)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 1, 10, 1, 1)
        self.selectedYAccLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedYAccLineEdit.setReadOnly(True)
        self.selectedYAccLineEdit.setObjectName("selectedYAccLineEdit")
        self.gridLayout.addWidget(self.selectedYAccLineEdit, 1, 11, 1, 1)
        self.label_16 = QtWidgets.QLabel(VehicleInfo)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 2, 0, 1, 1)
        self.selectedFrontSDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedFrontSDLineEdit.setReadOnly(True)
        self.selectedFrontSDLineEdit.setObjectName("selectedFrontSDLineEdit")
        self.gridLayout.addWidget(self.selectedFrontSDLineEdit, 2, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(VehicleInfo)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 2, 2, 1, 1)
        self.selectedBackSDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedBackSDLineEdit.setReadOnly(True)
        self.selectedBackSDLineEdit.setObjectName("selectedBackSDLineEdit")
        self.gridLayout.addWidget(self.selectedBackSDLineEdit, 2, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(VehicleInfo)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 4, 1, 1)
        self.selectedDHWLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedDHWLineEdit.setReadOnly(True)
        self.selectedDHWLineEdit.setObjectName("selectedDHWLineEdit")
        self.gridLayout.addWidget(self.selectedDHWLineEdit, 2, 5, 1, 1)
        self.label_19 = QtWidgets.QLabel(VehicleInfo)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 2, 6, 1, 1)
        self.selectedTHWLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedTHWLineEdit.setReadOnly(True)
        self.selectedTHWLineEdit.setObjectName("selectedTHWLineEdit")
        self.gridLayout.addWidget(self.selectedTHWLineEdit, 2, 7, 1, 1)
        self.label_20 = QtWidgets.QLabel(VehicleInfo)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 2, 8, 1, 1)
        self.selectedTTCLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedTTCLineEdit.setReadOnly(True)
        self.selectedTTCLineEdit.setObjectName("selectedTTCLineEdit")
        self.gridLayout.addWidget(self.selectedTTCLineEdit, 2, 9, 1, 1)
        self.label_21 = QtWidgets.QLabel(VehicleInfo)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 2, 10, 1, 1)
        self.precedingXVelLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.precedingXVelLineEdit.setReadOnly(True)
        self.precedingXVelLineEdit.setObjectName("precedingXVelLineEdit")
        self.gridLayout.addWidget(self.precedingXVelLineEdit, 2, 11, 1, 1)
        self.label_22 = QtWidgets.QLabel(VehicleInfo)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 3, 0, 1, 1)
        self.precedingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.precedingIDLineEdit.setReadOnly(True)
        self.precedingIDLineEdit.setObjectName("precedingIDLineEdit")
        self.gridLayout.addWidget(self.precedingIDLineEdit, 3, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(VehicleInfo)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 3, 2, 1, 1)
        self.followingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.followingIDLineEdit.setReadOnly(True)
        self.followingIDLineEdit.setObjectName("followingIDLineEdit")
        self.gridLayout.addWidget(self.followingIDLineEdit, 3, 3, 1, 1)
        self.label_24 = QtWidgets.QLabel(VehicleInfo)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 3, 4, 1, 1)
        self.leftPrecedingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.leftPrecedingIDLineEdit.setReadOnly(True)
        self.leftPrecedingIDLineEdit.setObjectName("leftPrecedingIDLineEdit")
        self.gridLayout.addWidget(self.leftPrecedingIDLineEdit, 3, 5, 1, 1)
        self.label_25 = QtWidgets.QLabel(VehicleInfo)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 3, 6, 1, 1)
        self.leftAlongSideIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.leftAlongSideIDLineEdit.setReadOnly(True)
        self.leftAlongSideIDLineEdit.setObjectName("leftAlongSideIDLineEdit")
        self.gridLayout.addWidget(self.leftAlongSideIDLineEdit, 3, 7, 1, 1)
        self.label_26 = QtWidgets.QLabel(VehicleInfo)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 3, 8, 1, 1)
        self.leftFollowingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.leftFollowingIDLineEdit.setReadOnly(True)
        self.leftFollowingIDLineEdit.setObjectName("leftFollowingIDLineEdit")
        self.gridLayout.addWidget(self.leftFollowingIDLineEdit, 3, 9, 1, 1)
        self.label_27 = QtWidgets.QLabel(VehicleInfo)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 3, 10, 1, 1)
        self.rightPrecedingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.rightPrecedingIDLineEdit.setReadOnly(True)
        self.rightPrecedingIDLineEdit.setObjectName("rightPrecedingIDLineEdit")
        self.gridLayout.addWidget(self.rightPrecedingIDLineEdit, 3, 11, 1, 1)
        self.label_28 = QtWidgets.QLabel(VehicleInfo)
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 4, 0, 1, 1)
        self.rightAlongsideIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.rightAlongsideIDLineEdit.setReadOnly(True)
        self.rightAlongsideIDLineEdit.setObjectName("rightAlongsideIDLineEdit")
        self.gridLayout.addWidget(self.rightAlongsideIDLineEdit, 4, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(VehicleInfo)
        self.label_29.setObjectName("label_29")
        self.gridLayout.addWidget(self.label_29, 4, 2, 1, 1)
        self.rightFollowingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.rightFollowingIDLineEdit.setReadOnly(True)
        self.rightFollowingIDLineEdit.setObjectName("rightFollowingIDLineEdit")
        self.gridLayout.addWidget(self.rightFollowingIDLineEdit, 4, 3, 1, 1)
        self.label_30 = QtWidgets.QLabel(VehicleInfo)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 4, 4, 1, 1)
        self.selectedLaneNumLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedLaneNumLineEdit.setReadOnly(True)
        self.selectedLaneNumLineEdit.setObjectName("selectedLaneNumLineEdit")
        self.gridLayout.addWidget(self.selectedLaneNumLineEdit, 4, 5, 1, 1)

        self.retranslateUi(VehicleInfo)
        QtCore.QMetaObject.connectSlotsByName(VehicleInfo)

    def retranslateUi(self, VehicleInfo):
        _translate = QtCore.QCoreApplication.translate
        VehicleInfo.setWindowTitle(_translate("VehicleInfo", "Form"))
        self.label_5.setText(_translate("VehicleInfo", "ID:"))
        self.label_6.setText(_translate("VehicleInfo", "Type:"))
        self.label_7.setText(_translate("VehicleInfo", "Length:"))
        self.label_8.setText(_translate("VehicleInfo", "Width:"))
        self.label_9.setText(_translate("VehicleInfo", "Number of lane changes:"))
        self.label_10.setText(_translate("VehicleInfo", "X position:"))
        self.label_11.setText(_translate("VehicleInfo", "Y Position:"))
        self.label_12.setText(_translate("VehicleInfo", "X velocity:"))
        self.label_13.setText(_translate("VehicleInfo", "Y velocity:"))
        self.label_14.setText(_translate("VehicleInfo", "X Acceleration:"))
        self.label_15.setText(_translate("VehicleInfo", "Y Acceleration:"))
        self.label_16.setText(_translate("VehicleInfo", "Front sight distance:"))
        self.label_17.setText(_translate("VehicleInfo", "Back sight distance:"))
        self.label_18.setText(_translate("VehicleInfo", "DHW:"))
        self.label_19.setText(_translate("VehicleInfo", "THW:"))
        self.label_20.setText(_translate("VehicleInfo", "TTC:"))
        self.label_21.setText(_translate("VehicleInfo", "Preceding x velocity:"))
        self.label_22.setText(_translate("VehicleInfo", "Preceding ID:"))
        self.label_23.setText(_translate("VehicleInfo", "Folowing ID:"))
        self.label_24.setText(_translate("VehicleInfo", "Left Preceding ID:"))
        self.label_25.setText(_translate("VehicleInfo", "Left Alongside ID:"))
        self.label_26.setText(_translate("VehicleInfo", "Left Following ID:"))
        self.label_27.setText(_translate("VehicleInfo", "Right Preceding ID:"))
        self.label_28.setText(_translate("VehicleInfo", "Right Alongside ID:"))
        self.label_29.setText(_translate("VehicleInfo", "Right Following ID:"))
        self.label_30.setText(_translate("VehicleInfo", "Lane number:"))
