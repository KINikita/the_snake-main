from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Родительский класс GameObject нужен для
    создания дочерних классов Snake и Apple
    """

    def __init__(self) -> None:
        """Конструктор для объектов класса GameObject"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Пустой метод, создан для переиспользования
        в дочерних классах (полиморфизм)
        """
        pass


class Apple(GameObject):
    """
    Дочерний класс Apple (родитель - GameObject) нужен для создания,
    отрисовки яблока в случайной позиции на игровом поле
    """

    def __init__(self):
        """
        Конструктор класса Apple задает цвет и случайную
        позицию в рамках игрового поля
        """
        self.body_color = APPLE_COLOR
        self.position = (
            self.randomize_position(GRID_WIDTH, 'WIDTH'),
            self.randomize_position(GRID_HEIGHT, 'HEIGHT'),
        )

    def randomize_position(self, limit: int, side: str):
        """
        Используется в конструкторе класса для создания случайного положения
        в рамках игрового поля. Принимает предел и сторону,
        у которой определен данный предел. Возвращает рандомную координату.
        """
        res = randint(0, limit) * GRID_SIZE
        if (
            res >= SCREEN_WIDTH and side == 'WIDTH') \
                or (res >= SCREEN_HEIGHT and side == 'HEIGHT'):
            return res - GRID_SIZE
        else:
            return res

    def get_apple_position(self):
        """
        Возвращает позицию яблока. Используется в методе eat()
        для создания события съедания яблока
        """
        return self.position

    def draw(self):
        """Рисует яблоко на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Snake является дочерним. Родитель - GameObject. Методы класса Snake
    создают объект класса, отрисовывают его на поле, увеличивают змею при
    съедании яблока и обнуляют игру, если змея съедает себя.
    """

    positions: list = []
    length: int = 1
    direction: tuple = RIGHT
    next_direction = None

    def __init__(self):
        """
        Конструктор класса Snake создает объект класса, добавляет в змейку
        позицию ее головы, задает ее цвет, и устанавливает атрибуту класса
        last значение None
        """
        super().__init__()
        list.append(self.positions, self.position)
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        Используется в методах eat() и move().
        """
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет позицию змейки после нажатия клавиш.
        Связана с функцией handle_keys()
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def add_square(self, x: int, y: int):
        """Добавляет квадратик к змейке. Используется в методе move()"""
        list.insert(
            self.positions,
            0,
            (x, y)
        )

    def move(self):
        """
        Создает иллюзию передвижения змейки, добавляя в начало новый
        квадратик (с помощью метода add_square()) змеи и удаляя его в конце.
        Если змейка попытается выйти за границы, она вернется с
        противоположной стороны.
        """
        head = self.get_head_position()
        if head[1] == SCREEN_HEIGHT and self.direction != DOWN:
            self.add_square(head[0], 0)
        elif head[0] == SCREEN_WIDTH and self.direction != RIGHT:
            self.add_square(0, head[1])
        elif self.direction == RIGHT:
            if head[0] != SCREEN_WIDTH:
                self.add_square(head[0] + GRID_SIZE, head[1])
            else:
                self.add_square(0, head[1])
        elif self.direction == LEFT:
            if head[0] != 0:
                self.add_square(head[0] - GRID_SIZE, head[1])
            else:
                self.add_square(SCREEN_WIDTH - GRID_SIZE, head[1])
        elif self.direction == DOWN:
            if head[1] != SCREEN_HEIGHT:
                self.add_square(head[0], head[1] + GRID_SIZE)
            else:
                self.add_square(head[0], 0)
        elif self.direction == UP:
            if head[1] != 0:
                self.add_square(head[0], head[1] - GRID_SIZE)
            else:
                self.add_square(head[0], SCREEN_HEIGHT - GRID_SIZE)
        if len(self.positions) > self.length:
            self.last = self.positions[len(self.positions) - 1]
            list.pop(self.positions, len(self.positions) - 1)

    def eat(self, apple: Apple):
        """
        Обрабатывает событие поедания яблока змеей. При совпадении
        координат головы змеи и яблока, змейка увеличивается. Возращает True,
        если событие произошло, при этом создается новое яблоко в функции main.
        """
        if self.get_head_position() == apple.get_apple_position():
            self.length += 1
            return True
        else:
            return False

    def reset(self):
        """
        Сбрасывает прогресс игры, если змейка съедает себя, то есть
        координаты змейки всегда должны различаться, иначе игра закончится
        и начнется заново с рандомным направлением змейки, но создание головы
        остаётся в центре экрана.
        """
        for position in self.positions:
            if list.count(self.positions, position) != 1:
                self.length = 1
                list.clear(self.positions)
                list.append(self.positions,
                            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
                self.direction = choice(DIRECTIONS)
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                pass

    # Метод draw класса Snake
    def draw(self):
        """
        Отрисовывает змею, затирая последний элемент змеи для
        создания иллюзии перемещения.
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш с клавиатуры, меняя направление змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция, в которой создается объекты классов Apple и Snake.
    Описана основная логика игры.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        handle_keys(snake)
        snake.move()
        snake.draw()
        flag = snake.eat(apple)
        if flag is True:
            apple = Apple()
        else:
            pass
        snake.update_direction()
        snake.reset()
        pygame.display.update()


if __name__ == "__main__":
    main()
