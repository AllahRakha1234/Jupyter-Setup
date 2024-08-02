import sys
import stdio # type: ignore
import stdarray # type: ignore


def check_sink_range(row_max, col_max, row, col, size):
    """
    Function to check whether a sink is in the correct position.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board
        row (int): The row of the sink
        col (int): The column of the sink

    Returns:
        bool: True if the sink is in the correct range, False otherwise.
    """
    if row < 0 or col < 0 or row + size > row_max or col + size > col_max:
        return False
    else:
        return True


def check_piece_range(row_max, col_max, row, col):
    """
    Function to check whether a piece is in the correct position.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board
        row (int): The row of the piece
        col (int): The column of the piece

    Returns:
        bool: True if the piece is in the correct range, False otherwise.
    """
    if 0 <= row < row_max and 0 <= col < col_max:
        return True
    else:
        return False


def check_piece_upright(row, col, board):
    """
    Function to check whether a piece is upright, or whether it is lying on it's
    side.

    Args:
        row (int): The row of the piece
        col (int): The column of the piece
        board (2D array of str): The game board

    Returns:
        bool: True if the piece is upright, False otherwise.
    """
    top_cell = board[row - 1][col] if row > 0 else None
    bottom_cell = board[row + 1][col] if row < len(board) - 1 else None
    left_cell = board[row][col - 1] if col > 0 else None
    right_cell = board[row][col + 1] if col < len(board[0]) - 1 else None

    if top_cell == board[row][col] and bottom_cell == board[row][col]:
        return True
    elif left_cell == board[row][col] and right_cell == board[row][col]:
        return False
    else:
        return None


def get_piece_fields(row, col, board):
    """
    Get all the coordinates belonging to the piece at coordinate (row, col).

    Args:
        row (int): The row of the piece
        col (int): The column of the piece
        board (2D array of str): The game board

    Returns:
        array of coordinates: The fields that the piece occupies
    """
    piece_type = board[row][col]
    piece_fields = []

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == piece_type:
                piece_fields.append((r, c))

    return piece_fields


def validate_move(row, col, direction, board):
    """
    Checks whether the given move is valid by checking that all aspects of the
    move are legal.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board

    Returns:
        bool: True if the move is valid, False otherwise
    """
    if not (0 <= row < len(board) and 0 <= col < len(board[0])):
        return False

    if direction == 'up':
        new_row, new_col = row - 1, col
    elif direction == 'down':
        new_row, new_col = row + 1, col
    elif direction == 'left':
        new_row, new_col = row, col - 1
    elif direction == 'right':
        new_row, new_col = row, col + 1
    else:
        return False

    if not (0 <= new_row < len(board) and 0 <= new_col < len(board[0])):
        return False

    if board[new_row][new_col] in [' ', board[row][col]]:
        return True
    else:
        return False


def do_move(row, col, direction, board, scores, gui_mode):
    """
    Executes the given move on the board.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board
        scores (array of int): The current scores for each player
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """
    if direction not in ['up', 'down', 'left', 'right']:
        stdio.writeln("Invalid direction! Please provide a valid direction: 'up', 'down', 'left', 'right'.")
        return
    
    new_row, new_col = row, col
    if direction == 'up':
        new_row -= 1
    elif direction == 'down':
        new_row += 1
    elif direction == 'left':
        new_col -= 1
    elif direction == 'right':
        new_col += 1

    if new_row < 0 or new_row >= len(board) or new_col < 0 or new_col >= len(board[0]):
        stdio.writeln("Cannot move outside the board!")
        return

    if board[new_row][new_col] != ' ':
        stdio.writeln("Cannot move to a non-empty cell!")
        return

    board[new_row][new_col] = board[row][col]
    board[row][col] = ' '


    print_and_read_board(board)



def generate_all_moves(board):
    """
    Generates a list of all moves (valid or invalid) that could potentially be
    played on the current board.

    Args:
        board (2D array of str): The game board

    Returns:
        array of moves: The moves that could be played on the given board
    """
    
    all_moves = []

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == ' ':
                all_moves.append((row, col, 'up'))
                all_moves.append((row, col, 'down'))
                all_moves.append((row, col, 'left'))
                all_moves.append((row, col, 'right'))

    return all_moves


def is_empty(row, col, board):
    return board[row][col] == ' '


def print_and_read_board(row_max, col_max):
    """
    Reads the board from standard input and prints it out.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board

    Returns:
        2D array of str: The game board
    """
    board = stdarray.create2D(row_max,col_max)
    piece_sizes = {'a': (1, 1, 1), 'b': (1, 1, 2), 'c': (1, 1, 3), 'd': (2, 2, 2)}

    for row in range(row_max):
        for col in range(col_max):
            board[row][col] = ' '



    num_rows = len(board)
    num_cols = len(board[0])

    # Print the board
    num_rows = len(board)
    num_cols = len(board[0])

    stdio.write(" ")
    for col in range(num_cols):
        stdio.write(f"{col:3}")
    stdio.writeln()

    for row in range(num_rows -1, -1, -1):
        stdio.write("  +")
        for col in range(num_cols):
            stdio.write("--+")
        stdio.writeln()
        stdio.write(f"{row} |")
        for col in range(num_cols):
            stdio.write(f"{board[row][col]} |")
        stdio.writeln()
    stdio.write("  +")
    for col in range(num_cols):
        stdio.write("--+")
    stdio.writeln()

       
    try:
        while True:
            line = stdio.readString()
            if line == '#':
                break  # Stop reading input when encountering '#'
            parts = line[0:1], line[2:3], line[4:5], line[6:7]  # Using array slicing
            if not parts:
                continue  # Skip empty lines
            obj_type, size, row, col = parts

            if obj_type == 's':
                if row.isdigit() and col.isdigit():
                    size = int(size)
                    row = int(row)
                    col = int(col)
                    if not check_sink_range(row_max, col_max, row, col, size):
                        stdio.writeln("ERROR: Sink in the wrong position")
                        sys.exit(1)
                    for i in range(row, row + size):
                        for j in range(col, col + size):
                            board[i][j] = 's'
                else:
                    stdio.writeln("ERROR: Missing information for 's' object")
                    sys.exit(1)
            elif obj_type == 'x':
                if row.isdigit() and col.isdigit():
                    row = int(row)
                    col = int(col)
                    board[row][col] = 'x'
                else:
                    stdio.writeln("ERROR: Missing coordinate for 'x' object")
                    sys.exit(1)
            elif obj_type in ['d', 'l']:
                if obj_type == 'd':
                    size = size.upper()
                else:
                    size = size.lower()
                for i in range(piece_sizes.get(size, (0, 0, 0))[0]):
                    for j in range(piece_sizes.get(size, (0, 0, 0))[1]):
                        if size == 'a':
                            board[row + i][col + j] = 'a'
                        elif size == 'b':
                            idx = (row + i) * col_max + (col + j)
                            if len(str(idx)) == 1:
                                idx = ' ' + str(idx)
                            else:
                                idx = str(idx)
                            if i == 0 and j == 0:
                                board[row + i][col + j] = 'b'
                            else:
                                board[row + i][col + j] = idx
                        elif size == 'c':
                            idx = (row + i) * col_max + (col + j)
                            if len(str(idx)) == 1:
                                idx = ' ' + str(idx)
                            else:
                                idx = str(idx)
                            if i == 0 and j == 0:
                                board[row + i][col + j] = 'c'
                            else:
                                board[row + i][col + j] = idx
                        elif size == 'd':
                            idx = (row + i) * col_max + (col + j)
                            if len(str(idx)) == 1:
                                idx = ' ' + str(idx)
                        else:
                            idx = str(idx)
                        if i == 0 and j == 0:
                            board[row + i][col + j] = 'd'
                        else:
                            board[row + i][col + j] = idx

    except EOFError:
        sys.exit(1)

    return board



def game_loop(board, gui_mode):
    """
    Executes the main game loop including
        * reading in a move
        * checking if the move is valid
        * if it is, doing the move
        * printing (or displaying) the board
        * and repeating.

    Args:
        board (2D array of str): The game board
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """

    player_turn = 1
    game_over = False

    while not game_over:

        while True:
            try:
                row_input = sys.stdin.readline().rstrip()  # Read row and remove trailing newline
                if not row_input:  # Check for EOF
                    raise EOFError()
                row = int(row_input)  # Convert to integer
                col_input = sys.stdin.readline().rstrip()  # Read column and remove trailing newline
                if not col_input:  # Check for EOF
                    raise EOFError()
                col = int(col_input)  # Convert to integer
                direction_input = sys.stdin.readline().rstrip()  # Read direction and remove trailing newline
                if not direction_input:  # Check for EOF
                    raise EOFError()
                direction = direction_input
                break
            except ValueError:
                stdio.writeln("Invalid input! Please enter valid integers for row and column.")
            except EOFError:
                sys.exit(1)

        if validate_move(row, col, direction, board):
            do_move(row, col, direction, board, [], gui_mode)
            player_turn = 2 if player_turn == 1 else 1
        else:
            stdio.writeln("Invalid move! Please try again.")

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def main():

    if len(sys.argv) < 4:
        stdio.writeln("ERROR: Too few arguments")
        sys.exit(1)
    elif len(sys.argv) > 4:
        stdio.writeln("ERROR: Too many arguments")
        sys.exit(1)
    elif len(sys.argv) == 4:
        row= sys.argv[1]
        col= sys.argv[2]
        gui_mode = sys.argv[3]
        if not is_integer(row) or not is_integer(col) or not is_integer(gui_mode):
                stdio.writeln("ERROR: Illegal argument")
                sys.exit(1)

        row_max = int(row)
        col_max = int(col)
        gui_mode = int(gui_mode)

    if row_max <= 0 or col_max <= 0:
        stdio.writeln("ERROR: Rows and columns must be positive integers")
        sys.exit(1)


    board = print_and_read_board(row_max, col_max)
    gui_mode = False 
    game_loop(board, gui_mode)

if __name__ == "__main__":
    main()
