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

    def update_bitmap_(self, bit_map):
        temp_y = int(self.upper_corner.getY())
        temp_x = int(self.upper_corner.getX())

        if not bit_map[temp_y][temp_x]:
            bit_map[temp_y][temp_x] = 1
        else:
            return False

        if not bit_map[temp_y + 1][temp_x]:
            bit_map[temp_y + 1][temp_x] = 1
        else:
            return False

        if not bit_map[temp_y][temp_x + 1]:
            bit_map[temp_y][temp_x + 1] = 1
        else:
            return False

        if not bit_map[temp_y + 1][temp_x + 1]:
            bit_map[temp_y + 1][temp_x + 1] = 1
        else:
            return False

        return True

    def count_neighbors_(self, bitmap, neighbor_size):
        temp_y = int(self.upper_corner.getY())
        temp_x = int(self.upper_corner.getX())

        for index in range(-neighbor_size, neighbor_size + 2):
            if index == 0:
                continue
            if 0 <= temp_y + index <= WINDOW_HEIGHT - 1:
                self.nr_living_neighbors += bitmap[temp_y + index][temp_x]
            if 0 <= temp_x + index <= WINDOW_WIDTH - 1:
                self.nr_living_neighbors += bitmap[temp_y][temp_x + index]
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y + index <= WINDOW_HEIGHT - 1):
                self.nr_living_neighbors += bitmap[temp_y + index][temp_x + index]
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y - index <= WINDOW_HEIGHT - 1):
                self.nr_living_neighbors += bitmap[temp_y - index][temp_x + index]

        print(self.nr_living_neighbors)


def generate_houses(bitmap, nr_houses, window, neighbor_size):
    for house in range(nr_houses):
        while True:
            temp_house = House(Point(randint(0, WINDOW_WIDTH - 10),
                                     randint(0, WINDOW_HEIGHT - 10)))
            temp_house.count_neighbors_(bitmap, neighbor_size)

            if temp_house.nr_living_neighbors == 0 and \
                    randint(0, 25 * neighbor_size) != 0:
                break
            spawn_threshold = randint(0, int(neighbor_size / 3))
            if temp_house.nr_living_neighbors < spawn_threshold:
                break
            if temp_house.update_bitmap_(bitmap):
                temp_house.draw(window)
                break


def main():
    bitmap = [[0 for i in range(WINDOW_WIDTH)] for j in range(WINDOW_HEIGHT)]

    win = GraphWin("gen", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("olivedrab")

    generate_houses(bitmap, 35000, win, 30)

    win.getMouse()


if __name__ == '__main__':
    main()
