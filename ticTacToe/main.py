import pygame as pg
import sys
from gameAlgorithm import solver

pg.init()
pg.font.init()

gameConstants = {
    "fps" : 60,
    "width" : 600,
    "height" : 600,
    "positions" : [(0, 0)]
}

colours = {
    "black" : (0, 0, 0),
    "white" : (255, 255, 255),
    "green" : (168, 234, 184)
}

screen = pg.display.set_mode((gameConstants["width"], gameConstants["height"]))
pg.display.set_caption("Tic Tac Toe")
clock = pg.time.Clock()

class Place():
    def __init__(self, x, y, width, height, location):
        self.rect = pg.Rect(x, y, width, height)
        self.position = (x + 20, y + 20)
        self.location = location

rects = [Place(0, 0, 200, 200, [0, 0]), Place(200, 0, 200, 200, [0, 1]), Place(400, 0, 200, 200, [0, 2]),
        Place(0, 200, 200, 200, [1, 0]), Place(200, 200, 200, 200, [1, 1]), Place(400, 200, 200, 200, [1, 2]),
        Place(0, 400, 200, 200, [2, 0]), Place(200, 400, 200, 200, [2, 1]), Place(400, 400, 200, 200, [2, 2])]

def writeText(text, size, position, colour):
    font = pg.font.Font(pg.font.match_font("chalkboard"), size)
    surface = font.render(text, True, colour)
    screen.blit(surface, position)

def isEven(num):
    if num % 2:
        return "O"
    else:
        return "X"

def drawBackground(colour):
    pg.draw.rect(screen, colour, (gameConstants["width"] / 3, 0, 20, gameConstants["height"]))
    pg.draw.rect(screen, colour, (gameConstants["width"] * (2 / 3), 0, 20, gameConstants["height"]))
    pg.draw.rect(screen, colour, (0, gameConstants["height"] / 3, gameConstants["width"], 20))
    pg.draw.rect(screen, colour, (0, gameConstants["height"] * (2/3), gameConstants["width"], 20))

def move(turn, position, pieces):
    if turn % 2:
        pieces.append({
            "text" : "X",
            "position" : position,
            "colour" : colours["black"]
        })
    else:
        pieces.append({
            "text" : "O",
            "position" : position,
            "colour" : colours["black"]
        })

def winCheck(board, writeText, screen, main):
    isE = False
    for i in board:
        for j in i:
            if j == "E":
                isE = True

    if not isE and solver(board) == -1:
        pg.draw.rect(screen, colours["white"], (0, 0, gameConstants["width"], gameConstants["height"]))
        pg.draw.rect(screen, colours["green"], ((gameConstants["width"] / 2) - (200 / 2), (gameConstants["height"] / 2) + 100, 200, 100), 3)
        writeText("Tie!", 150, (50, 200), colours["black"])
        writeText("Replay", 40, ((gameConstants["width"] / 2) - 50, (gameConstants["height"] / 2) + 130), colours["black"])

        button = pg.Rect(((gameConstants["width"] / 2) - (200 / 2), (gameConstants["height"] / 2) + 100, 200, 100))
        
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(pg.mouse.get_pos()):
                        main()

    elif solver(board) != -1:
        pg.draw.rect(screen, colours["white"], (0, 0, gameConstants["width"], gameConstants["height"]))
        pg.draw.rect(screen, colours["green"], ((gameConstants["width"] / 2) - (200 / 2), (gameConstants["height"] / 2) + 100, 200, 100), 3)
        writeText(str(solver(board)), 150, (50, 200), colours["black"])
        writeText("Replay", 40, ((gameConstants["width"] / 2) - 50, (gameConstants["height"] / 2) + 130), colours["black"])

        button = pg.Rect(((gameConstants["width"] / 2) - (200 / 2), (gameConstants["height"] / 2) + 100, 200, 100))
        
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(pg.mouse.get_pos()):
                        main()

def main():
    turn = 1
    board = [
        ["E", "E", "E"],
        ["E", "E", "E"],
        ["E", "E", "E"]
    ]
    pieces = []

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in rects:
                        if i.rect.collidepoint(pg.mouse.get_pos()):
                            if board[i.location[0]][i.location[1]] == "E":
                                print("collision")
                                move(turn, i.position, pieces)
                                print(turn)
                                turn += 1
                                board[i.location[0]][i.location[1]] = isEven(turn)

        clock.tick(gameConstants["fps"])
        screen.fill(colours["white"])
        drawBackground(colours["black"])
        for piece in pieces:
            writeText(piece["text"], 150, piece["position"], piece["colour"])
        winCheck(board, writeText, screen, main)
        pg.display.flip()


main()

pg.quit()