from graphics import *
from random import randint


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

X_CENTER = WINDOW_WIDTH / 2
Y_CENTER = WINDOW_HEIGHT / 2


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


class Tree(Point):
    def __init__(self, x_pos, y_pos):
        self.nr_living_neighbors = 0
        self.dist_center = -1
        Point.__init__(self, x_pos, y_pos)
        self.setFill("greenyellow")

    def update_map_(self, win_map, window):
        temp_y = int(self.getY())
        temp_x = int(self.getX())

        if not win_map[temp_y][temp_x]:
            win_map[temp_y][temp_x] = 3
            self.draw(window)
            return True
        return False

    def count_neighbors_(self, win_map, neighbor_size):
        temp_y = int(self.getY())
        temp_x = int(self.getX())

        for index in range(-neighbor_size, neighbor_size + 1):
            if index == 0:
                continue
            if (0 <= temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y + index][temp_x] == 3):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (win_map[temp_y][temp_x + index] == 3):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y + index][temp_x + index] == 3):
                self.nr_living_neighbors += 1
            if (0 <= temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= temp_y - index <= WINDOW_HEIGHT - 1) and \
                    (win_map[temp_y - index][temp_x + index] == 3):
                self.nr_living_neighbors += 1

    def distance_to_center(self):
        x_dist = abs(self.getX() - X_CENTER)
        y_dist = abs(self.getY() - Y_CENTER)

        self.dist_center = x_dist + y_dist


class Lake(Circle):
    def __init__(self, center, radius):
        Circle.__init__(self, center, radius)
        self.setFill("blue")
        self.setOutline("blue")

    def update_map_(self, win_map, window):
        low_x = int(self.getP1().getX())
        low_y = int(self.getP1().getY())
        high_x = int(self.getP2().getX())
        high_y = int(self.getP2().getY())

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                if win_map[row_y][col_x]:
                    return False

        self.draw(window)

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                win_map[row_y][col_x] = 2
                self.fill_surroundings(window, row_y, col_x)
        return True

    def fill_surroundings(self, window, row_y, col_x):
        x_dist = abs(self.getCenter().getX() - col_x)
        y_dist = abs(self.getCenter().getY() - row_y)
        total_dist = x_dist + y_dist
        modifier = int(self.radius / 3)

        if x_dist * x_dist + y_dist * y_dist < self.radius * self.radius:
            return
        if randint(0, total_dist * modifier) > self.radius:
            return

        window.plot(col_x, row_y, "blue")


class RiverPart(Rectangle):
    def __init__(self, top_corner):
        self.size = 10
        self.inside_win = True
        Rectangle.__init__(self, top_corner, Point(top_corner.getX() + self.size,
                                                   top_corner.getY() + self.size))
        self.setOutline("blue")
        self.setFill("blue")

    def update_map_(self, win_map, window):
        low_x = int(self.getP1().getX())
        low_y = int(self.getP1().getY())
        high_x = int(self.getP2().getX())
        high_y = int(self.getP2().getY())

        is_valid = True

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                if win_map[row_y][col_x]:
                    is_valid = False

        if not is_valid:
            return

        self.draw(window)

        for row_y in range(low_y, high_y + 1):
            for col_x in range(low_x, high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    self.inside_win = False
                    break
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    self.inside_win = False
                    break
                win_map[row_y][col_x] = 4

        if not self.inside_win:
            print("not inside")


def generate_houses(win_map, nr_houses, window, neighbor_size):
    for house in range(nr_houses):
        while True:
            temp_house = House(Point(randint(0, WINDOW_WIDTH - 10),
                                     randint(0, WINDOW_HEIGHT - 10)))
            temp_house.count_neighbors_(win_map, neighbor_size)

            if temp_house.nr_living_neighbors == 0 and \
                    randint(0, 10 * neighbor_size) != 0:
                break
            spawn_threshold = randint(0, int(neighbor_size / 5))
            if temp_house.nr_living_neighbors < spawn_threshold:
                break
            if temp_house.update_map_(win_map):
                temp_house.draw(window)
                break


def generate_trees(win_map, nr_trees, window, neighbor_size):
    for tree in range(nr_trees):
        while True:
            temp_tree = Tree(randint(0, WINDOW_WIDTH - 10), randint(0, WINDOW_HEIGHT - 10))
            temp_tree.distance_to_center()
            if temp_tree.dist_center < randint(100, WINDOW_HEIGHT - 50):
                break
            temp_tree.count_neighbors_(win_map, neighbor_size)

            if temp_tree.nr_living_neighbors == 0 and \
                    randint(0, 20 * neighbor_size) != 0:
                break
            spawn_threshold = randint(0, int(neighbor_size / 20))
            if temp_tree.nr_living_neighbors < spawn_threshold:
                break
            if temp_tree.update_map_(win_map, window):
                break


def generate_lakes(win_map, nr_iterations, window):
    for attempt in range(nr_iterations):
        if randint(0, 2):
            continue
        temp_lake = Lake(Point(randint(0, WINDOW_WIDTH - 10),
                               randint(0, WINDOW_HEIGHT - 10)), randint(40, 100))
        if not temp_lake.update_map_(win_map, window):
            continue


def manage_river(win_map, nr_iterations, window, spawn_rate):
    for iteration in range(nr_iterations):
        if spawn_rate < randint(0, 100):
            continue
        generate_river(win_map, window)


def generate_river(win_map, window):
    river = RiverPart(Point(randint(0, WINDOW_WIDTH - 10),
                            randint(0, WINDOW_HEIGHT - 10)))
    river.update_map_(win_map, window)

    last_corner = river.clone().getP1()
    while True:
        direction = randint(1, 4)

        if direction == 1:
            temp_river = RiverPart(Point(last_corner.getX() + 11,
                                         last_corner.getY()))
        elif direction == 2:
            temp_river = RiverPart(Point(last_corner.getX(),
                                         last_corner.getY() + 11))
        elif direction == 3:
            temp_river = RiverPart(Point(last_corner.getX() - 11,
                                         last_corner.getY()))
        elif direction == 4:
            temp_river = RiverPart(Point(last_corner.getX(),
                                         last_corner.getY() - 11))

        temp_river.update_map_(win_map, window)
        last_corner = temp_river.clone().getP1()
        if not temp_river.inside_win:
            break


def main():
    window_map = [[0 for col in range(WINDOW_WIDTH)]
                  for row in range(WINDOW_HEIGHT)]

    win = GraphWin("gen", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")

    manage_river(window_map, 8, win, 80)
    generate_trees(window_map, 100000, win, 20)
    generate_houses(window_map, 15000, win, 20)
    win.getMouse()


if __name__ == '__main__':
    main()
