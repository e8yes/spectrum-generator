# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1280, 1024)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QSize(1280, 1024))
        Widget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(Widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.source_mode_radio = QRadioButton(self.groupBox)
        self.source_mode_radio.setObjectName(u"source_mode_radio")
        self.source_mode_radio.setChecked(True)

        self.horizontalLayout_3.addWidget(self.source_mode_radio)

        self.target_mode_radio = QRadioButton(self.groupBox)
        self.target_mode_radio.setObjectName(u"target_mode_radio")

        self.horizontalLayout_3.addWidget(self.target_mode_radio)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.groupBox)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.feature_selector = QFormLayout()
        self.feature_selector.setObjectName(u"feature_selector")
        self.feature_combo_box = QComboBox(Widget)
        self.feature_combo_box.setObjectName(u"feature_combo_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.feature_combo_box.sizePolicy().hasHeightForWidth())
        self.feature_combo_box.setSizePolicy(sizePolicy1)
        self.feature_combo_box.setEditable(False)

        self.feature_selector.setWidget(1, QFormLayout.FieldRole, self.feature_combo_box)

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")

        self.feature_selector.setWidget(1, QFormLayout.LabelRole, self.label)


        self.verticalLayout_2.addLayout(self.feature_selector)

        self.scatter_chart = QFrame(Widget)
        self.scatter_chart.setObjectName(u"scatter_chart")
        sizePolicy1.setHeightForWidth(self.scatter_chart.sizePolicy().hasHeightForWidth())
        self.scatter_chart.setSizePolicy(sizePolicy1)
        self.scatter_chart.setMinimumSize(QSize(500, 500))
        self.scatter_chart.setStyleSheet(u"")
        self.scatter_chart.setFrameShape(QFrame.StyledPanel)
        self.scatter_chart.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.scatter_chart)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addWidget(self.scatter_chart)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.user_name_input = QLineEdit(Widget)
        self.user_name_input.setObjectName(u"user_name_input")

        self.horizontalLayout_2.addWidget(self.user_name_input)

        self.search_user_button = QPushButton(Widget)
        self.search_user_button.setObjectName(u"search_user_button")

        self.horizontalLayout_2.addWidget(self.search_user_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.profile_distance_output = QLineEdit(Widget)
        self.profile_distance_output.setObjectName(u"profile_distance_output")
        self.profile_distance_output.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.profile_distance_output)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.tweet_display = QFrame(Widget)
        self.tweet_display.setObjectName(u"tweet_display")
        self.tweet_display.setFrameShape(QFrame.StyledPanel)
        self.tweet_display.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.tweet_display)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.source_user_tweet_output = QTextBrowser(self.tweet_display)
        self.source_user_tweet_output.setObjectName(u"source_user_tweet_output")

        self.horizontalLayout.addWidget(self.source_user_tweet_output)

        self.target_user_tweet_output = QTextBrowser(self.tweet_display)
        self.target_user_tweet_output.setObjectName(u"target_user_tweet_output")

        self.horizontalLayout.addWidget(self.target_user_tweet_output)


        self.verticalLayout_2.addWidget(self.tweet_display)


        self.retranslateUi(Widget)

        self.feature_combo_box.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"User Profile Explorer", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Selection Mode", None))
        self.source_mode_radio.setText(QCoreApplication.translate("Widget", u"Source", None))
        self.target_mode_radio.setText(QCoreApplication.translate("Widget", u"Target", None))
        self.feature_combo_box.setCurrentText("")
        self.feature_combo_box.setPlaceholderText("")
        self.label.setText(QCoreApplication.translate("Widget", u"Feature", None))
        self.user_name_input.setPlaceholderText(QCoreApplication.translate("Widget", u"@TwitterUserName", None))
        self.search_user_button.setText(QCoreApplication.translate("Widget", u"Search ", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Profile Distance:", None))
        self.profile_distance_output.setPlaceholderText(QCoreApplication.translate("Widget", u"nan", None))
        self.source_user_tweet_output.setPlaceholderText(QCoreApplication.translate("Widget", u"Source user representative data", None))
        self.target_user_tweet_output.setPlaceholderText(QCoreApplication.translate("Widget", u"Target user representative data", None))
    # retranslateUi

