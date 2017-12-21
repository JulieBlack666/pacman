import sys
from threading import Timer

from PyQt5.QtGui import QPainter, QColor, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt

from Level import Level
from Point import Point
from Game import Game


class GamePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.images_directory = 'images'
        self.timer = QTimer()
        self.timer.timeout.connect(self.repaint_game)
        self.start_new_game()
        self.setWindowTitle('PacMan')
        self.window_width = self.game.element_size * self.game.width + 20
        self.window_height = self.game.element_size * self.game.height + 80
        self.setGeometry(200, 25, self.window_width, self.window_height)
        self.show()

    def start_new_game(self):
        self.game = Game(Level().create(32))
        self.init_images()
        self.timer.start(0.5)

    def init_images(self):
        self.static_images = [[None for _ in range(self.game.width)] for _ in range(self.game.height)]
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.map[y][x] is not None:
                    image_name = str.format('{}/{}', self.images_directory, self.game.map[y][x].image_name)
                    self.static_images[y][x] = QPixmap(image_name)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_game_panel(qp)
        self.draw_moving_objects(qp)
        qp.end()

    def draw_game_panel(self, qp):
        qp.setBrush(QColor(10, 10, 10))
        qp.drawRect(10, 10, self.width() - 20, self.height() - 20)
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.map[y][x] is not None:
                    qp.drawPixmap(10 + x * self.game.element_size,
                                  10 + y * self.game.element_size, self.static_images[y][x])
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(15, 720, "LIVES:  ")
        for i in range(self.game.player.lives_count - 1):
            qp.drawPixmap(60 + i*self.game.element_size, 700, QPixmap('images/life.png'))
        qp.drawText(550, 720, str.format('SCORE: {}', self.game.player.score))

    def draw_moving_objects(self, qp):
        for obj in self.game.moving_objects:
                image_name = str.format('{}/{}', self.images_directory, obj.get_image_name())
                image = QPixmap(image_name)
                qp.drawPixmap(10 + obj.location.x, 10 + obj.location.y, image)
        if self.game.game_is_over:
            self.timer.stop()
            qp.drawPixmap(0, 0, QPixmap('images/gameover.png'))
        if self.game.won:
            self.timer.stop()
            qp.drawPixmap(0, 0, QPixmap('images/gamewon.png'))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.game.player.set_direction(Point(0, -1))
        elif e.key() == Qt.Key_Down:
            self.game.player.set_direction(Point(0, 1))
        elif e.key() == Qt.Key_Left:
            self.game.player.set_direction(Point(-1, 0))
        elif e.key() == Qt.Key_Right:
            self.game.player.set_direction(Point(1, 0))
        elif self.game.game_is_over or self.game.won:
            self.start_new_game()
        self.repaint()

    def repaint_game(self):
        self.game.update()
        self.repaint()

    def closeEvent(self, QCloseEvent):
        for ghost in self.game.moving_objects[1:]:
            ghost.stop_timers()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GamePanel()
    sys.exit(app.exec_())
