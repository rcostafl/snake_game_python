import pdb
import random
# pip install pygame
import pygame
import sys
#from cobrinha import Cobra
#from comida import Comida
import time

class Food:
    def __init__(self, screen):
        self._x_pos = [x * 10 for x in range(int(screen[0]/10))]
        self._y_pos = [x * 10 for x in range(int(screen[1]/10))]
        self.new_food()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def new_food(self):
        self._x = self._x_pos[random.randint(0, len(self._x_pos)-1)]
        self._y = self._y_pos[random.randint(0, len(self._y_pos)-1)]

class Block:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value        

class Snake:
    def __init__(self, block=Block(200,200), block_width=10, block_height=10):
        self._blocks = []
        self._blocks.append(block)
        self._blocks.append(Block(190,200))
        self._blocks.append(Block(180,200))

        self._width  = block_width
        self._heigth = block_height

        self._dropped_tail = None

        self._heading = 'E'

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        self.blocks = value

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        self._heading = value

    def step(self):
        self.blocks.insert(0, Block(self.blocks[0].x, self.blocks[0].y)) #pos, element
        
        if self._heading == 'E':
            self.blocks[0].x += 10
        elif self._heading == 'W':
            self.blocks[0].x -= 10
        elif self._heading == 'N':
            self.blocks[0].y -= 10
        elif self._heading == 'S':
            self.blocks[0].y += 10
        
        self._dropped_tail = self.blocks.pop()

    def head(self):
        return self._blocks[0]

    def eat(self, food):

        if (self.head().x == food.x) and (self.head().y == food.y):
            self.blocks.append(self._dropped_tail)
            return True

        return False

    def is_tangled(self):
        for block in self._blocks[1:]:
            if (self.head().x == block.x) and (self.head().y == block.y):
                return True

        return False

class Main:
    
    def __init__(self):
        self.TAM_TELA    = (400,400)
        self._snake = Snake()
        self._food  = Food(self.TAM_TELA)
        self._game_over = False
        self._game_speed = 4

    def colided(self):

        if self._snake.head().x >= self.TAM_TELA[0]-9:
            return True
        elif self._snake.head().x < 0:
            return True
        elif self._snake.head().y >= self.TAM_TELA[1]-9:
            return True
        elif self._snake.head().y < 0:
            return True
        elif self._snake.is_tangled():
            print(self._snake.is_tangled())
            return True
        return False  
        
    def run(self):
        pygame.font.init()
        minha_fonte = pygame.font.SysFont('Comic Sans MS', 30)

        # inicializar o pygame
        pygame.init()
        
        tela = pygame.display.set_mode(self.TAM_TELA)
        game_time = pygame.time.Clock()

        # inicia o loop do jogo
        while True:

            tela.fill((255,255,255)) # RGB - Red, Green, Blue - (255,255,255)

            for event in pygame.event.get():
                # listener - mouse ou teclado
                if event.type == pygame.QUIT:
                    # interrompe pygame
                    pygame.quit()
                    # fechar script (janela)
                    sys.exit()

                # se uma tecla foi pressionada
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        #inf_display = minha_fonte.render('Direita', True, (66, 117, 184))
                        self._snake.heading = 'E'
                    elif event.key == pygame.K_UP:
                        self._snake.heading = 'N'
                    elif event.key == pygame.K_DOWN:
                        self._snake.heading = 'S'
                    elif event.key == pygame.K_LEFT:
                        self._snake.heading = 'W'
            
            self._snake.step()

            if self._snake.eat(self._food):
                self._food.new_food()
                self._game_speed += 1


            if self.colided():
                inf_display = minha_fonte.render('Perdeu, playboy!!!', True, (66, 117, 184))
                tela.blit(inf_display, (10,10))
                self._game_over = True

            # drawing the snake
            for block in self._snake.blocks:
                pygame.draw.rect(
                    tela, 
                    pygame.Color(66, 117, 184),
                    pygame.Rect(block.x,block.y,10,10)
                )

            #drawing the food
            pygame.draw.rect(
                tela,
                pygame.Color(66, 117, 184),
                pygame.Rect(self._food.x, self._food.y,10,10)
            )

            pygame.display.update()
            
            if self._game_over == True:
                time.sleep(10)
                break

            # FPS - Frames por Segundo
            game_time.tick(self._game_speed)
    

if __name__ == '__main__':
    main = Main()
    main.run()