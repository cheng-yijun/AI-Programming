import copy
import random


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True
        # detect drop phase
        count = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != ' ':
                    count += 1
        if count >= 8:
            drop_phase = False

        move = []
        (row, col) = (random.randint(0, 4), random.randint(0, 4))
        (scr_row, scr_col) = (random.randint(0, 4), random.randint(0, 4))
        if not drop_phase:
            # choose a piece to move and remove it from the board
            #
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            # get all the valid coordinates for my_piece
            succs = self.succ(state, self.my_piece)
            max_succ = succs[0]
            max_score = self.heuristic_game_value(succs[0])
            max = float("-inf")
            next_state = None
            count_my = 0
            for i in range(5):
                for j in range(5):
                    if state[i][j] == self.my_piece:
                        count_my += 1
            for succ in succs:
                if_adj = self.check_distance(succ, count_my)
                if not if_adj:
                    continue
                score = self.Min_value(succ, 0)
                if score > max:
                    max = score
                    next_state = succ

            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ' and next_state[i][j] == self.my_piece:
                        (row, col) = (i, j)
                    if state[i][j] == self.my_piece and next_state[i][j] == ' ':
                        (scr_row, scr_col) = (i, j)
            move.insert(0, (row, col))
            move.insert(1, (scr_row, scr_col))
            return move

        # select an unoccupied space randomly
        # implement a minimax algorithm to play better

        first_drop = True  # first time to drop
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    first_drop = False
                    break
        if first_drop is True:
            if state[2][2] == ' ':
                move.insert(0, (2, 2))
            else:
                move.insert(0, (2, 1))
            return move

        succs = self.succ(state, self.my_piece)
        #  max_succ = succs[0]
        max_score = self.heuristic_game_value(succs[0])
        max_successors = []
        for cur_succ in succs:
            cur_score = self.heuristic_game_value(cur_succ)
            if cur_score == max_score:
                max_successors.append(cur_succ)
            elif cur_score > max_score:
                max_score = cur_score
                max_successors.clear()
                max_successors.append(cur_succ)
        max = float("-inf")
        next_state = None
        count_my = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    count_my += 1
        count_my += 1
        for succ in succs:
            if_adj = self.check_distance(succ, count_my)
            if not if_adj:
                continue
            score = self.Min_value(succ, 0)
            if score > max:
                max = score
                next_state = succ
        # self.print_spe_board(next_state)
        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ' and next_state[i][j] == self.my_piece:
                    (row, col) = (i, j)
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move

    def check_distance(self, state, num):
        count = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    if i-1 >= 0 and j-1 >= 0 and state[i-1][j-1] != ' ':
                        count += 1
                        continue
                    if i-1 >= 0 and state[i-1][j] != ' ':
                        count += 1
                        continue
                    if i-1 >= 0 and j+1 <= 4 and state[i-1][j+1] != ' ':
                        count += 1
                        continue
                    if j-1 >= 0 and state[i][j-1] != ' ':
                        count += 1
                        continue
                    if j+1 <= 4 and state[i][j+1] != ' ':
                        count += 1
                        continue
                    if i+1 <= 4 and j-1 >= 0 and state[i+1][j-1] != ' ':
                        count += 1
                        continue
                    if i+1 <= 4 and state[i+1][j] != ' ':
                        count += 1
                        continue
                    if i+1 <= 4 and j+1 <= 4 and state[i+1][j+1] != ' ':
                        count += 1
                        continue
        if count == num:
            return True
        else:
            return False

    def succ(self, state, piece):
        successor = []
        count_r = 0
        count_b = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == 'r':
                    count_r += 1
                if state[i][j] == 'b':
                    count_b += 1
        if count_b + count_r < 8:  # dropping phrase
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        tmp_state = copy.deepcopy(state)
                        tmp_state[i][j] = piece
                        successor.append(tmp_state)
        else:  # after dropping phrase
            my_cord = []
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:
                        my_cord.append([i, j])
            # my_cord now has 4 elements
            for cord in my_cord:
                if cord[0] - 1 >= 0 and state[cord[0] - 1][cord[1]] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] - 1][cord[1]] = piece
                    successor.append(tmp_state)
                if cord[0] + 1 <= 4 and state[cord[0] + 1][cord[1]] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] + 1][cord[1]] = piece
                    successor.append(tmp_state)
                if cord[1] - 1 >= 0 and state[cord[0]][cord[1] - 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0]][cord[1] - 1] = piece
                    successor.append(tmp_state)
                if cord[1] + 1 <= 4 and state[cord[0]][cord[1] + 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0]][cord[1] + 1] = piece
                    successor.append(tmp_state)
                if cord[0] - 1 >= 0 and cord[1] - 1 >= 0 and state[cord[0] - 1][cord[1] - 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] - 1][cord[1] - 1] = piece
                    successor.append(tmp_state)
                if cord[0] - 1 >= 0 and cord[1] + 1 <= 4 and state[cord[0] - 1][cord[1] + 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] - 1][cord[1] + 1] = piece
                    successor.append(tmp_state)
                if cord[0] + 1 <= 4 and cord[1] - 1 >= 0 and state[cord[0] + 1][cord[1] - 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] + 1][cord[1] - 1] = piece
                    successor.append(tmp_state)
                if cord[0] + 1 <= 4 and cord[1] + 1 <= 4 and state[cord[0] + 1][cord[1] + 1] == ' ':
                    tmp_state = copy.deepcopy(state)
                    tmp_state[cord[0]][cord[1]] = ' '
                    tmp_state[cord[0] + 1][cord[1] + 1] = piece
                    successor.append(tmp_state)
        return successor

    def check_move(self, state, i, j):
        if i - 1 >= 0 and self.board[i - 1][j] == ' ':
            return [i - 1, j]
        if i + 1 <= 4 and self.board[i + 1][j] == ' ':
            return [i + 1, j]
        if j - 1 >= 0 and self.board[i][j - 1] == ' ':
            return [i, j - 1]
        if j + 1 <= 4 and self.board[i][j + 1] == ' ':
            return [i, j + 1]
        return None

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def print_spe_board(self, state):
        """ Formatted printing for the board """
        for row in range(len(state)):
            line = str(row) + ": "
            for cell in state[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def heuristic_game_value(self, state):
        score = self.game_value(state)
        if score == 1:
            return 1
        if score == -1:
            return -1
        #  score is 0 and the game is terminated
        #  do heuristic on the current state
        score = -0.5
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    if j + 1 <= 4 and state[i][j + 1] == self.my_piece:
                        if j + 2 <= 4 and state[i][j + 2] == self.my_piece:  # ... /....
                            if j + 3 <= 4 and state[i][j + 3] == self.my_piece:
                                if score < 1:
                                    score = 1
                            else:
                                if j + 3 <= 4 and state[i][j + 3] != ' ':
                                    if score < 0.4:
                                        score = 0.4
                                else:
                                    if score < 0.5:
                                        score = 0.5
                        elif i + 1 <= 4 and state[i + 1][j] == self.my_piece:  # :'
                            if state[i + 1][j + 1] != ' ':
                                if score < 0.4:
                                    score = 0.4
                            else:
                                if score < 0.5:
                                    score = 0.5
                        elif i + 1 <= 4 and state[i + 1][j + 1] == self.my_piece:  # ':
                            if state[i + 1][j] != ' ':
                                if score < 0.4:
                                    score = 0.4
                            else:
                                if score < 0.5:
                                    score = 0.5
                        else:  # ..
                            if score < 0:
                                score = 0
                    elif i + 1 <= 4 and state[i + 1][j] == self.my_piece:
                        if i + 2 <= 4 and state[i + 2][j] == self.my_piece:
                            if i + 3 <= 4 and state[i + 3][j] == self.my_piece:  # |
                                if score < 1:
                                    score = 1
                            else:
                                if i + 3 <= 4 and state[i + 3][j] != ' ':
                                    if score < 0.4:
                                        score = 0.4
                                else:
                                    if score < 0.5:
                                        score = 0.5
                        elif j + 1 <= 4 and state[i + 1][j + 1] == self.my_piece:
                            if state[i][j+1] != ' ':
                                if score < 0.4:
                                    score = 0.4
                            else:
                                if score < 0.5:
                                    score = 0.5  # :.
                        else:
                            if score < 0:
                                score = 0
                    elif i + 1 <= 4 and j - 1 >= 0 and state[i + 1][j - 1] == self.my_piece:
                        if i + 2 <= 4 and j - 2 >= 0 and state[i + 2][j - 2] == self.my_piece:
                            if i + 3 <= 4 and j - 3 >= 0 and state[i + 3][j - 3] == self.my_piece:
                                if score < 1:
                                    score = 1
                            else:
                                if i + 3 <= 4 and j - 3 >= 0 and state[i + 3][j - 3] != ' ':
                                    if score < 0.4:
                                        score = 0.4
                                else:
                                    if score < 0.5:
                                        score = 0.5
                        else:
                            if score < 0:
                                score = 0
                    elif i + 1 <= 4 and j + 1 <= 4 and state[i + 1][j + 1] == self.my_piece:
                        if i + 2 <= 4 and j + 2 <= 4 and state[i + 2][j + 2] == self.my_piece:
                            if i + 3 <= 4 and j + 3 <= 4 and state[i + 3][j + 3] == self.my_piece:
                                if score < 1:
                                    score = 1
                            else:
                                if i + 3 <= 4 and j + 3 <= 4 and state[i + 3][j + 3] != ' ':
                                    if score < 0.4:
                                        score = 0.4
                                elif i + 3 > 4 or j + 3 > 4:
                                    if score < 0.4:
                                        score = 0.4
                                else:
                                    if score < 0.5:
                                        score = 0.5
                        else:
                            if score < 0:
                                score = 0
        if self.my_piece == self.pieces[0]:
            opo_piece = self.pieces[1]
        else:
            opo_piece = self.pieces[0]
        count_opo = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == opo_piece:
                    count_opo += 1

        if count_opo == 3 or count_opo == 4:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == opo_piece:
                        if j-1 >= 0 and j + 3 <= 4 and state[i][j+1] == state[i][j+2] == opo_piece and (state[i][j+3] == ' ' or state[i][j-1] == ' '):
                            return -0.6
                        if i == 1 and state[i+1][j] == state[i+2][j] == opo_piece and (state[i+3][j] == ' ' or state[i-1][j] == ' '):
                            return -0.6
                        if i == 1 and j == 1 and state[i+1][j+1] == state[i+2][j+2] == opo_piece and (state[i+3][j+3] == ' ' or state[i-1][j-1] == ' '):
                            return -0.6
                        if i == 1 and j == 3 and state[i+1][j-1] == state[i+2][j-2] == opo_piece and (state[i+3][j-3] == ' ' or state[i-1][j+1] == ' '):
                            return -0.6
                        if i+1 <= 4 and j+1 <= 4:
                            if state[i][j+1] == state[i+1][j] == opo_piece and state[i+1][j+1] == ' ':
                                return -0.6
                            if state[i][j+1] == state[i+1][j+1] == opo_piece and state[i+1][j] == ' ':
                                return -0.6
                            if state[i+1][j] == state[i+1][j+1] == opo_piece and state[i][j+1] == ' ':
                                return -0.6
                        if i+1 <=4 and j-1 >= 0 and state[i+1][j] == state[i+1][j-1] == opo_piece and state[i][j-1] == ' ':
                            return -0.6
        return score

    def Max_Value(self, state, depth):
        score = self.game_value(state)
        if score == 1:
            return 1
        if score == -1:
            return -1
        if depth == 2:
            return self.heuristic_game_value(state)
        successors = self.succ(state, self.my_piece)
        a = float("-inf")
        for succ in successors:
            cur_score = self.Min_value(succ, depth + 1)
            # print("cur_score is " + str(cur_score))
            a = max(a, cur_score)
        return a

    def Min_value(self, state, depth):
        score = self.game_value(state)
        if score == 1:
            return 1
        if score == -1:
            return -1
        if depth == 2:
            return self.heuristic_game_value(state)
        if self.my_piece == self.pieces[0]:
            oppo_piece = self.pieces[1]
        else:
            oppo_piece = self.pieces[0]
        successors = self.succ(state, oppo_piece)
        b = float("inf")
        for succ in successors:
            cur_score = self.Max_Value(succ, depth + 1)
            b = min(b, cur_score)
        return b

    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2] == state[3][3]:
            return 1 if state[0][0] == self.my_piece else -1
        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3] == state[4][4]:
            return 1 if state[1][1] == self.my_piece else -1
        if state[1][0] != ' ' and state[1][0] == state[2][1] == state[3][2] == state[4][3]:
            return 1 if state[1][0] == self.my_piece else -1
        if state[0][1] != ' ' and state[0][1] == state[1][2] == state[2][3] == state[3][4]:
            return 1 if state[0][1] == self.my_piece else -1
        # check / diagonal wins
        if state[0][4] != ' ' and state[0][4] == state[1][3] == state[2][2] == state[3][1]:
            return 1 if state[0][4] == self.my_piece else -1
        if state[1][3] != ' ' and state[1][3] == state[2][2] == state[3][1] == state[4][0]:
            return 1 if state[1][3] == self.my_piece else -1
        if state[0][3] != ' ' and state[0][3] == state[1][2] == state[2][1] == state[3][0]:
            return 1 if state[0][3] == self.my_piece else -1
        if state[1][4] != ' ' and state[1][4] == state[2][3] == state[3][2] == state[4][1]:
            return 1 if state[1][4] == self.my_piece else -1
        # check 2x2 box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == state[i + 1][j + 1] == state[i][j + 1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
        print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                  (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")


# if state[row][col] != ' ' and state[row+1][col] == ' ' and state[row+1][col-1] == state[row + 1][col+1] == state[row + 2][col] == state[row][col]: