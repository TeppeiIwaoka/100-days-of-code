import sys


print(" 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------\n 7 | 8 | 9 ")
chosen_number = input("Choose 1 as ○ or 2 as ×:")
if int(chosen_number) == 1:
    player1 = "○"
    player2 = "×"
elif int(chosen_number) == 2:
    player1 = "×"
    player2 = "○"
else:
    print("Invalid Number.Finish program")
    sys.exit()


left_number_list = list(range(1, 10, 1))
print(left_number_list)
chosen_number_player_dict = {}
square_string = " 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------\n 7 | 8 | 9 "

while len(left_number_list) >= 1:
    player1_number = input(f"{player1} choose number from {left_number_list}:")
    if int(player1_number) not in left_number_list:
        print("Invalid Number.Finish program")
        sys.exit()
    left_number_list.remove(int(player1_number))
    chosen_number_player_dict.setdefault(player1_number, player1)
    for key, value in chosen_number_player_dict.items():
        square_string = square_string.replace(str(key), value)
    print(square_string)

    while len(left_number_list) >= 1:
        player2_number = input(f"{player2} choose number from {left_number_list}:")
        if int(player2_number) not in left_number_list:
            print("Invalid Number.Finish program")
            sys.exit()
        left_number_list.remove(int(player2_number))
        chosen_number_player_dict.setdefault(player2_number, player2)
        for key, value in chosen_number_player_dict.items():
            square_string = square_string.replace(str(key), value)
        print(square_string)
        break


print("Finish Game")

