#5mport pygame
import random
import NeuralNetwork
import tensorflow as tf
import math


class Game():
    def __init__(self, nn = 0, display = True, params = {}, maxMove = 500000, scoring = {"death": 0, "eat": 0, "goodMove": 0, "badMove": 0}):
        """
        This function inits the game and its parameters.
        """
        self.bot_params = params

        if display and nn == 0:
            self.d = Drawing(0)
        elif display:
            self.d = Drawing(1)

        self.s = Snake()
        self.SetApple()
        self.board = [[]]
        self.nn = nn
        self.display = display
        self.maxMove = maxMove
        self.scoring = scoring
        self.points = 0

        return

    def SetApple(self):
        """
        This function sets a new apple location.
        """

        self.apple = (random.randint(0, 24), random.randint(0, 24))

        while self.apple in self.s.body:
            self.apple = (random.randint(0, 24), random.randint(0, 24))

    def RunGame(self):
        """
        This function runs the game in a loop and calls the move and draw functions.
        """

        self.score = 0
        self.UpdateBoard()
        alive = True
        move = 0
        prevDistance = self.distance2()

        while alive and move < self.maxMove:
            move += 1

            self.UpdateBoard()

            currentDistance = self.distance2()

            if currentDistance > prevDistance:
                self.score += self.scoring.get('badMove')
            elif prevDistance >= currentDistance:
                self.score += self.scoring.get('goodMove')

            prevDistance = currentDistance

            if self.display:
                self.d.DrawBoard(self.board, self.bot_params)

            if self.nn == 0:
                pygame.time.delay(200)
                if not self.s.MovePlayer():
                     break
            else:
                if self.display:
                    pygame.time.delay(200)
                if not self.s.move_ai(self.getParameters(), self.nn, self.display, self.bot_params):
                    break

            alive = self.CheckMove()


        if not alive:
            self.score += self.scoring.get('death')

        IsUserExit = alive and (move != self.maxMove)

        return self.score , IsUserExit, self.points



    def UpdateBoard(self):
        """
        This function sets the snakes nodes and apple on the board.
        """
        self.board = [[0] * 25 for _ in range(25)]
        self.board[self.apple[1]][self.apple[0]] = 2
        for t in self.s.body:
            self.board[t[1]][t[0]] = 1

    def CheckMove(self):
        """
        This function checks if the last move has killed the snake or ate an apple.
        :return: whether the last move was valid.
        """

        if self.apple != self.s.body[0]:
            del self.s.body[-1]
        else:
            self.SetApple()
            self.score += self.scoring.get('eat')
            self.points += 1

        if self.s.body[0][0] < 0 or self.s.body[0][0] > 24 or self.s.body[0][1] < 0 or self.s.body[0][1] > 24 or (self.board[self.s.body[0][1]][self.s.body[0][0]] == 1 and self.s.body[0] != self.s.body[-1]):
            return False

        return True

    def distance(self, x, y):
        """
        This function calculates the distance between the snakes head and an obstacle in a given direction.
        :param x: x axis modifier.
        :param y: y axis modifier.
        :return: the calculated distance.
        """

        counter = 1
        while self.s.body[0][0] + counter * x >= 0 and self.s.body[0][0] + counter * x <= 24 and self.s.body[0][1] + counter * y >= 0 and self.s.body[0][1] + counter * y <= 24 and self.board[self.s.body[0][1] + counter * y][self.s.body[0][0] + counter * x] != 1:
            counter += 1

        return counter

    def getParameters(self):
        """
        This function calculates the parameters for the neural network.
        """

        data = []
        data.append(float(self.distance(-1, 0)))
        data.append(float(self.distance(-1, -1)))
        data.append(float(self.distance(0, -1)))
        data.append(float(self.distance(1, -1)))
        data.append(float(self.distance(1, 0)))
        data.append(float(self.distance(1, 1)))
        data.append(float(self.distance(0, 1)))
        data.append(float(self.distance(-1, 1)))

        if self.s.direction >= 1:
            data.append(data.pop(0))
            data.append(data.pop(0))
        if self.s.direction >= 2:
            data.append(data.pop(0))
            data.append(data.pop(0))
        if self.s.direction >= 3:
            data.append(data.pop(0))
            data.append(data.pop(0))

        if self.s.direction == 0:
            data.append(float(self.s.body[0][0] - self.apple[0]))
            data.append(float(self.s.body[0][1] - self.apple[1]))
        elif self.s.direction == 1:
            data.append(float(self.s.body[0][1] - self.apple[1]))
            data.append(float(self.apple[0] - self.s.body[0][0]))
        elif self.s.direction == 2:
            data.append(float(self.apple[0] - self.s.body[0][0]))
            data.append(float(self.apple[1] - self.s.body[0][1]))
        elif self.s.direction == 3:
            data.append(float(self.apple[1] - self.s.body[0][1]))
            data.append(float(self.s.body[0][0] - self.apple[0]))

        return [data]

    def distance2(self):
        return math.sqrt(math.pow(self.apple[0] -  self.s.body[0][0], 2) + math.pow(self.apple[1] -  self.s.body[0][1], 2))



class Drawing():
    def __init__(self, mode = 0):
        """
        This function inits the games screen.
        :param sizeTemp: number of positions on the length and width of the screen.
        """

        pygame.init()
        pygame.font.init()
        self.size = 25
        self.cube = 20
        self.mode = mode

        if mode == 0:
            self.screen = pygame.display.set_mode([self.size * self.cube + self.size - 1, self.size * self.cube + self.size - 1])
        elif mode == 1:
            self.screen = pygame.display.set_mode([self.size * self.cube + self.size - 1 + 350, self.size * self.cube + self.size - 1])

        pygame.display.set_caption('Snake Eye Game')

    def DrawBoard(self, board, bot_params):
        """
        This function prints the board to the screen.
        :param board: array the represents the location of the snakes nodes and the apple.
        """

        self.screen.fill([0, 0, 0])

        for y in range(self.size):
            for x in range(self.size):
                if board[y][x] == 1:
                    pygame.draw.rect(self.screen, [255, 255, 255], [(y * self.cube) + y, (x * self.cube) + x, self.cube, self.cube], 0)
                if board[y][x] == 2:
                    pygame.draw.rect(self.screen, [255, 0, 0], [(y * self.cube) + y, (x * self.cube) + x, self.cube, self.cube], 0)

        if self.mode == 1:
            pygame.draw.rect(self.screen, [255, 255, 255], [525, 0,  10, 524], 0)
            myfont = pygame.font.SysFont('comicsansms', 30)
            myfont2 = pygame.font.SysFont('comicsansms', 18)

            textsurface = myfont.render('Mutate Chance: ' + str(bot_params.get('mutate_chance')), False, (255,255,255))
            self.screen.blit(textsurface, (560, 20))
            textsurface = myfont2.render('Y: +    H: -', False, (255,255,255))
            self.screen.blit(textsurface, (560, 55))

            textsurface = myfont.render('Mutate Rate: ' + str(bot_params.get('mutate_rate')), False, (255,255,255))
            self.screen.blit(textsurface, (560, 90))
            textsurface = myfont2.render('U: +    J: -', False, (255,255,255))
            self.screen.blit(textsurface, (560, 125))

            textsurface = myfont.render('Retain Chance: ' + str(bot_params.get('retain')), False, (255,255,255))
            self.screen.blit(textsurface, (560, 160))
            textsurface = myfont2.render('I: +    K: -', False, (255,255,255))
            self.screen.blit(textsurface, (560, 195))

            textsurface = myfont.render('Random Chance: ' + str(bot_params.get('random_select')), False, (255,255,255))
            self.screen.blit(textsurface, (560, 230))
            textsurface = myfont2.render('O: +    L: -', False, (255,255,255))
            self.screen.blit(textsurface, (560, 265))

        pygame.display.flip()

class Snake():

    def __init__(self):
        """
        This function inits the snakes location and direction.
        """
        self.body = [(12, 12)]
        self.direction = random.randint(0, 3)

    def MovePlayer(self):
        """
        This function moves the snakes position by the players input.
        :return: whether the user chose to close the game.
        """

        turned = False
        for event in pygame.event.get():
            if event == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != 2 and not turned:
                    self.direction = 0
                    turned = True
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != 0 and not turned:
                    self.direction = 2
                    turned = True
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != 1 and not turned:
                    self.direction = 3
                    turned = True
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != 3 and not turned:
                    self.direction = 1
                    turned = True
                elif event.key == pygame.K_ESCAPE:
                    return False

        if self.direction == 0:
            self.body.insert(0, (self.body[0][0] - 1, self.body[0][1]))
        if self.direction == 1:
            self.body.insert(0, (self.body[0][0], self.body[0][1] - 1))
        if self.direction == 2:
            self.body.insert(0, (self.body[0][0] + 1, self.body[0][1]))
        if self.direction == 3:
            self.body.insert(0, (self.body[0][0], self.body[0][1] + 1))


        return True

    def move_ai(self, data, nn, display, bot_params):
        self.direction += (nn.get_move(data) - 1)
        self.direction %= 4

        if display:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_y:
                        if bot_params['mutate_chance'] != 1:
                            bot_params['mutate_chance'] = round(bot_params.pop('mutate_chance') + 0.1, 1)
                    elif event.key == pygame.K_h:
                        if bot_params['mutate_chance'] != 0:
                            bot_params['mutate_chance'] = round(bot_params.pop('mutate_chance') - 0.1, 1)
                    elif event.key == pygame.K_u:
                        if bot_params['mutate_rate'] != 1:
                            bot_params['mutate_rate'] = round(bot_params.pop('mutate_rate') + 0.1, 1)
                    elif event.key == pygame.K_j:
                        if bot_params['mutate_rate'] != 0.1:
                            bot_params['mutate_rate'] = round(bot_params.pop('mutate_rate') - 0.1, 1)
                    elif event.key == pygame.K_i:
                        if bot_params['retain'] != 1:
                            bot_params['retain'] = round(bot_params.pop('retain') + 0.1, 1)
                    elif event.key == pygame.K_k:
                        if bot_params['retain'] != 0.1:
                            bot_params['retain'] = round(bot_params.pop('retain') - 0.1, 1)
                    elif event.key == pygame.K_o:
                        if bot_params['random_select'] != 0.5:
                            bot_params['random_select'] = round(bot_params.pop('random_select') + 0.1, 1)
                    elif event.key == pygame.K_l:
                        if bot_params['random_select'] != 0:
                            bot_params['random_select'] = round(bot_params.pop('random_select') - 0.1, 1)

        if self.direction == 0:
            self.body.insert(0, (self.body[0][0] - 1, self.body[0][1]))
        if self.direction == 1:
            self.body.insert(0, (self.body[0][0], self.body[0][1] - 1))
        if self.direction == 2:
            self.body.insert(0, (self.body[0][0] + 1, self.body[0][1]))
        if self.direction == 3:
            self.body.insert(0, (self.body[0][0], self.body[0][1] + 1))

        return True