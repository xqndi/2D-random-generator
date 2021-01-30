from graphics import *
from random import randint

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720


class House(Rectangle):
    def __init__(self, top_corner):
        self.size = 1
        self.nr_living_neighbors = 0
        self.upper_corner = top_corner
        self.lower_corner = Point(top_corner.getX() + self.size,
                                  top_corner.getY() + self.size)
        Rectangle.__init__(self, self.upper_corner, self.lower_corner)
        self.setFill("black")
        self.setOutline("black")

    def update_map_(self, win_map):
        temp_y = int(self.upper_corner.getY())
        temp_x = int(self.upper_corner.getX())

        if not win_map[temp_y][temp_x]:
            win_map[temp_y][temp_x] = 1
        else:
            return False

        if not win_map[temp_y + 1][temp_x]:
            win_map[temp_y + 1][temp_x] = 1
        else:
            return False

        if not win_map[temp_y][temp_x + 1]:
            win_map[temp_y][temp_x + 1] = 1
        else:
            return False

        if not win_map[temp_y + 1][temp_x + 1]:
            win_map[temp_y + 1][temp_x + 1] = 1
        else:
            return False

        return True

    def count_neighbors_(self, win_map, neighbor_size):
        temp_y = int(self.upper_corner.getY())
        temp_x = int(self.upper_corner.getX())

        for index in range(-neighbor_size, neighbor_size + 2):
            if index == 0:
                continue
            if (0 <= temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y + index][temp_x] == 1):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (win_map[temp_y][temp_x + index] == 1):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y + index][temp_x + index] == 1):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y - index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y - index][temp_x + index] == 1):
                self.nr_living_neighbors += 1
        print(self.nr_living_neighbors)


class Lake(Circle):
    def __init__(self, center, radius):
        Circle.__init__(self, center, radius)
        self.setFill("blue")
        self.setOutline("blue")

    def update_map_(self, win_map):

        low_x = int(self.getP1().getX())
        low_y = int(self.getP1().getY())
        high_x = int(self.getP2().getX())
        high_y = int(self.getP2().getY())
        print(low_x, low_y, high_x, high_y)

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                if win_map[row_y][col_x]:
                    return False

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                win_map[row_y][col_x] = 2
        return True


def generate_houses(win_map, nr_houses, window, neighbor_size):
    for house in range(nr_houses):
        while True:
            temp_house = House(Point(randint(0, WINDOW_WIDTH - 10),
                                     randint(0, WINDOW_HEIGHT - 10)))
            temp_house.count_neighbors_(win_map, neighbor_size)

            if temp_house.nr_living_neighbors == 0 and \
                    randint(0, 20 * neighbor_size) != 0:
                break
            spawn_threshold = randint(0, int(neighbor_size / 3))
            if temp_house.nr_living_neighbors < spawn_threshold:
                break
            if temp_house.update_map_(win_map):
                temp_house.draw(window)
                break


def generate_lakes(win_map, nr_iterations, window):
    for attempt in range(nr_iterations):
        if randint(0, 2):
            continue
        temp_lake = Lake(Point(randint(0, WINDOW_WIDTH - 10),
                               randint(0, WINDOW_HEIGHT - 10)), randint(40, 100))
        if not temp_lake.update_map_(win_map):
            continue
        temp_lake.draw(window)
        # Rectangle(temp_lake.getP1(), temp_lake.getP2()).draw(window)


def main():
    window_map = [[0 for col in range(WINDOW_WIDTH)]
                  for row in range(WINDOW_HEIGHT)]

    win = GraphWin("gen", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("olivedrab")

    generate_lakes(window_map, 5, win)
    generate_houses(window_map, 45000, win, 30)

    win.getMouse()


if __name__ == '__main__':
    main()
