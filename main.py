# Доступ к функциям операционной системы
import sys
# Генератор случайных чисел
import random
# Для работы с аудио
from playsound import playsound
# Загрузчик формочек от QtCreator
from PyQt5 import uic
# Классики для работы с Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QErrorMessage

# Загружаем формочку, нарисованную в QtCreator
Form, Window = uic.loadUiType("main.ui")


# Класс формы с логикой
class BatTestForm(Form):
    # Конструктор получает на вход переменную total - количество вопросов, на которые должен ответить ребенок
    def __init__(self, total):
        # Вызываем конструктор родителя
        super().__init__()
        # x - первый множитель
        self.x = 0
        # y - второй множитель
        self.y = 0
        # score - число ответов ребеонка
        self.score = 0
        # total - количество правильных ответов, на которые должен ответить ребенок
        self.total = total

    # Метод повторной генерации множителей
    def update(self):
        # x - случайное целое число от 1 до 9
        self.x = random.randint(1, 9)
        # y - случайное целое число от 1 до 9
        self.y = random.randint(1, 9)
        # Отображаем надпись на формочке, типа x x y =
        self.label.setText(f"{self.x} x {self.y} = ")

    # обработчик нажатия кнопки
    def check(self):
        # z - ответ, введенныйв поле
        z = int(self.result.toPlainText().strip())

        # Если ответ правильный
        if z == self.x * self.y:
            # увеличиваем счетчик правильных ответов
            self.score += 1

            # Играем победную мелодию
            playsound("ok.wav", False)
            # Если можно продолжать игру дальше
            if self.score < self.total:
                # Диалоговое окошко показывает, что ответ правильный
                msg = QMessageBox()
                # Значок информационного окошка
                msg.setIcon(QMessageBox.Information)
                # Хвалим игррока=)
                msg.setText("Ты молодец!")
                # Хвалим еще сильнее!
                msg.setWindowTitle("Отлично!")
                # Диалоговое окошко имеет только кнопку OK
                msg.setStandardButtons(QMessageBox.Ok)
                # Показываем диалоговое окошко
                msg.exec_()

                # Очищаем поле ввода
                self.result.setText("")
                # Ставим курсов в поле ввода
                self.result.setFocus()

                # Генерируем следующий вопрос
                self.update()
            # Если конец игры (кончились попытки)
            else:
                # Диалоговое окошко сообщает о конце игры
                msg = QMessageBox()
                # Значок окошка с вопросом
                msg.setIcon(QMessageBox.Question)
                # Спрашиваем, будет ли игрок продолжать?
                msg.setText("Еще одну битву?")
                # Заголовок окошка
                msg.setWindowTitle("Конец битвы!")
                # Добавляем кнопки Ok и Cancel диалоговому окошку
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # Отображаем окошко и сохраняем ответ пользователя
                res = msg.exec_()

                # Если игрок нажал Ok - обнуляем счетчик попыток и начинаем заново
                if res == QMessageBox.Ok:
                    self.score = 0

                    self.result.setText("")
                    self.result.setFocus()

                    self.update()
                else:
                    # Если игрок нажал Cancel - завершаем программу
                    sys.exit(0)
        # Если ответ неправильный
        else:
            # Играем мелодию проигрыша
            playsound("error.wav", False)
            # Создаем окно ошибки
            m = QErrorMessage()
            # Тект ошибки
            m.showMessage("Неправильно((( Давай еще разок")
            # Показываем ошибку
            m.exec_()


# Объект Qt приложения
application = QApplication([])
# Главное окно
window = Window()
# Форма в главном окне
form = BatTestForm(10)
# Отображаем форму в окне
form.setupUi(window)
# Вызываем метод BatTestForm.update - генерируем первый вопрос
form.update()
# Связываем нажатие на кнопку и метод BatTestForm.check
form.refresh.clicked.connect(form.check)
# Показываем главное окно
window.show()

# Играем победную музыку
playsound("ok.wav", False)

# Запускаем приложение и ждем закрытия
application.exec_()
