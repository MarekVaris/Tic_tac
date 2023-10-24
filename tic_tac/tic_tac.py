import pygame
import random
import sys

# Game visual
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption('Tic_Tac_Toe')
Icon = pygame.image.load('img/o.png')
pygame.display.set_icon(Icon)
font = pygame.font.SysFont(None, 48)
font_s = pygame.font.SysFont(None, 30)

# Background color
bg_color = (100, 100, 100)

# Game name
gamename = font_s.render("Tic Tac Toe", True, (0, 0, 0))

# Importing img of O and X
o = pygame.image.load('img/o.png')
x = pygame.image.load('img/x.png')

# Resizing img
o_player = pygame.transform.scale(o, (150, 150))
x_player = pygame.transform.scale(x, (150, 150))

# Choosing box on start
chose_box = pygame.Rect(150, 150, 450, 200)

option1 = pygame.Rect(200, 250, 100, 50)
option2 = pygame.Rect(450, 250, 100, 50)

chose_box_text = font.render("Play vs AI or PVP?", True, (0, 0, 0))
option1_text = font_s.render("PVP", True, (0, 0, 0))
option2_text = font_s.render("AI", True, (0, 0, 0))

# Boxes on hover/press
box1 = pygame.Rect(150, 50, 150, 150)
box2 = pygame.Rect(303, 50, 150, 150)
box3 = pygame.Rect(456, 50, 150, 150)
box4 = pygame.Rect(150, 203, 150, 150)
box5 = pygame.Rect(303, 203, 150, 150)
box6 = pygame.Rect(456, 203, 150, 150)
box7 = pygame.Rect(150, 356, 150, 150)
box8 = pygame.Rect(303, 356, 150, 150)
box9 = pygame.Rect(456, 356, 150, 150)

# Game main
turn = 1
player_turn = 1
mouse_enabled = True
mouse_timer = 0

player1 = player2 = 0
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]

# AI Smart
def min_max(board, base_turn):
    current_turn = base_turn
    empty_cells = [index for index, num in enumerate(board) if num == 0]
    best_score = float('-inf')
    best_move = None

    for i in empty_cells:
        board_ai = board[:]
        board_ai[i] = current_turn
        score = min_value(board_ai, 3 - current_turn, current_turn)
        if score > best_score:
            best_score = score
            best_move = i

    return best_move

def min_value(board_ai, current_turn, original_turn):
    if check_win(board_ai, original_turn, current_turn):
        return 1
    elif check_win(board_ai, 3 - original_turn, current_turn):
        return -1
    elif check_draw(board_ai):
        return 0

    best_score = float('inf')

    for i, cell in enumerate(board_ai):
        if cell == 0:
            board_ai[i] = current_turn
            score = max_value(board_ai, 3 - current_turn, original_turn)
            board_ai[i] = 0
            best_score = min(best_score, score)

    return best_score

def max_value(board_ai, current_turn, original_turn):
    if check_win(board_ai, original_turn, current_turn):
        return 1
    elif check_win(board_ai, 3 - original_turn, current_turn):
        return -1
    elif check_draw(board_ai):
        return 0

    best_score = float('-inf')

    for i, cell in enumerate(board_ai):
        if cell == 0:
            board_ai[i] = current_turn
            score = min_value(board_ai, 3 - current_turn, original_turn)
            board_ai[i] = 0
            best_score = max(best_score, score)

    return best_score

def check_win(board_ai, player, current_turn):
    
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for combo in winning_combinations:
        if board_ai[combo[0]] == board_ai[combo[1]] == board_ai[combo[2]] == player:
            return True

    return False

def check_draw(board_ai):
    return all(cell != 0 for cell in board_ai)

# Functions
def place_symbol(symbol_pos, i):
    global player1, player2, turn

    if board[i] == 0 and turn != 0:
        data = str(symbol_pos)
        s_ind = data.find("(") + 1
        in_ind = data.find(",", s_ind)
        e_ind = data.find(",", in_ind + 1)
        xval = int(data[s_ind:in_ind])
        yval = int(data[in_ind + 1:e_ind])
        board[i] = turn
        pygame.draw.rect(screen, (100, 100, 100), symbol_pos)

        if turn == 1:
            screen.blit(o_player, (xval, yval))
            if win():
                if player_turn % 2 == 0:
                    player1 += 1
                else:
                    player2 += 1
                return 0
            return 2
        elif turn == 2:
            screen.blit(x_player, (xval, yval))
            if win():
                if player_turn % 2 == 0:
                    player2 += 1
                else:
                    player1 += 1
                return 0
            return 1
    return turn

def win():
    for i in [0, 3, 6]:
        if board[i] != 0:
            if board[i] == board[i + 1] == board[i + 2]:
                return True

    for i in range(3):
        if board[i] != 0:
            if board[i] == board[i + 3] == board[i + 6]:
                return True

    if board[4] != 0:
        if board[0] == board[4] == board[8]:
            return True
        elif board[2] == board[4] == board[6]:
            return True

    return False

def status():
    info_box = pygame.Rect(200, 150, 350, 200)
    text_info = font.render("Score!", True, (0, 0, 0))
    player_info = font.render("Player1:      Player2:", True, (0, 0, 0))
    score_info = font.render(f"{player1}                   {player2}", True, (0, 0, 0))

    pygame.draw.rect(screen, (125, 0, 0), info_box)

    screen.blit(text_info, (320, 160))
    screen.blit(player_info, (220, 220))
    screen.blit(score_info, (270, 280))

    pygame.display.update()
    pygame.time.delay(3000)

def newround(player_tr):
    screen.fill(bg_color)
    pygame.draw.line(screen, (0, 0, 0), (300, 50), (300, 506), 2)
    pygame.draw.line(screen, (0, 0, 0), (453, 50), (453, 506), 2)
    pygame.draw.line(screen, (0, 0, 0), (150, 200), (606, 200), 2)
    pygame.draw.line(screen, (0, 0, 0), (150, 353), (606, 353), 2)

    if player_turn % 2 == 0:
        player1_symbol = font_s.render("Player1: O", True, (0, 0, 0))
        player2_symbol = font_s.render("Player2: X", True, (0, 0, 0))
    else:
        player1_symbol = font_s.render("Player1: X", True, (0, 0, 0))
        player2_symbol = font_s.render("Player2: O", True, (0, 0, 0))

    screen.blit(player1_symbol, (10, 10))
    screen.blit(player2_symbol, (10, 35))
    screen.blit(gamename, (300, 10))

    for i in range(len(board)):
        board[i] = 0
    pygame.display.update()
    return 1

def start():
    screen.fill(bg_color)
    pygame.draw.rect(screen, (125, 0, 0), chose_box)
    screen.blit(chose_box_text, (230, 170))
    pygame.draw.rect(screen, (255, 0, 0), option1)
    screen.blit(option1_text, (230, 265))
    pygame.draw.rect(screen, (0, 0, 255), option2)
    screen.blit(option2_text, (490, 265))

# Main run
chosen = False
start()
running = True
player_turn = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if chosen == False:
                if option1.collidepoint(event.pos):
                    turn = newround(player_turn)
                    chosen = True
                    pvp = True
                    mouse_enabled = False
                    mouse_timer = pygame.time.get_ticks()
                    pygame.display.update()
                elif option2.collidepoint(event.pos):
                    turn = newround(player_turn)
                    chosen = True
                    pvp = False
                    mouse_enabled = False
                    mouse_timer = pygame.time.get_ticks()
                    pygame.display.update()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not mouse_enabled:
        elapsed_time = pygame.time.get_ticks() - mouse_timer
        if elapsed_time >= 300:
            mouse_enabled = True

    if chosen == True and mouse_enabled:
        if pvp == False:
            if (player_turn % 2 == 0 and turn == 2) or (player_turn % 2 == 1 and turn == 1):
                maxsym = min_max(board, turn)
                pygame.time.delay(200)
                turn = place_symbol(boxes[maxsym], maxsym)
                if turn == 0:
                    turn = 1
                pygame.display.update()

                if win():
                    status()
                    turn = newround(player_turn)
                    player_turn += 1
                    pygame.time.delay(500)

        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(boxes)):
            if boxes[i].collidepoint(mouse_pos):
                if board[i] == 0:
                    pygame.draw.rect(screen, (150, 150, 150), boxes[i])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boxes[i].collidepoint(event.pos):
                        turn = place_symbol(boxes[i], i)
                        board_left = [num for num in board if num == 0]
                        if (turn == 0 and len(board_left) < 8) or len(board_left) == 0:
                            pygame.display.update()
                            status()
                            turn = newround(player_turn)
                            player_turn += 1
                            pygame.time.delay(500)
            elif board[i] == 0:
                pygame.draw.rect(screen, (100, 100, 100), boxes[i])
    pygame.display.update()
    clock.tick(30)

pygame.quit()
