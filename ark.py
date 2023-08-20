import pygame
pygame.init()


back = (0,0,140)#колір фону (background)
mw = pygame.display.set_mode((500,500))#Вікно програми (main window)
mw.fill(back)
clock = pygame.time.Clock()


#змінні, що відповідають за координати платформи
racket_x =200
racket_y =330


#прапор закінчення гри
game_over = False
#клас із попереднього проекту
class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color


    def color(self, new_color):
        self.fill_color = new_color


    def fill(self):
        pygame.draw.rect(mw,self.fill_color,self.rect)

        def outline(self, frame_color, thickness): #обведення існуючого прямокутника
            pygame.draw.rect(mw, frame_color, self.rect, thickness)
    
        def collidepoint(self, x, y):
            return self.rect.collidepoint(x, y)  
        def colliderect(self, rect):
            return self.rect.colliderect(rect) 
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width =10, height =10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)
 
    def draw(self):
        mw.blit(self.image, (self.rect.x,self.rect.y))
class Lable(Area):
    def set_text(self, text, fsize=12, text_color=(0,0,0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text,True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))



ball = Picture('bbb.png', 160, 200, 50, 50)
platform = Picture('platform.png',200, 330, 100, 30)
fire = Picture('fire2.png',0,200,500,500)

#Створення ворогів
start_x =5 #координати створення першого монстра
start_y =5
count =9 #кількість монстрів у верхньому ряду
monsters = []#список для зберігання об'єктів-монстрів

for j in range(3):#цикл по стовпцях
    y = start_y + (55* j)#координата монстра у кожному слід. стовпці буде зміщена на 55 пікселів по y
    x = start_x + (27.5* j)#і 27.5 по x
    for i in range(count):#цикл по рядах(рядків) створює в рядку кількість монстрів,що дорівнює count
        d = Picture('ld.png', x, y,50,50)#створюємо монстра
        monsters.append(d)#додаємо до списку
        x = x +55 #збільшуємо координату наступного монстра
    count = count -1 #для наступного ряду зменшуємо кількість монстрів

game_over = False

move_right =False
move_left =False
dx = 3
dy = 3

while not game_over:
    ball.fill()
    platform.fill()
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            game_over =True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type== pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right =False
            if event.key == pygame.K_LEFT:
                move_left =False
    if move_right == True:
        platform.rect.x +=6
    if move_left == True:
        platform.rect.x -=6

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *=-1
    if ball.rect.x < 0 or ball.rect.x > 450:
        dx *=-1
    if ball.rect.colliderect(platform.rect):
        dy *= -1



    ball.fill()
    platform.fill()
    if len(monsters) == 0:
        time_text = Lable(150,150,50,50, back)
        time_text.set_text('ти виграв',60, (255,0,0))
        time_text.draw(10,10)
        game_over =True
    if ball.rect.y > (racket_y +20):
        time_text = Lable(150,150,50,50, back)
        time_text.set_text('YOU LOSE',60, (255,0,0))
        time_text.draw(10,10)
        game_over =True
    #малюємо всіх монстрів зі списку
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1

    platform.draw()
    ball.draw()
    fire.draw()

    pygame.display.update()

    clock.tick(40)