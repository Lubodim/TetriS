import sys
import pygame

from config import Config
from shape_factory import TetroFactory, Tetromino


def draw_grid(screen, config: Config, board):
    cols = config.cols
    rows = config.rows
    tile = config.tile_size
    colors = config.colors

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * tile, y * tile, tile, tile)

            pygame.draw.rect(screen, colors["GRAY"], rect)
            pygame.draw.rect(screen, colors["BLACK"], rect, 1)

            cell_color = board[y][x]
            if cell_color is not None:
                inner = rect.inflate(-4, -4)
                pygame.draw.rect(screen, cell_color, inner)


def draw_tetromino(screen, config: Config, tetromino: Tetromino):
    tile = config.tile_size
    colors = config.colors

    for (x, y) in tetromino.get_cells():
        if y < 0:
            continue

        rect = pygame.Rect(x * tile, y * tile, tile, tile)
        pygame.draw.rect(screen, tetromino.color, rect)
        pygame.draw.rect(screen, colors["BLACK"], rect, 1)


def is_valid_position(tetromino: Tetromino, config: Config, board) -> bool:

    for x, y in tetromino.get_cells():
        if x < 0 or x >= config.cols:
            return False
        if y >= config.rows:
            return False

        if y >= 0 and board[y][x] is not None:
            return False
    return True


def lock_piece_to_board(tetromino: Tetromino, board, config: Config):

    for x, y in tetromino.get_cells():
        if 0 <= x < config.cols and 0 <= y < config.rows:
            board[y][x] = tetromino.color


def clear_full_lines(board, config: Config) -> int:

    cols = config.cols
    rows = config.rows

    new_board = []
    cleared = 0

    for y in range(rows - 1, -1, -1):
        if all(board[y][x] is not None for x in range(cols)):
            cleared += 1
        else:
            new_board.append(board[y])

    while len(new_board) < rows:
        new_board.append([None for _ in range(cols)])

    new_board.reverse()

    for y in range(rows):
        board[y] = new_board[y]

    return cleared


def hard_drop(tetromino: Tetromino, config: Config, board):

    while True:
        test_piece = Tetromino(
            tetromino.x,
            tetromino.y,
            list(tetromino.blocks),
            tetromino.color,
        )
        test_piece.move(0, 1)

        if is_valid_position(test_piece, config, board):
            tetromino.move(0, 1)
        else:
            break


def main():
    pygame.init()

    config = Config()
    colors = config.colors

    width = config.cols * config.tile_size + config.sidebar_width
    height = config.rows * config.tile_size

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Lovely TetriS")
    clock = pygame.time.Clock()

    running = True

    board = [[None for _ in range(config.cols)] for _ in range(config.rows)]

    current_piece = TetroFactory.create_random(config.cols)

    fall_interval_ms = 500
    last_fall_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                    if not is_valid_position(current_piece, config, board):
                        current_piece.move(1, 0)  # връщаме

                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                    if not is_valid_position(current_piece, config, board):
                        current_piece.move(-1, 0)  # връщаме

                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
                    if not is_valid_position(current_piece, config, board):
                        current_piece.move(0, -1)  # връщаме

                elif event.key == pygame.K_UP:
                    old_blocks = current_piece.blocks.copy()
                    current_piece.rotate()
                    if not is_valid_position(current_piece, config, board):
                        current_piece.blocks = old_blocks  # връщаме старото завъртане

                elif event.key == pygame.K_SPACE:
                    hard_drop(current_piece, config, board)
                    lock_piece_to_board(current_piece, board, config)
                    clear_full_lines(board, config)
                    current_piece = TetroFactory.create_random(config.cols)

        now = pygame.time.get_ticks()
        if now - last_fall_time >= fall_interval_ms:
            test_piece = Tetromino(
                current_piece.x,
                current_piece.y,
                list(current_piece.blocks),
                current_piece.color,
            )
            test_piece.move(0, 1)

            if is_valid_position(test_piece, config, board):
                current_piece.move(0, 1)
            else:
                lock_piece_to_board(current_piece, board, config)
                clear_full_lines(board, config)
                current_piece = TetroFactory.create_random(config.cols)

            last_fall_time = now

        screen.fill(colors["DARK_GRAY"])
        draw_grid(screen, config, board)
        draw_tetromino(screen, config, current_piece)

        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()
    sys.exit()


main()
