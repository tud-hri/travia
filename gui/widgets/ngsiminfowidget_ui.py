# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ngsiminfowidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VehicleInfo(object):
    def setupUi(self, VehicleInfo):
        VehicleInfo.setObjectName("VehicleInfo")
        VehicleInfo.resize(1262, 150)
        self.gridLayout = QtWidgets.QGridLayout(VehicleInfo)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.selectedIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedIDLineEdit.setReadOnly(True)
        self.selectedIDLineEdit.setObjectName("selectedIDLineEdit")
        self.gridLayout.addWidget(self.selectedIDLineEdit, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(VehicleInfo)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 5, 1, 1)
        self.selectedAccLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedAccLineEdit.setReadOnly(True)
        self.selectedAccLineEdit.setObjectName("selectedAccLineEdit")
        self.gridLayout.addWidget(self.selectedAccLineEdit, 1, 8, 1, 1)
        self.label_30 = QtWidgets.QLabel(VehicleInfo)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 4, 5, 1, 1)
        self.destinationZoneLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.destinationZoneLineEdit.setReadOnly(True)
        self.destinationZoneLineEdit.setObjectName("destinationZoneLineEdit")
        self.gridLayout.addWidget(self.destinationZoneLineEdit, 4, 4, 1, 1)
        self.selectedTypeLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedTypeLineEdit.setReadOnly(True)
        self.selectedTypeLineEdit.setObjectName("selectedTypeLineEdit")
        self.gridLayout.addWidget(self.selectedTypeLineEdit, 0, 4, 1, 1)
        self.label_11 = QtWidgets.QLabel(VehicleInfo)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 3, 1, 1)
        self.label_25 = QtWidgets.QLabel(VehicleInfo)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 3, 7, 1, 1)
        self.label_5 = QtWidgets.QLabel(VehicleInfo)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(VehicleInfo)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 5, 1, 1)
        self.originZoneLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.originZoneLineEdit.setReadOnly(True)
        self.originZoneLineEdit.setObjectName("originZoneLineEdit")
        self.gridLayout.addWidget(self.originZoneLineEdit, 4, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(VehicleInfo)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 3, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(VehicleInfo)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 4, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(VehicleInfo)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(VehicleInfo)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 5, 1, 1)
        self.label_24 = QtWidgets.QLabel(VehicleInfo)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 3, 5, 1, 1)
        self.sectionLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.sectionLineEdit.setReadOnly(True)
        self.sectionLineEdit.setObjectName("sectionLineEdit")
        self.gridLayout.addWidget(self.sectionLineEdit, 3, 8, 1, 1)
        self.selectedWidthLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedWidthLineEdit.setReadOnly(True)
        self.selectedWidthLineEdit.setObjectName("selectedWidthLineEdit")
        self.gridLayout.addWidget(self.selectedWidthLineEdit, 0, 8, 1, 1)
        self.selectedXPosLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedXPosLineEdit.setReadOnly(True)
        self.selectedXPosLineEdit.setObjectName("selectedXPosLineEdit")
        self.gridLayout.addWidget(self.selectedXPosLineEdit, 1, 2, 1, 1)
        self.precedingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.precedingIDLineEdit.setReadOnly(True)
        self.precedingIDLineEdit.setObjectName("precedingIDLineEdit")
        self.gridLayout.addWidget(self.precedingIDLineEdit, 3, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(VehicleInfo)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 2, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(VehicleInfo)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.selectedVeLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedVeLineEdit.setReadOnly(True)
        self.selectedVeLineEdit.setObjectName("selectedVeLineEdit")
        self.gridLayout.addWidget(self.selectedVeLineEdit, 1, 6, 1, 1)
        self.label_8 = QtWidgets.QLabel(VehicleInfo)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 7, 1, 1)
        self.timeHeadwayLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.timeHeadwayLineEdit.setReadOnly(True)
        self.timeHeadwayLineEdit.setObjectName("timeHeadwayLineEdit")
        self.gridLayout.addWidget(self.timeHeadwayLineEdit, 2, 4, 1, 1)
        self.spaceHeadwayLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.spaceHeadwayLineEdit.setReadOnly(True)
        self.spaceHeadwayLineEdit.setObjectName("spaceHeadwayLineEdit")
        self.gridLayout.addWidget(self.spaceHeadwayLineEdit, 2, 2, 1, 1)
        self.intersectionLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.intersectionLineEdit.setReadOnly(True)
        self.intersectionLineEdit.setObjectName("intersectionLineEdit")
        self.gridLayout.addWidget(self.intersectionLineEdit, 3, 6, 1, 1)
        self.selectedLaneNumLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedLaneNumLineEdit.setReadOnly(True)
        self.selectedLaneNumLineEdit.setObjectName("selectedLaneNumLineEdit")
        self.gridLayout.addWidget(self.selectedLaneNumLineEdit, 4, 6, 1, 1)
        self.label_22 = QtWidgets.QLabel(VehicleInfo)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 3, 0, 1, 1)
        self.selectedLengthLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedLengthLineEdit.setReadOnly(True)
        self.selectedLengthLineEdit.setObjectName("selectedLengthLineEdit")
        self.gridLayout.addWidget(self.selectedLengthLineEdit, 0, 6, 1, 1)
        self.followingIDLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.followingIDLineEdit.setReadOnly(True)
        self.followingIDLineEdit.setObjectName("followingIDLineEdit")
        self.gridLayout.addWidget(self.followingIDLineEdit, 3, 4, 1, 1)
        self.selectedYPosLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.selectedYPosLineEdit.setReadOnly(True)
        self.selectedYPosLineEdit.setObjectName("selectedYPosLineEdit")
        self.gridLayout.addWidget(self.selectedYPosLineEdit, 1, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(VehicleInfo)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(VehicleInfo)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 7, 1, 1)
        self.movementLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.movementLineEdit.setReadOnly(True)
        self.movementLineEdit.setObjectName("movementLineEdit")
        self.gridLayout.addWidget(self.movementLineEdit, 2, 6, 1, 1)
        self.label_16 = QtWidgets.QLabel(VehicleInfo)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 2, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(VehicleInfo)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 4, 7, 1, 1)
        self.directionLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.directionLineEdit.setReadOnly(True)
        self.directionLineEdit.setObjectName("directionLineEdit")
        self.gridLayout.addWidget(self.directionLineEdit, 4, 8, 1, 1)
        self.headingLineEdit = QtWidgets.QLineEdit(VehicleInfo)
        self.headingLineEdit.setObjectName("headingLineEdit")
        self.gridLayout.addWidget(self.headingLineEdit, 2, 8, 1, 1)
        self.label = QtWidgets.QLabel(VehicleInfo)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 7, 1, 1)

        self.retranslateUi(VehicleInfo)
        QtCore.QMetaObject.connectSlotsByName(VehicleInfo)

    def retranslateUi(self, VehicleInfo):
        _translate = QtCore.QCoreApplication.translate
        VehicleInfo.setWindowTitle(_translate("VehicleInfo", "Form"))
        self.label_7.setText(_translate("VehicleInfo", "Length:"))
        self.label_30.setText(_translate("VehicleInfo", "Lane number:"))
        self.label_11.setText(_translate("VehicleInfo", "Y Position:"))
        self.label_25.setText(_translate("VehicleInfo", "Section:"))
        self.label_5.setText(_translate("VehicleInfo", "ID:"))
        self.label_12.setText(_translate("VehicleInfo", "Velocity:"))
        self.label_23.setText(_translate("VehicleInfo", "Folowing ID:"))
        self.label_21.setText(_translate("VehicleInfo", "Destination Zone:"))
        self.label_6.setText(_translate("VehicleInfo", "Type:"))
        self.label_18.setText(_translate("VehicleInfo", "Movement:"))
        self.label_24.setText(_translate("VehicleInfo", "Intersection:"))
        self.label_17.setText(_translate("VehicleInfo", "Time Headway:"))
        self.label_10.setText(_translate("VehicleInfo", "X position:"))
        self.label_8.setText(_translate("VehicleInfo", "Width:"))
        self.label_22.setText(_translate("VehicleInfo", "Preceding ID:"))
        self.label_20.setText(_translate("VehicleInfo", "Origin Zone:"))
        self.label_13.setText(_translate("VehicleInfo", "Acceleration:"))
        self.label_16.setText(_translate("VehicleInfo", "Space headway:"))
        self.label_19.setText(_translate("VehicleInfo", "Direction:"))
        self.label.setText(_translate("VehicleInfo", "Heading:"))
