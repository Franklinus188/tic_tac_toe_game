from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np

FONT_NAME = "Courier"
POSITIONS = [(20, 20), (235, 20), (450, 20), (20, 235), (235, 235), (450, 235), (20, 450), (235, 450), (450, 450)]
turn = 0
board = np.zeros((3, 3), dtype=np.int16)
game_session = 1
score = {"x": 0, "o": 0}


def create_buttons():
    # Create interactive place buttons and set them to board
    files = [
        "button" + str(i) for i in range(9)
    ]  # creates list to replace your actual inputs for troubleshooting purposes
    buttons = []  # creates list to store the buttons ins
    for i in range(len(files)):  # this says for *counter* in *however many elements there are in the list files*
        buttons.append(
            Button(
                canvas,
                text=files[i],
                image=blank_image,
                highlightthickness=0,
                bd=0,
                command=lambda c=i: put_symbol(buttons[c].cget("text")),
            )
        )
        buttons[i].place(x=POSITIONS[i][0], y=POSITIONS[i][1])  # this place the buttons
    return buttons


def put_symbol(button):
    global turn
    num = int(button[-1])
    if is_it_x_turn():
        btn[int(num)].config(image=xcross_image, command=0, relief="sunken")
        board[btn_pos[button][0]][btn_pos[button][1]] = 1
        turn_label.config(text="Turn: O")
    else:
        btn[int(num)].config(image=circle_image, command=0, relief="sunken")
        board[btn_pos[button][0]][btn_pos[button][1]] = 2
        turn_label.config(text="Turn: X")
    if check_win():
        if is_it_x_turn():
            score["x"] += 1
            if messagebox.askyesno("X won!", "X won this game!\nDo you want retry?"):
                restart_game()
            else:
                root.destroy()
        else:
            score["o"] += 1
            if messagebox.askyesno("O won!", "O won this game!\nDo you want retry?"):
                restart_game()
            else:
                root.destroy()
    if board.all() != 0:
        if messagebox.askyesno("Draw", "No one won this game!\nDo you want retry?"):
            restart_game()
        else:
            root.destroy()
    turn += 1


def check_win():
    if (
        (board[0][0] == board[0][1] == board[0][2] != 0)
        or (board[1][0] == board[1][1] == board[1][2] != 0)
        or (board[2][0] == board[2][1] == board[2][2] != 0)
        or (board[0][0] == board[1][0] == board[2][0] != 0)
        or (board[0][1] == board[1][1] == board[2][1] != 0)
        or (board[0][2] == board[1][2] == board[2][2] != 0)
        or (board[0][0] == board[1][1] == board[2][2] != 0)
        or (board[2][0] == board[1][1] == board[0][2] != 0)
    ):
        return True
    return False


def is_it_x_turn():
    if turn % 2 == 0:
        return True
    else:
        return False


def restart_game():
    global turn, board, btn, game_session
    if game_session % 2 == 0:
        turn = -1
    else:
        turn = 0
    board = np.zeros((3, 3), dtype=np.int16)
    btn = create_buttons()
    game_session += 1
    game_label.config(text=f"Game:{game_session}")
    score_label.config(text=f"X-{score['x']} O-{score['o']}")


def who_won():
    if score["x"] == score["o"]:
        return "Draw."
    if score["x"] > score["o"]:
        return "X Won!"
    else:
        return "O Won!"


# Window config
root = Tk()
root.title("Tic Tac Toe")
root.geometry("754x754")
root.config(padx=50, pady=65, bg="black")
# Import images
board_image = ImageTk.PhotoImage(Image.open("board.png"))
xcross_image = ImageTk.PhotoImage(Image.open("x-cross.png"))
circle_image = ImageTk.PhotoImage(Image.open("circle.png"))
blank_image = ImageTk.PhotoImage(Image.open("blank.png"))
# Create background canvas
canvas = Canvas(root, width=654, height=654)
canvas.create_image(327, 327, image=board_image)
canvas.place(x=0, y=0)

# Connect buttons with array
btn = create_buttons()
pos_list = [(x, y) for x in range(3) for y in range(3)]
btn_pos = {btn[i].cget("text"): pos_list[i] for i in range(len(btn))}

# Create labels to show score, turn, games
turn_label = Label(root, text="Turn: X", font=(FONT_NAME, 32, "bold"))
turn_label.place(anchor="n", x=327, y=-60)

game_label = Label(root, text=f"Game:{game_session}", font=(FONT_NAME, 32, "bold"))
game_label.place(anchor="ne", x=654, y=-60)

score_label = Label(root, text=f"X-{score['x']} O-{score['o']}", font=(FONT_NAME, 32, "bold"))
score_label.place(anchor="nw", x=0, y=-60)


root.mainloop()

messagebox.showinfo("Game results", f"Games: {game_session}\nScore: X-{score['x']}   O-{score['o']}\n{who_won()}")
print(f"Games: {game_session}\nScore: X-{score['x']} O-{score['o']}\n{who_won()}")
