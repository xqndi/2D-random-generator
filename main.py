import json
from graphics import *
from random import randint


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

X_CENTER = WINDOW_WIDTH / 2
Y_CENTER = WINDOW_HEIGHT / 2

                                    # MAKE THEM LOCAL
surnames_list = []
male_names_list = []
female_names_list = []

lake_extras = ["Lake", "Lagoon", "Sea", "Pond"]
lakes_list = []
lake_dict = {}


def main():
    house_list = []

    parse_json_files()

    window_map = [[0 for col in range(WINDOW_WIDTH)]
                  for row in range(WINDOW_HEIGHT)]

    win = GraphWin("gen", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("green")

    manage_river(window_map, 9, win, 75)
    generate_trees(window_map, 100000, win, 20)
    generate_houses(window_map, 25000, win, 20, house_list)

    while True:
        mouse = win.getMouse()
        if not mouse:
            continue
        print(window_map[int(mouse.getY())][int(mouse.getX())])
        check_houses(house_list, mouse, win)
        check_lakes(mouse, window_map, win)


class Family:
    def __init__(self):
        self.surname = surnames_list[randint(0, len(surnames_list) - 1)]
        self.names = []
        self.male_index_list = []
        self.female_index_list = []

        for it in range(randint(1, 5)):
            if randint(0, 1):
                self.create_male()
            else:
                self.create_female()

    def create_female(self):
        valid_name = False
        while not valid_name:
            index = randint(0, 4)
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

    def create_male(self):
        valid_name = False
        while not valid_name:
            index = randint(0, 4)
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
        self.setFill("greenyellow")
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


def generate_trees(win_map, nr_trees, window, neighbor_size):
    for tree in range(nr_trees):
        while True:
            temp_tree = Tree(randint(0, WINDOW_WIDTH - 10), randint(0, WINDOW_HEIGHT - 10))
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
    def __init__(self, top_corner):
        self.size = 1
        self.family = Family()
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


def generate_houses(win_map, nr_houses, window, neighbor_size, houses_list):
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
                houses_list.append(temp_house)
                temp_house.draw(window)
                break


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


def generate_lakes(win_map, nr_iterations, window):
    for attempt in range(nr_iterations):
        if randint(0, 2):
            continue
        temp_lake = Lake(Point(randint(0, WINDOW_WIDTH - 10),
                               randint(0, WINDOW_HEIGHT - 10)), randint(40, 100))
        if not temp_lake.update_map_(win_map, window):
            continue


class RiverPart(Rectangle):
    def __init__(self, top_corner, key):
        self.size = 10
        self.map_key = key
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
                win_map[row_y][col_x] = self.map_key


def generate_river(win_map, window, map_key):
    river = RiverPart(Point(randint(0, WINDOW_WIDTH - 10),
                            randint(0, WINDOW_HEIGHT - 10)), map_key)
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


def manage_river(win_map, nr_iterations, window, spawn_rate):
    used_lake_indices = []

    for iteration in range(nr_iterations):
        if spawn_rate < randint(0, 100):
            continue
        create_lake_name(iteration + 4, used_lake_indices)
        generate_river(win_map, window, iteration + 4)

    print(used_lake_indices)


def create_lake_name(key, used_lake_indices):
    while True:
        new_index = randint(0, len(lakes_list) - 1)
        if new_index not in used_lake_indices:
            break

    name = lakes_list[new_index]
    used_lake_indices.append(new_index)

    lake_title = randint(0, len(lake_extras) - 1)
    if lake_title:
        name = name + " " + lake_extras[lake_title]
    else:
        name = lake_extras[lake_title] + " " + name

    lake_dict[str(key)] = name
    print(lake_dict[str(key)])


def check_lakes(mouse_point, win_map, graph_win):
    key = win_map[int(mouse_point.getY())][int(mouse_point.getX())]
    print("key: " + str(key))

    if key < 4:
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


def parse_json_files():
    Surnames_file = open('babynames/Surnames.json')
    Babynames_file = open('babynames/Names.json')
    Lakenames_file = open('babynames/Lake_Names.json')

    Surname_data = json.load(Surnames_file)

    for name in Surname_data:
        surnames_list.append(name["surname"])
    Surnames_file.close()

    Babyname_data = json.load(Babynames_file)

    name_index = 0
    for name in Babyname_data:
        if name_index % 2 == 0:
            male_names_list.append(name["name"])
        else:
            female_names_list.append(name["name"])

        name_index += 1
    male_names_list.pop()
    Babynames_file.close()

    Lakename_data = json.load(Lakenames_file)
    for lake_name in Lakename_data:
        lakes_list.append(lake_name["lake"])
    Lakenames_file.close()

    print(lakes_list)
    print(surnames_list)
    print(female_names_list)
    print(male_names_list)


if __name__ == '__main__':
    main()
