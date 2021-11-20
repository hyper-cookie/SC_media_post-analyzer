from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, \
    QGroupBox, QComboBox

from PostAnalyzer.MLModel.MLModel import *
from PostAnalyzer.WebParser.WebParser import *


class FormBuilder(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.MLModel_object = PredictionModel()
        self.parser_object = PostParser()

        self.create_all_forms()
        self.fill_forms()
        self.create_layers()

    def create_all_forms(self):
        self.input_layer = QLabel()
        self.social_media_combobox = QComboBox()
        self.user_url = QLineEdit(placeholderText="Ссылка на пост")

        self.actions_label = QLabel()
        self.start_button = QPushButton()

        self.result_label = QLabel()
        self.positive_result = QLineEdit(placeholderText='Позитивный шанс')
        self.negative_result = QLineEdit(placeholderText='Отрицательный шанс')

    def fill_forms(self):
        self.input_layer.setText("Ввод")
        self.social_media_combobox.addItems(('ВКонтакте', 'Инстаграм', 'Телеграм'))

        self.actions_label.setText("Действия")
        self.start_button.setText("Начать анализ")
        self.start_button.clicked.connect(self.start_analysis)

        self.result_label.setText("Результаты анализа")
        self.positive_result.setDisabled(True)
        self.negative_result.setDisabled(True)

    def create_layers(self):
        outline = '''
                            QGroupBox {
                                margin-top: 2ex;
                            }
                            QGroupBox::title {
                                subcontrol-origin: margin;
                                left: 3ex;
                            }
                        '''

        main_layout = QVBoxLayout(self)

        self.second_groupbox = QGroupBox(self.input_layer.text())
        self.second_groupbox.setStyleSheet(outline)
        second_groupbox_layout = QHBoxLayout(self.second_groupbox)
        second_groupbox_layout.addWidget(self.user_url)
        second_groupbox_layout.addWidget(self.social_media_combobox)
        main_layout.addWidget(self.second_groupbox)

        self.third_groupbox = QGroupBox(self.actions_label.text())
        self.third_groupbox.setStyleSheet(outline)
        third_groupbox_layout = QHBoxLayout(self.third_groupbox)
        third_groupbox_layout.addWidget(self.start_button)
        main_layout.addWidget(self.third_groupbox)

        self.fourth_groupbox = QGroupBox(self.result_label.text())
        self.fourth_groupbox.setStyleSheet(outline)
        fourth_groupbox_layout = QVBoxLayout(self.fourth_groupbox)
        fourth_groupbox_layout.addWidget(self.positive_result)
        fourth_groupbox_layout.addWidget(self.negative_result)
        main_layout.addWidget(self.fourth_groupbox)

    def start_analysis(self):
        social_media = {'ВКонтакте': 'VKONTAKTE', 'Инстаграм': 'INSTAGRAM', 'Телеграм': 'TELEGRAM'}

        social_url = self.user_url.text()
        social_media = social_media[self.social_media_combobox.currentText()]

        post_text = self.parser_object.parse_sc_post(social_media, social_url)
        prediction = self.MLModel_object.make_prediction(post_text)

        self.positive_result.setText('Положительная вероятность ' + str(round(prediction[0][1] * 100, 2)) + '%')
        self.negative_result.setText('Положительная вероятность ' + str(round(prediction[0][0] * 100, 2)) + '%')
