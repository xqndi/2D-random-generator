import json
from babynames.babynames.spiders import surnames_spider,\
    names_spider, lakes_spider, lakesall_spider, mountains_spider, canyons_spider
from scrapy.crawler import CrawlerProcess
from pathlib import Path
from random import randint, gauss
from graphics import *


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

X_CENTER = WINDOW_WIDTH / 2
Y_CENTER = WINDOW_HEIGHT / 2


def main():
    house_list = []
    surnames_list = []
    male_names_list = []
    female_names_list = []
    lakes_list = []
    lake_dict = {}
    mountains_list = []
    mountain_dict = {}
    canyons_list = []
    canyons_dict = {}

    parse_json_files(surnames_list, male_names_list, female_names_list,
                     lakes_list, mountains_list, canyons_list)

    window_map = [[0 for col in range(WINDOW_WIDTH)]
                  for row in range(WINDOW_HEIGHT)]

    win = GraphWin("gen", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("seagreen")

    CanyonPart.manage_canyon(window_map, 3, win, 50, canyons_dict, canyons_list)
    Mountain.manage_mountains(window_map, 7, win, 80, mountain_dict, mountains_list)
    RiverPart.manage_river(window_map, 16, win, 75, lake_dict, lakes_list)
    Tree.generate_trees(window_map, 200000, win, 20)
    House.generate_houses(window_map, 20000, win, 20, house_list,
                          surnames_list, male_names_list, female_names_list)

    while True:
        mouse = win.getMouse()
        if not mouse:
            continue
        print(window_map[int(mouse.getY())][int(mouse.getX())])
        House.check_houses(house_list, mouse, win)
        RiverPart.check_lakes(mouse, window_map, win, lake_dict)
        Mountain.check_mountains(mouse, window_map, win, mountain_dict)
        CanyonPart.check_canyons(mouse, window_map, win, canyons_dict)


class Family:
    def __init__(self, surnames_list, male_names_list, female_names_list):
        self.surname = surnames_list[randint(0, len(surnames_list) - 1)]
        self.names = []
        self.male_index_list = []
        self.female_index_list = []

        for it in range(randint(1, 5)):
            if randint(0, 1):
                self.create_male(male_names_list)
            else:
                self.create_female(female_names_list)

    def create_female(self, female_names_list):
        valid_name = False
        while not valid_name:
            index = randint(0, len(female_names_list) - 1)
            counter = self.female_index_list.count(index)

            if counter == 1:
                self.names.append(female_names_list[index])
                self.names[-1] = self.names[-1] + ", the 2nd"
                self.female_index_list.append(index)
                return

            if counter > 1:
                continue

            self.names.append(female_names_list[index])
            self.female_index_list.append(index)
            return

    def create_male(self, male_names_list):
        valid_name = False
        while not valid_name:
            index = randint(0, len(male_names_list) - 1)
            counter = self.male_index_list.count(index)

            if counter == 1:
                self.names.append(male_names_list[index])
                self.names[-1] = self.names[-1] + " Jr."
                self.male_index_list.append(index)
                return

            if counter > 1:
                continue

            self.names.append(male_names_list[index])
            self.male_index_list.append(index)
            return

    def print_all(self):
        for person in self.names:
            print(self.surname + " " + person)

    def display_all(self, graph_win):
        height_offset = 0
        entry_list = []

        for person in self.names:
            text = Entry(Point(118, 15 + height_offset), 25)
            text.setText(self.surname + " " + person)
            text.setFill("brown")
            text.draw(graph_win)

            entry_list.append(text)
            height_offset += 25

        # keep displaying while mouse is not not clicked
        while not graph_win.getMouse():
            continue

        for entry in entry_list:
            entry.undraw()


class Tree(Point):
    def __init__(self, x_pos, y_pos):
        self.nr_living_neighbors = 0
        self.dist_center = -1

        Point.__init__(self, x_pos, y_pos)
        self.setFill("darkgreen")
        self.temp_y = int(self.getY())
        self.temp_x = int(self.getX())

    def update_map_(self, win_map, window):
        if not win_map[self.temp_y][self.temp_x]:
            win_map[self.temp_y][self.temp_x] = 3
            self.draw(window)
            return True
        return False

    def count_neighbors_(self, win_map, neighbor_size):

        for index in range(-neighbor_size, neighbor_size + 1):
            if index == 0:
                continue
            if (0 <= self.temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y + index][self.temp_x] == 3):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (win_map[self.temp_y][self.temp_x + index] == 3):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= self.temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y + index][self.temp_x + index] == 3):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= self.temp_y - index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y - index][self.temp_x + index] == 3):
                self.nr_living_neighbors += 1

    def distance_to_center(self):
        x_dist = abs(self.getX() - X_CENTER)
        y_dist = abs(self.getY() - Y_CENTER)

        self.dist_center = x_dist + y_dist

        if self.dist_center > (WINDOW_HEIGHT - Y_CENTER):
            self.dist_center = WINDOW_HEIGHT - Y_CENTER

    @staticmethod
    def generate_trees(win_map, nr_trees, window, neighbor_size):
        for tree in range(nr_trees):
            while True:
                temp_tree = Tree(randint(0, WINDOW_WIDTH - 2), randint(0, WINDOW_HEIGHT - 2))
                temp_tree.distance_to_center()
                if temp_tree.dist_center < randint(50, WINDOW_HEIGHT - 100):
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


class House(Rectangle):
    def __init__(self, top_corner, surnames_list, male_names_list, female_names_list):
        self.size = 1
        self.family = Family(surnames_list, male_names_list, female_names_list)
        self.nr_living_neighbors = 0
        self.upper_corner = top_corner
        self.lower_corner = Point(top_corner.getX() + self.size,
                                  top_corner.getY() + self.size)
        Rectangle.__init__(self, self.upper_corner, self.lower_corner)
        self.setFill("black")
        self.setOutline("black")
        self.temp_y = int(self.upper_corner.getY())
        self.temp_x = int(self.upper_corner.getX())

    def update_map_(self, win_map):

        if not win_map[self.temp_y][self.temp_x]:
            win_map[self.temp_y][self.temp_x] = 1
        else:
            return False

        if not win_map[self.temp_y + 1][self.temp_x]:
            win_map[self.temp_y + 1][self.temp_x] = 1
        else:
            return False

        if not win_map[self.temp_y][self.temp_x + 1]:
            win_map[self.temp_y][self.temp_x + 1] = 1
        else:
            return False

        if not win_map[self.temp_y + 1][self.temp_x + 1]:
            win_map[self.temp_y + 1][self.temp_x + 1] = 1
        else:
            return False

        return True

    def count_neighbors_(self, win_map, neighbor_size):

        for index in range(-neighbor_size, neighbor_size + 2):
            if index == 0:
                continue
            if (0 <= self.temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y + index][self.temp_x] == 1):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (win_map[self.temp_y][self.temp_x + index] == 1):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= self.temp_y + index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y + index][self.temp_x + index] == 1):
                self.nr_living_neighbors += 1
            if (0 <= self.temp_x + index <= WINDOW_WIDTH - 1) and \
                    (0 <= self.temp_y - index <= WINDOW_HEIGHT - 1) and \
                    (win_map[self.temp_y - index][self.temp_x + index] == 1):
                self.nr_living_neighbors += 1

    @staticmethod
    def generate_houses(win_map, nr_houses, window, neighbor_size, houses_list,
                        surnames_list, male_names_list, female_names_list):
        for house in range(nr_houses):
            while True:
                temp_house = House(Point(randint(0, WINDOW_WIDTH - 2),
                                         randint(0, WINDOW_HEIGHT - 2)),
                                   surnames_list, male_names_list, female_names_list)
                temp_house.count_neighbors_(win_map, neighbor_size)

                if temp_house.nr_living_neighbors == 0 and \
                        randint(0, 10 * neighbor_size) != 0:
                    break
                spawn_threshold = randint(0, int(neighbor_size / 5))
                if temp_house.nr_living_neighbors < spawn_threshold:
                    break
                if temp_house.update_map_(win_map):
                    houses_list.append(temp_house)
                    temp_house.draw(window)
                    break

    @staticmethod
    def check_houses(houses_list, mouse_point, graph_window):
        mouse_x = mouse_point.getX()
        mouse_y = mouse_point.getY()

        for house in houses_list:
            house_x = house.upper_corner.getX()
            house_y = house.upper_corner.getY()

            for offset in range(-1, 2):
                if (mouse_x + offset == house_x) and (mouse_y == house_y):
                    house.family.display_all(graph_window)
                    return
                if (mouse_x + offset == house_x) and (mouse_y + offset == house_y):
                    house.family.display_all(graph_window)
                    return
                if (mouse_x == house_x) and (mouse_y + offset == house_y):
                    house.family.display_all(graph_window)
                    return
                if (mouse_x - offset == house_x) and (mouse_y + offset == house_y):
                    house.family.display_all(graph_window)
                    return


#       ---------- class currently not in use ----------
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

    @staticmethod
    def generate_lakes(win_map, nr_iterations, window):
        for attempt in range(nr_iterations):
            if randint(0, 2):
                continue
            temp_lake = Lake(Point(randint(0, WINDOW_WIDTH - 2),
                                   randint(0, WINDOW_HEIGHT - 2)), randint(40, 100))
            if not temp_lake.update_map_(win_map, window):
                continue


class Mountain(Rectangle):
    def __init__(self, upper_corner, size):
        self.size = size
        Rectangle.__init__(self, upper_corner, Point(upper_corner.getX() + self.size,
                                                     upper_corner.getY() + self.size))
        self.setFill("gray")
        self.low_x = int(self.getP1().getX())
        self.low_y = int(self.getP1().getY())
        self.high_x = int(self.getP2().getX())
        self.high_y = int(self.getP2().getY())

    def update_map(self, win_map, window, key):
        for row_y in range(self.low_y - 1, self.high_y + 1):
            for col_x in range(self.low_x - 1, self.high_x + 1):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    return False
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    return False
                if win_map[row_y][col_x]:
                    return False

        self.draw(window)

        for row_y in range(self.low_y - 1, self.high_y + 1):
            for col_x in range(self.low_x - 1, self.high_x + 1):
                win_map[row_y][col_x] = key
        return True

    def fill(self, graph_win):
        inner_dist = 3
        while True:
            inner_p1_x = self.getP1().getX() + inner_dist
            inner_p1_y = self.getP1().getY() + inner_dist
            inner_p2_x = self.getP2().getX() - inner_dist
            inner_p2_y = self.getP2().getY() - inner_dist

            if (inner_p2_x - inner_p1_x <= 3) or (inner_p2_y - inner_p1_y <= 3):
                break

            temp_rec = Rectangle(Point(inner_p1_x, inner_p1_y),
                                 Point(inner_p2_x, inner_p2_y))
            temp_rec.draw(graph_win)
            if inner_dist % 6:
                temp_rec.setFill("dimgrey")
            else:
                temp_rec.setFill("gray")

            inner_dist += 3

    @staticmethod
    def generate_mountains(win_map, window, key):
        while True:
            temp_size = 5 * randint(8, 50)
            temp_mountain = Mountain(Point(randint(0, WINDOW_WIDTH - 2),
                                           randint(0, WINDOW_HEIGHT - 2)), temp_size)
            if temp_mountain.update_map(win_map, window, key):
                temp_mountain.fill(window)
                return

    @staticmethod
    def manage_mountains(win_map, nr_iterations, window, spawn_rate, mountain_dict, mountains_list):
        used_mountain_indices = []

        for iteration in range(nr_iterations):
            if spawn_rate < randint(0, 100):
                continue
            Mountain.create_mountain_name(- (iteration + 1), used_mountain_indices,
                                          mountain_dict, mountains_list)
            Mountain.generate_mountains(win_map, window, - (iteration + 1))

        print(used_mountain_indices)

    @staticmethod
    def create_mountain_name(key, used_mountain_indices, mountain_dict, mountains_list):
        extras = ["Highlands", "Hillside", "Peaks", "Rise", "Heights"]
        while True:
            new_index = randint(0, len(mountains_list) - 1)
            if new_index not in used_mountain_indices:
                break

        name = mountains_list[new_index]
        if len(name.split()) == 1:
            name = "The" + " " + name + " " + extras[randint(0, len(extras) - 1)]
            print("-----------------")
            print(name)
        used_mountain_indices.append(new_index)

        mountain_dict[str(key)] = name
        print(mountain_dict[str(key)])

    @staticmethod
    def check_mountains(mouse_point, win_map, graph_win, mountain_dict):
        key = win_map[int(mouse_point.getY())][int(mouse_point.getX())]
        print("key(mountain): " + str(key))

        if key >= 0:
            return
        text = Entry(Point(150, 15), 32)

        text.setText(mountain_dict[str(key)])
        text.setStyle("italic")
        text.setFill("mediumorchid")
        text.draw(graph_win)

        # keep displaying while mouse is not not clicked
        while not graph_win.getMouse():
            continue

        text.undraw()


class CanyonPart(Rectangle):
    def __init__(self, top_corner, key):
        self.size = 20
        self.map_key = key
        self.inside_win = True
        Rectangle.__init__(self, top_corner, Point(top_corner.getX() + self.size,
                                                   top_corner.getY() + self.size))
        self.setOutline("sienna")
        self.setFill("peru")

    def update_map_(self, win_map, window):
        low_x = int(self.getP1().getX())
        low_y = int(self.getP1().getY())
        high_x = int(self.getP2().getX())
        high_y = int(self.getP2().getY())

        is_valid = True

        for row_y in range(low_y, high_y):
            for col_x in range(low_x, high_x):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    continue
                if win_map[row_y][col_x] and (win_map[row_y][col_x] != self.map_key):
                    is_valid = False

        if not is_valid:
            return False

        self.draw(window)

        for row_y in range(low_y, high_y):
            for col_x in range(low_x, high_x):
                if not (0 <= row_y <= WINDOW_HEIGHT - 1):
                    self.inside_win = False
                    break
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    self.inside_win = False
                    break
                win_map[row_y][col_x] = self.map_key
        return True

    @staticmethod
    def generate_canyon(win_map, window, map_key, general_direction,
                        general_linearity, starting_point):
        canyon = CanyonPart(starting_point, map_key)
        canyon.update_map_(win_map, window)

        last_corner = canyon.clone().getP1()
        last_direction = 1
        counter = 0
        while True:
            temp_canyon = -1
            if counter < 3:
                direction = general_direction
            elif randint(1, 10) < general_linearity:
                direction = general_direction
            elif randint(0, 1):
                if last_direction < 4:
                    direction = last_direction + 1
                else:
                    direction = last_direction - 3
            else:
                if last_direction > 1:
                    direction = last_direction - 1
                else:
                    direction = last_direction + 3

            if direction == 1:
                temp_canyon = CanyonPart(Point(last_corner.getX() + 20,
                                               last_corner.getY()), map_key)
            elif direction == 2:
                temp_canyon = CanyonPart(Point(last_corner.getX(),
                                               last_corner.getY() + 20), map_key)
            elif direction == 3:
                temp_canyon = CanyonPart(Point(last_corner.getX() - 20,
                                               last_corner.getY()), map_key)
            elif direction == 4:
                temp_canyon = CanyonPart(Point(last_corner.getX(),
                                               last_corner.getY() - 20), map_key)

            if not temp_canyon.update_map_(win_map, window):
                break
            last_corner = temp_canyon.clone().getP1()
            last_direction = direction
            counter += 1
            if not temp_canyon.inside_win:
                break

    @staticmethod
    def manage_canyon(win_map, nr_iterations, window, spawn_rate, canyon_dict, canyons_list):
        used_canyon_indices = []

        for iteration in range(nr_iterations):
            if spawn_rate < randint(0, 100):
                continue

            starting_edge = randint(1, 4)

            if starting_edge == 1:
                x_pos = 0
                raw_y_pos = randint(20, WINDOW_HEIGHT - 20)
                y_pos = my_round(raw_y_pos, WINDOW_HEIGHT - 20)
                general_dir = 1
            elif starting_edge == 2:
                raw_x_pos = randint(20, WINDOW_WIDTH - 20)
                x_pos = my_round(raw_x_pos, WINDOW_WIDTH - 20)
                y_pos = 0
                general_dir = 2
            elif starting_edge == 3:
                x_pos = WINDOW_WIDTH
                raw_y_pos = randint(20, WINDOW_HEIGHT - 20)
                y_pos = my_round(raw_y_pos, WINDOW_HEIGHT - 20)
                general_dir = 3
            else:
                raw_x_pos = randint(20, WINDOW_WIDTH - 20)
                x_pos = my_round(raw_x_pos, WINDOW_WIDTH - 20)
                y_pos = WINDOW_HEIGHT
                general_dir = 4

            linearity = int(gauss(5, 2))
            if linearity > 9:
                linearity = 9
            elif linearity < 1:
                linearity = 1

            CanyonPart.create_canyon_name(iteration + 100, used_canyon_indices,
                                          canyon_dict, canyons_list)
            CanyonPart.generate_canyon(win_map, window, iteration + 100,
                                       general_dir, linearity, Point(x_pos, y_pos))

        print(used_canyon_indices)

    @staticmethod
    def create_canyon_name(key, used_canyon_indices, canyon_dict, canyons_list):
        while True:
            new_index = randint(0, len(canyons_list) - 1)
            if new_index not in used_canyon_indices:
                break

        name = canyons_list[new_index]
        used_canyon_indices.append(new_index)

        canyon_dict[str(key)] = name
        print(canyon_dict[str(key)])

    @staticmethod
    def check_canyons(mouse_point, win_map, graph_win, canyon_dict):
        key = win_map[int(mouse_point.getY())][int(mouse_point.getX())]
        print("key(can): " + str(key))

        if key < 100:
            return
        text = Entry(Point(118, 15), 25)

        text.setText(canyon_dict[str(key)])
        text.setStyle("italic")
        text.setFill("orange")
        text.draw(graph_win)

        # keep displaying while mouse is not not clicked
        while not graph_win.getMouse():
            continue

        text.undraw()


class RiverPart(Rectangle):
    def __init__(self, top_corner, key):
        self.size = 10
        self.map_key = key
        self.inside_win = True
        Rectangle.__init__(self, top_corner, Point(top_corner.getX() + self.size,
                                                   top_corner.getY() + self.size))
        # self.setOutline("blue")
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
                    continue
                if not (0 <= col_x <= WINDOW_WIDTH - 1):
                    self.inside_win = False
                    continue
                win_map[row_y][col_x] = self.map_key

    @staticmethod
    def generate_river(win_map, window, map_key):
        river = RiverPart(Point(randint(0, WINDOW_WIDTH - 2),
                                randint(0, WINDOW_HEIGHT - 2)), map_key)
        river.update_map_(win_map, window)

        last_corner = river.clone().getP1()
        while True:
            direction = randint(1, 4)
            temp_river = -1

            if direction == 1:
                temp_river = RiverPart(Point(last_corner.getX() + 11,
                                             last_corner.getY()), map_key)
            elif direction == 2:
                temp_river = RiverPart(Point(last_corner.getX(),
                                             last_corner.getY() + 11), map_key)
            elif direction == 3:
                temp_river = RiverPart(Point(last_corner.getX() - 11,
                                             last_corner.getY()), map_key)
            elif direction == 4:
                temp_river = RiverPart(Point(last_corner.getX(),
                                             last_corner.getY() - 11), map_key)

            temp_river.update_map_(win_map, window)
            last_corner = temp_river.clone().getP1()
            if not temp_river.inside_win:
                break

    @staticmethod
    def manage_river(win_map, nr_iterations, window, spawn_rate, lake_dict, lakes_list):
        used_lake_indices = []

        for iteration in range(nr_iterations):
            if spawn_rate < randint(0, 100):
                continue
            RiverPart.create_lake_name(iteration + 4, used_lake_indices, lake_dict, lakes_list)
            RiverPart.generate_river(win_map, window, iteration + 4)

        print(used_lake_indices)

    @staticmethod
    def create_lake_name(key, used_lake_indices, lake_dict, lakes_list):
        while True:
            new_index = randint(0, len(lakes_list) - 1)
            if new_index not in used_lake_indices:
                break

        name = lakes_list[new_index]
        used_lake_indices.append(new_index)

        lake_dict[str(key)] = name
        print(lake_dict[str(key)])

    @staticmethod
    def check_lakes(mouse_point, win_map, graph_win, lake_dict):
        key = win_map[int(mouse_point.getY())][int(mouse_point.getX())]
        print("key: " + str(key))

        if (key < 4) or (key >= 100):
            return
        text = Entry(Point(118, 15), 25)

        text.setText(lake_dict[str(key)])
        text.setStyle("italic")
        text.setFill("lightblue")
        text.draw(graph_win)

        # keep displaying while mouse is not not clicked
        while not graph_win.getMouse():
            continue

        text.undraw()


def parse_json_files(surnames_list, male_names_list, female_names_list,
                     lakes_list, mountains_list, canyons_list):
    run_spiders()

    Surnames_file = open('babynames/Surnames.json')
    Babynames_file = open('babynames/Names.json')
    Texas_lakes_file = open('babynames/Lake_Names.json')
    World_lakes_file = open('babynames/Lakes_All.json')
    Mountains_file = open('babynames/Mountains.json')
    Canyons_file = open('babynames/Canyons.json')

    Surname_data = json.load(Surnames_file)
    for name in Surname_data:
        surnames_list.append(name["surname"])
    Surnames_file.close()

    Babyname_data = json.load(Babynames_file)
    name_index = 0
    for name in Babyname_data:
        if name_index < 1000:
            male_names_list.append(name["name"])
        else:
            female_names_list.append(name["name"])
        name_index += 1
    Babynames_file.close()

    Texas_lake_data = json.load(Texas_lakes_file)
    lake_extras = ["Lake", "Lagoon", "Sea", "Pond"]
    for lake_name in Texas_lake_data:
        lakes_list.append(lake_name["lake"])
        lake_title = randint(0, len(lake_extras) - 1)
        if lake_title:
            lakes_list[-1] = lakes_list[-1] + " " + lake_extras[lake_title]
        else:
            lakes_list[-1] = lake_extras[lake_title] + " " + lakes_list[-1]
    Texas_lakes_file.close()

    World_lake_data = json.load(World_lakes_file)
    for lake_name in World_lake_data:
        lakes_list.append(lake_name["lake_name"])
    World_lakes_file.close()

    Mountains_data = json.load(Mountains_file)
    for mountain_name in Mountains_data:
        mountains_list.append(mountain_name["mountain"])
    Mountains_file.close()

    Canyons_data = json.load(Canyons_file)
    for canyon_name in Canyons_data:
        canyons_list.append(canyon_name["canyon"])
    Canyons_file.close()

    print(lakes_list)
    print(surnames_list)
    print(female_names_list)
    print(male_names_list)
    print(mountains_list)
    print(canyons_list)


def run_spiders():
    process = 0
    if not Path('babynames/Surnames.json').is_file():
        print("crawling for surnames...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Surnames.json": {"format": "json"},
            },
        })
        process.crawl(surnames_spider.SurnamesSpider)

    if not Path('babynames/Names.json').is_file():
        print("crawling for names...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Names.json": {"format": "json"},
            },
        })
        process.crawl(names_spider.NamesSpider)

    if not Path('babynames/Lake_Names.json').is_file():
        print("crawling for Texas-lakes...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Lake_Names.json": {"format": "json"},
            },
        })
        process.crawl(lakes_spider.LakesSpider)

    if not Path('babynames/Lakes_All.json').is_file():
        print("crawling for all lakes...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Lakes_All.json": {"format": "json"},
            },
        })
        process.crawl(lakesall_spider.LakesAllSpider)

    if not Path('babynames/Mountains.json').is_file():
        print("crawling for mountains...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Mountains.json": {"format": "json"},
            },
        })
        process.crawl(mountains_spider.MountainsSpider)

    if not Path('babynames/Canyons.json').is_file():
        print("crawling for canyons...")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "babynames/Canyons.json": {"format": "json"},
            },
        })
        process.crawl(canyons_spider.CanyonsSpider)

    if process:
        process.start()


def my_round(x, upper_limit, base=20):
    val = base * round(x/base)

    if val > upper_limit:
        val = upper_limit

    return val


if __name__ == '__main__':
    main()
