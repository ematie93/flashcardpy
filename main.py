
import pygame, sys, random, os, yaml
from pygame.locals import *

TITLE = "The CerPYfitication Game"
BASE_GREY =     (180, 180, 180)
DARK_AZURE =    ( 23,  28,  50)
BLACK =         (  0,   0,   0)
WHITE=          (255, 255, 255)
CORRECT_GREEN = ( 62,  99,  28)
WORONG_RED =    ( 48,   8,   8)

MAIN_FONT_COLOR = DARK_AZURE

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_assets = os.path.join(dir_path, "assets")
QUESTION_YAML = "exaple.yml"

mainClock = pygame.time.Clock()


pygame.init()

fontVeradana = pygame.font.SysFont("Verdana", 15)
buttons = pygame.sprite.Group()

class button(pygame.sprite.Sprite):
    def __init__(self, text, position, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.button_surfce = pygame.Surface(size)
        self.color = DARK_AZURE
        self.button_surfce.fill(self.color)
        self.text = text
        draw_text_fit_to_rect(self.button_surfce, self.text,(5, 5), fontVeradana, WHITE)
        self.image = self.button_surfce
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.correct = False
        self.wrong = False
    
    def update(self):
        if self.correct == True:
            self.color = CORRECT_GREEN

        if self.wrong == True:
            self.color = WORONG_RED

        self.button_surfce.fill (self.color)
        draw_text_fit_to_rect(self.button_surfce, self.text,(5, 5), fontVeradana, WHITE)


pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((500, 700), 0, 32, 0)

font = pygame.font.SysFont(None, 20)

main_title_png_path =           os.path.join(dir_assets, "Main_Title.png")
flash_card_button_png_path =    os.path.join(dir_assets, "Flash_Card_mode_BT.png")
exam_simulation_png_path =      os.path.join(dir_assets, "Exam_simulation_BT.png")
bonus_png_path =                os.path.join(dir_assets, "BONUS_BT.png")
credit_png_path =               os.path.join(dir_assets, "Credits.png")
return_png_path =               os.path.join(dir_assets, "Return_BT.png")
show_answer_path =              os.path.join(dir_assets, "Show_Answer.png")
next_path =                     os.path.join(dir_assets, "Next.png")

main_title_png =            pygame.image.load(main_title_png_path)
flash_card_button_png =     pygame.image.load(flash_card_button_png_path)
exam_simulation_png =       pygame.image.load(exam_simulation_png_path)
bonus_png =                 pygame.image.load(bonus_png_path)
credit_png =                pygame.image.load(credit_png_path)
return_png =                pygame.image.load(return_png_path)
show_answer_png =           pygame.image.load(show_answer_path)
next_png =                  pygame.image.load(next_path)

def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

def draw_text_fit_to_rect(surface, text, pos, font, color):
    #Function copied from StackOverFlow provided by the user: Ted Klein Bergman
    #https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    words = [word.split(" ") for word in text.splitlines()]
    space = font.size(" ")[0]
    max_width, max_height = surface.get_size()
    x, y = pos

    for line in words:
        for word in line:
            words_surface = font.render(word, 0, color)
            word_width, word_height = words_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(words_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def yaml_question_loader(yamlfile):
    with open(yamlfile, "r", encoding="utf8") as file:
        questionFile = yaml.safe_load(file)

    return questionFile      

nutanixQuestionsFile = os.path.basename(QUESTION_YAML)
nutanixQuestionList = yaml_question_loader(nutanixQuestionsFile)
random.shuffle(nutanixQuestionList)


def main_menu():
    click = False

    while True:

        maxWidth, maxHeight = screen.get_size()

        screen.fill(BASE_GREY)
        xpos_main_title_png = maxWidth // 2 - main_title_png.get_rect().width // 2
        screen.blit(main_title_png, (xpos_main_title_png, 50))
                
        mx, my = pygame.mouse.get_pos()

        flash_card_button_png_rect = flash_card_button_png.get_rect(topleft = (150, 200))
        exam_simulation_png_rect = exam_simulation_png.get_rect(topleft = (150, 325))
        bonus_png_rect = bonus_png.get_rect(topleft = (150, 450))
        credit_png_rect = credit_png.get_rect(topleft =(150, 500))

        if flash_card_button_png_rect.collidepoint((mx, my)):
            if click:
                flashCardMode(0)
        
        if exam_simulation_png_rect.collidepoint((mx, my)):
            if click:
                examSimulationMode()
        
        if bonus_png_rect.collidepoint((mx, my)):
            if click:
                bonus()
        
        if credit_png_rect.collidepoint((mx, my)):
            if click:
                exit_credits()
                pygame.quit()
                sys.exit()

        screen.blit(flash_card_button_png, (maxWidth // 2 - flash_card_button_png_rect.width // 2, 200))
        screen.blit(exam_simulation_png, (maxWidth // 2 - exam_simulation_png_rect.width // 2, 325))
        screen.blit(bonus_png, ((maxWidth // 2 - bonus_png_rect.width // 2, 450)))
        screen.blit(credit_png,((maxWidth // 2 - credit_png_rect.width // 2, 575)))

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(30)

def flashCardMode(num, correct=False, wrong=False):

    questionNumber = len(nutanixQuestionList)
    questionDict = nutanixQuestionList[num]
    question = questionDict["Question"]
    questionText = question["QuestionText"]
    questionOptions = question["Options"]
    questionCorrects = question["Correct"]
    questionID = question["ID"]

    buttons.empty()
    click = False
    running = True
    maxWidth, maxHeight = screen.get_size()

    return_png_scale = pygame.transform.scale(return_png, (100, 50))
    return_png_rect = return_png_scale.get_rect(topleft = (25, 625))

    show_answer_png_scale = pygame.transform.scale(show_answer_png, (100, 50))
    show_answer_rect = show_answer_png_scale.get_rect(topleft = (200, 625))

    next_png_scale = pygame.transform.scale(next_png, (100, 50))
    next_png_rect = next_png_scale.get_rect(topleft = (375, 625))

    questionIndicator = questionNumber

    random.shuffle(questionOptions)
    for idx, answer in enumerate(questionOptions):
            answerButt = button(answer, (maxWidth // 2, ((maxHeight // 2 - 50) + (idx * 75))), (maxWidth - 100, 50))
            buttons.add(answerButt)

    while running:
        screen.fill(BASE_GREY)
        pos = pygame.mouse.get_pos()
        show = False
                 
        question_area_width, question_area_height = 400, 200
        question_area = pygame.Surface((question_area_width, question_area_height))
        question_area.fill(WHITE)
        draw_text_fit_to_rect(question_area, questionText, (20, 20), fontVeradana, DARK_AZURE)
        screen.blit(question_area, (50, 50))

        draw_text('Flash Card Mode',fontVeradana, DARK_AZURE, screen, 20, 20)
        indicatorText = str(questionIndicator) + "/" + str(num + 1)
        draw_text(indicatorText, fontVeradana,DARK_AZURE, screen, 410, 20)

        buttons.update()
        buttons.draw(screen)

        screen.blit(return_png_scale, (25, 625))
        screen.blit(show_answer_png_scale, (200, 625))
        screen.blit(next_png_scale, (375, 625))

        if return_png_rect.collidepoint((pos)):
            if click:
                main_menu()
        if show_answer_rect.collidepoint((pos)):
            if click:
                show = True
        if next_png_rect.collidepoint((pos)):
            if click:
                new_idx = num + 1
                if wrong:
                    pass
                flashCardMode(new_idx)            

        for checkbutton in buttons:
            if show:
                if checkbutton.text in  questionCorrects:
                    checkbutton.correct = True
            if checkbutton.rect.collidepoint(pos):
                if click:
                    if checkbutton.text in questionCorrects:
                        checkbutton.correct = True
                        if not wrong:
                            if not correct:
                                correct = True
                    else:                      
                        checkbutton.wrong = True
                        if not correct:
                            if not wrong:
                                wrong = True
  
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        mainClock.tick(30)

def examSimulationMode():
    running = True
    while running:
        screen.fill(BASE_GREY)
        
        draw_text('Exam Simulation Mode', fontVeradana, (255, 255, 255), screen, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)

def bonus():
    running = True
    while running:
        screen.fill(BASE_GREY)
        
        draw_text('Bonus', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)

def exit_credits():
    running = True
    exit_and_credits = ['Created by: Maciej Tomasz Gross', 'LinkedIn: https://www.linkedin.com/in/maciej-tomasz-gross/', 'Special Thanks to: ', 'Rafa Laguna: https://www.twitch.tv/rafalagoon/', "Tech With Tim: https://www.youtube.com/c/TechWithTim"]
    while running:
        screen.fill(BASE_GREY)
        
        for idx, textRow in enumerate(exit_and_credits):
            xpos = 50
            yStartpos = 100
            yincrement = 25
            draw_text(textRow,font,(255, 255, 255), screen, xpos, yStartpos + (yincrement * idx))

        draw_text('Credits', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)

main_menu()