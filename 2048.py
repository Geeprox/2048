import platform
import random
import os

system = platform.system()
if system == "Windows":
    clearCommand = "cls"
else:
    clearCommand = "clear"

path_of_date_file = './data/'
name_of_data_file = 'score.dat'
game_title = "==========[2048]=========="

matrix = []
random_options_list = []
matrix_n = 4
user_data = {}

current_user_name = ""
current_user_highest_score = 0
current_user_average_score = 0
current_user_played_times = 0
current_user_current_score = 0

add_done_once = False
nothing_done = False


def init_matrix():
    global matrix
    matrix = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


def load_data_file():
    data_file = open(path_of_date_file + name_of_data_file)

    while True:
        data = data_file.readline()
        if data:
            global current_user_name, current_user_highest_score, current_user_average_score, current_user_played_times
            current_user_name = data.split(":")[0]
            value = data.split(":")[1].split(",")
            current_user_highest_score = int(value[0])
            current_user_average_score = float(value[1])
            current_user_played_times = int(value[2])
            user_data[current_user_name] = \
                [current_user_highest_score, current_user_average_score, current_user_played_times]
        else:
            break

    data_file.close()


def check_if_exist_user():
    if not os.path.exists(path_of_date_file):
        os.mkdir(path_of_date_file)
    if os.path.isfile(path_of_date_file + name_of_data_file):
        load_data_file()
        return True
    else:
        return False


def init_current_game():
    global matrix
    init_matrix()
    set_random_position_value()
    set_random_position_value()

    global current_user_current_score
    current_user_current_score = 0


def quit_game():
    print("Quit Game")
    save_game()
    quit()


def save_game():
    data_file = open(path_of_date_file + name_of_data_file, "w+")
    user_data[current_user_name] = [current_user_highest_score, current_user_average_score, current_user_played_times]

    saving_data = ""
    for saving_key, saving_value in user_data.items():
        saving_data += saving_key + ":"
        for saving_value_ in saving_value:
            saving_data += str(saving_value_) + ","
        saving_data += "\n"
    data_file.write(saving_data)
    data_file.close()


def save_current_game():
    global current_user_name, current_user_highest_score, current_user_average_score, current_user_played_times
    current_user_sum_score = current_user_played_times * current_user_average_score
    current_user_sum_score += current_user_current_score
    current_user_played_times += 1
    current_user_average_score = current_user_sum_score / current_user_played_times
    if current_user_highest_score < current_user_current_score:
        current_user_highest_score = current_user_current_score
    user_data[current_user_name] = [current_user_highest_score, current_user_average_score, current_user_played_times]

    save_game()


def set_random_position_value():
    if check_exist_position():
        line, column = find_random_position()
        matrix[line][column] = 2


def check_exist_position():
    global random_options_list
    random_options_list = []
    for line in range(matrix_n):
        for column in range(matrix_n):
            if matrix[line][column] == 0:
                random_options_list.append([line, column])
    if len(random_options_list) != 0:
        return True
    else:
        return False


def find_random_position():
    index = random.randrange(0, len(random_options_list))
    return random_options_list[index][0], random_options_list[index][1]


def get_forward_position(current_position, direction):
    if direction == "Up":
        return [current_position[0] - 1, current_position[1]]
    elif direction == "Down":
        return [current_position[0] + 1, current_position[1]]
    elif direction == "Left":
        return [current_position[0], current_position[1] - 1]
    elif direction == "Right":
        return [current_position[0], current_position[1] + 1]


def out_of_checkerboard(destination):
    if destination[0] < 0 or destination[1] < 0 or destination[0] > matrix_n - 1 or destination[1] > matrix_n - 1:
        return True
    else:
        return False


def move_forward(current_position, direction):
    assert matrix[current_position[0]][current_position[1]] != 0
    global nothing_done, add_done_once, current_user_current_score
    destination = get_forward_position(current_position, direction)
    if out_of_checkerboard(destination):
        return
    else:
        if matrix[destination[0]][destination[1]] == 0:
            matrix[destination[0]][destination[1]] = matrix[current_position[0]][current_position[1]]
            matrix[current_position[0]][current_position[1]] = 0
            nothing_done = False
        else:
            if not add_done_once \
                    and matrix[destination[0]][destination[1]] == matrix[current_position[0]][current_position[1]]:
                matrix[destination[0]][destination[1]] *= 2
                matrix[current_position[0]][current_position[1]] = 0
                current_user_current_score += matrix[destination[0]][destination[1]]
                nothing_done = False
                add_done_once = True
        move_forward(destination, direction)


def move_up():
    print("Log: move up")
    global nothing_done, add_done_once
    nothing_done = True
    for column in range(matrix_n):
        add_done_once = False
        for line in range(matrix_n):
            if matrix[line][column] != 0:
                move_forward([line, column], "Up")

    if not nothing_done:
        set_random_position_value()


def move_down():
    print("Log: move down")
    global nothing_done, add_done_once
    nothing_done = True
    for column in range(matrix_n):
        add_done_once = False
        for line in range(matrix_n - 1, -1, -1):
            if matrix[line][column] != 0:
                move_forward([line, column], "Down")

    if not nothing_done:
        set_random_position_value()


def move_left():
    print("Log: move left")
    global nothing_done, add_done_once
    nothing_done = True
    for line in range(matrix_n):
        add_done_once = False
        for column in range(matrix_n):
            if matrix[line][column] != 0:
                move_forward([line, column], "Left")

    if not nothing_done:
        set_random_position_value()


def move_right():
    print("Log: move right")
    global nothing_done, add_done_once
    nothing_done = True
    for line in range(matrix_n):
        add_done_once = False
        for column in range(matrix_n - 1, -1, -1):
            if matrix[line][column] != 0:
                move_forward([line, column], "Right")

    if not nothing_done:
        set_random_position_value()


def check_result():
    not_game_over = False

    if not check_exist_position():
        for line in range(matrix_n):
            for column in range(matrix_n - 1):
                if matrix[line][column] == matrix[line][column+1]:
                    not_game_over = True
                    break

        for column in range(matrix_n):
            for line in range(matrix_n - 1):
                if matrix[line][column] == matrix[line+1][column]:
                    not_game_over = True
                    break
    else:
        not_game_over = True

    if not_game_over:
        return "Continue game"
    else:
        return "Game over"


def print_matrix():
    for line in matrix:
        for number in line:
            if number == 0:
                print("|" + "".center(4), end="")
            else:
                print("|" + str(number).center(4), end="")
        print("|\n+----+----+----+----+")


def show_leader_board():
    os.system(clearCommand)
    print("==========Leader board==========")
    for user, value in user_data.items():
        print(str(user) + ": " + str(value[0]))
    print("\nKey:Q to back")
    while True:
        if get_keyboard() == "Quit":
            return


def get_keyboard():
    input_from_keyboard = input()
    if input_from_keyboard == "W" or input_from_keyboard == "w":
        return "Up"
    elif input_from_keyboard == "S" or input_from_keyboard == "s":
        return "Down"
    elif input_from_keyboard == "A" or input_from_keyboard == "a":
        return "Left"
    elif input_from_keyboard == "D" or input_from_keyboard == "d":
        return "Right"
    elif input_from_keyboard == "L" or input_from_keyboard == "l":
        return "Leader_board"
    elif input_from_keyboard == "C" or input_from_keyboard == "c":
        return "Continue"
    elif input_from_keyboard == "Q" or input_from_keyboard == "q":
        return "Quit"
    elif input_from_keyboard == "P" or input_from_keyboard == "p":
        return "Pause"
    else:
        return input_from_keyboard


def register_new_user():
    user_name = input("Input a user name to sign up: ")
    if user_name in user_data.keys():
        load_exist_user(user_name)
    else:
        global current_user_name, current_user_highest_score, current_user_average_score, current_user_played_times
        current_user_name = user_name
        current_user_highest_score = 0
        current_user_average_score = 0
        current_user_played_times = 0
        user_data[user_name] = [0, 0, 0]


def load_exist_user(user_name):
    global current_user_name, current_user_highest_score, current_user_average_score, current_user_played_times
    current_user_name = user_name
    current_user_highest_score = user_data[user_name][0]
    current_user_average_score = user_data[user_name][1]
    current_user_played_times = user_data[user_name][2]


def refresh_paint():
    os.system(clearCommand)
    print(game_title)
    print("User: " + current_user_name)
    print("Score: " + str(current_user_current_score))
    print("Up:W | Down:S | Left:A | Right:D | Quit:Q | Pause:P")
    print("==========================\n")
    print("+----+----+----+----+")
    print_matrix()


def run_game():
    while True:
        refresh_paint()
        key = get_keyboard()
        if key == "Up":
            move_up()
        elif key == "Down":
            move_down()
        elif key == "Left":
            move_left()
        elif key == "Right":
            move_right()
        elif key == "Quit":
            quit_game()
        elif key == "Pause":
            pause_game()

        result = check_result()
        if result == "Game over":
            refresh_paint()
            print("==========Game Over==========\n\n")
            return


def pause_game():
    print(game_title)
    print("L:to Show leader board; C:to Continue game; Q:to Quit game")
    key = get_keyboard()
    if key == "Leader_board":
        show_leader_board()
    elif key == "Continue":
        return
    elif key == "Quit":
        quit_game()
    else:
        return


def init_game():
    exist_user = check_if_exist_user()
    if not exist_user:
        register_new_user()
    else:
        user = input("Input your user name to login: ")
        if user in user_data.keys():
            load_exist_user(user)
        else:
            print("No user found!")
            register_new_user()


def start_events_loop():
    while True:
        init_current_game()
        run_game()
        save_current_game()

        while True:
            print("C:to start a new game; Q:to quit")
            key = get_keyboard()
            if key == "Continue":
                break
            elif key == "Quit":
                quit_game()

# Run from here
init_game()
start_events_loop()
