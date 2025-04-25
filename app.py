import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QLabel, QMessageBox
)
from db import Session
from models import Oprosnik

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Опросник")
        self.resize(700, 500)

        # Таблица
        self.table = QTableWidget()

        # Кнопка обновления
        self.refresh_button = QPushButton("Обновить")
        
        # Форма добавления пользователя
        self.opros_input = QLineEdit()
        self.opros_input.setPlaceholderText("Номер опросника")

        self.correctanswer_input = QLineEdit()
        self.correctanswer_input.setPlaceholderText("Номер ответов")

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("ID пользователя (например, 1)")

        self.add_button = QPushButton("Добавить результаты")
        self.delete_button = QPushButton("Удалить результат")

        # Layout для формы
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Номер опросника:"))
        form_layout.addWidget(self.opros_input)
        form_layout.addWidget(QLabel("Номер ответов:"))
        form_layout.addWidget(self.correctanswer_input)
        form_layout.addWidget(QLabel("ID пользователя:"))
        form_layout.addWidget(self.user_id_input)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.delete_button)

        # Главный layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(form_layout)
        layout.addWidget(self.refresh_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Обработчики
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_opros)
        self.delete_button.clicked.connect(self.delete_opros)
        self.table.cellDoubleClicked.connect(self.load_selected_row)

        # Начальная загрузка
        self.load_data()

    def load_data(self):
        session = Session()
        opros = session.query(Oprosnik).all()

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Номер опросника", "Код ответов", "Пользователь"])
        self.table.setRowCount(len(opros))

        for row, oprosnik in enumerate(opros):
            self.table.setItem(row, 0, QTableWidgetItem(oprosnik.numberoprosnik))
            self.table.setItem(row, 1, QTableWidgetItem(oprosnik.correctanswer))
            self.table.setItem(row, 2, QTableWidgetItem(str(oprosnik.user_id)))

        session.close()

    def add_opros(self):
        numberoprosnik = self.opros_input.text().strip()
        correctanswer = self.correctanswer_input.text().strip()
        user_id = self.user_id_input.text().strip()

        if not numberoprosnik or not correctanswer or not user_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля корректно.")
            return

        session = Session()
        
        # Check if the record already exists
        existing_opros = session.query(Oprosnik).filter_by(
            numberoprosnik=numberoprosnik,
            correctanswer=correctanswer,
            user_id=int(user_id)
        ).first()

        if existing_opros:
            QMessageBox.warning(self, "Ошибка", "Запись с такими данными уже существует.")
            session.close()
            return

        # Create a new Oprosnik instance without setting the ID
        new_opros = Oprosnik(numberoprosnik=numberoprosnik, correctanswer=correctanswer, user_id=int(user_id))
        session.add(new_opros)
        
        try:
            session.commit()
            QMessageBox.information(self, "Успех", "Результат успешно добавлен.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить результат: {str(e)}")
        finally:
            session.close()

        # Очистка полей и обновление таблицы
        self.opros_input.clear()
        self.correctanswer_input.clear()
        self.user_id_input.clear()
        self.load_data()

    def delete_opros(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для удаления.")
            return

        session = Session()
        oprosnik_to_delete = session.query(Oprosnik).filter_by(
            numberoprosnik=self.table.item(selected_row, 0).text(),
            correctanswer=self.table.item(selected_row, 1).text(),
            user_id=int(self.table.item(selected_row, 2).text())
        ).first()

        if oprosnik_to_delete:
            session.delete(oprosnik_to_delete)
            session.commit()
            QMessageBox.information(self, "Успех", "Результат успешно удален.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти результат для удаления.")

        session.close()
        self.load_data()

    def load_selected_row(self, row):
        self.opros_input.setText(self.table.item(row, 0).text())
        self.correctanswer_input.setText(self.table.item(row, 1).text())
        self.user_id_input.setText(self.table.item(row, 2).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
