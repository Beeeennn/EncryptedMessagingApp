from email import message
import sys
import threading
from turtle import screensize
import pygame
pygame.init()
import UI as inp
import Utilities as U
from time import sleep
import Login_OOP as login
import client
#dims like 1000 x 1000
class SCREENS():
    def __init__(self,screen,user):
        self.screen = screen
        self.user = user
    def Login_page(self):
        screen = self.screen
        new = True
        pygame.display.set_caption("Login")


        login_img = pygame.image.load("AImages\Blue\login-button.png").convert_alpha()
        login_img_hover = pygame.image.load("AImages\Blue\login-hover.png").convert_alpha()

        exit_img = pygame.image.load("AImages\Blue\exit-button.png").convert_alpha()
        exit_img_hover = pygame.image.load("AImages\Blue\exit-hover.png").convert_alpha()

        create_img = pygame.image.load("AImages\Blue\create-button.png").convert_alpha()
        create_img_hover = pygame.image.load("AImages\Blue\create-hover.png").convert_alpha()

        login_button = inp.Button(500,850, login_img,login_img_hover, 35,screen)
        exit_button = inp.Button(150,875, exit_img,exit_img_hover, 18,screen)
        create_button = inp.Button(850,875, create_img,create_img_hover, 18,screen)

        username_box = inp.Textbox(None,80,"Username",500,550,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,False,screen)
        password_box = inp.Textbox(None,80,"Password",500,660,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,True,screen)
        boxes = [username_box,password_box]

        bottom_text = inp.Flash(50,720,None,50,(255,255,255),screen)
        flashes = [bottom_text]

        logo_img = pygame.image.load("AImages\Blue\logo.png").convert_alpha()
        logo = inp.image(500,230,logo_img,200,0,screen)
        images = [logo]



        run = True
        while run:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    for box in boxes:
                        box.active = False
                for box in boxes:
                    box.handle_event(event)
            for box in boxes:
                box.draw(screen)
            for image in images:
                image.draw(screen)
            for flsh in flashes:
                flsh.draw(screen)

            if login_button.draw(screen):
                if not new:
                    username = username_box.get_text()
                    password = password_box.get_text()
                    userlog = login.User(self.user)
                    enter = userlog.login(username,password)
                    if enter:
                        self.menu()
                        run = False
                    else:
                        bottom_text.show("Wrong username or password",2)
            if create_button.draw(screen):
                if not new:
                    self.Create_account_page()
                    run = False
            if exit_button.draw(screen):
                if not new:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            if pygame.mouse.get_pressed()[0] == 0:
                new = False

    def Create_account_page(self):
        screen = self.screen
        new = True
        pygame.display.set_caption("Create Account")

        back_img = pygame.image.load("AImages\Blue\\back-button.png").convert_alpha()
        back_img_hover = pygame.image.load("AImages\Blue\\back-hover.png").convert_alpha()

        create_img = pygame.image.load("AImages\Blue\create-button.png").convert_alpha()
        create_img_hover = pygame.image.load("AImages\Blue\create-hover.png").convert_alpha()

        back_button = inp.Button(150,875, back_img,back_img_hover, 18,screen)
        create_button = inp.Button(500,850, create_img,create_img_hover, 30,screen)

        username_box = inp.Textbox(None,80,"Username",500,380,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,False,screen)
        email_box = inp.Textbox(None,80,"Email",500,480,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,False,screen)
        password_box = inp.Textbox(None,80,"Password",500,580,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,True,screen)
        password2_box = inp.Textbox(None,80,"Confirm Password",500,680,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,True,screen)
        boxes = [username_box,password_box,email_box,password2_box]

        bottom_text = inp.Flash(50,740,None,50,(255,255,255),screen)
        flashes = [bottom_text]

        logo_img = pygame.image.load("AImages\Blue\logo.png").convert_alpha()
        logo = inp.image(500,175,logo_img,150,0,screen)
        images = [logo]

        run = True
        while run:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    for box in boxes:
                        box.active = False
                for box in boxes:
                    box.handle_event(event)
            for box in boxes:
                box.draw(screen)
            for image in images:
                image.draw(screen)
            for flsh in flashes:
                flsh.draw(screen)
            if back_button.draw(screen):
                if not new:
                    self.Login_page()
                    run = False
            if create_button.draw(screen):
                if not new:
                    username = username_box.get_text()
                    emailadd = email_box.get_text()
                    password = password_box.get_text()
                    password2 = password2_box.get_text()
                    active = login.User(self.user)
                    result = active.create_account(username,password,password2,emailadd)
                    if result[2]:
                        print("created")
                        bottom_text.show("Account Created",10)
                    else:
                        error = U.casechecker(result[0],result[1])
                        bottom_text.show(error,2)
            pygame.display.update()
            if pygame.mouse.get_pressed()[0] == 0:
                new = False

    def messaging(self,reciever):

        screen = self.screen
        user = self.user


        textbx = inp.ScrollingTextbox(None,50,"message",425,775,800,150,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,False,(0,0,0),screen)
        boxes = [textbx]

        bottom_text = inp.Flash(50,740,None,50,(255,255,255),screen)

        send_img = pygame.image.load("AImages\Blue\send-button.png").convert_alpha()
        send_img_hover = pygame.image.load("AImages\Blue\send-hover.png").convert_alpha()
        send_button = inp.Button(915,810,send_img,send_img_hover,18,screen)

        clear_img = pygame.image.load("AImages\Blue\clear-button.png").convert_alpha()
        clear_img_hover = pygame.image.load("AImages\Blue\clear-hover.png").convert_alpha()
        clear_button = inp.Button(425,925,clear_img,clear_img_hover,18,screen)

        back_img = pygame.image.load("AImages\Blue\\back-button.png").convert_alpha()
        back_img_hover = pygame.image.load("AImages\Blue\\back-hover.png").convert_alpha()
        back_button = inp.Button(100,925, back_img,back_img_hover, 18,screen)

        exit_img = pygame.image.load("AImages\Blue\exit-button.png").convert_alpha()
        exit_img_hover = pygame.image.load("AImages\Blue\exit-hover.png").convert_alpha()
        exit_button = inp.Button(915,100, exit_img,exit_img_hover, 18,screen)

        background = pygame.image.load("AImages\message_back.png").convert_alpha()
        text_display = inp.Messages(None,50,425,350,800,600,background,(0,0,0),(0,0,0),reciever,user,screen)

        reciever_text = inp.Text(750, 890,None,50,(255,255,255),True,screen)

        pygame.display.set_caption(f"Signed in as {user.nickname}")
        new = True
        run = True
        while run:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    text_display.running = False
                    for box in boxes:
                        box.active = False
                    user.stop()
                else:
                    textbx.handle_event(event)
                    text_display.handle_event(event)
            text_display.draw(screen)
            textbx.draw(screen)
            bottom_text.draw(screen)
            reciever_text.draw((f"Message {reciever}"),screen)
            if send_button.draw(screen):
                if not new:
                    text = textbx.get_text(user)
                    allowed = U.validate_message(text)
                    if allowed:
                        textbx.clear_text()
                        send_thread = threading.Thread(target=U.send_message,args =(text,reciever,user))
                        send_thread.daemon = True
                        send_thread.start()
                    else:
                        bottom_text.show("You cant use §•®© in the message",1)
            if clear_button.draw(screen):
                if not new:
                    textbx.clear_text()
            if back_button.draw(screen):
                if not new:
                    text_display.running=False
                    self.menu()
                    run = False
            if exit_button.draw(screen):
                if not new:
                    text_display.running = False
                    user.stop()
            reciever_text.draw((f"Message {reciever}"),screen)
            text_display.draw(screen)
            pygame.display.update()
            if pygame.mouse.get_pressed()[0] == 0:
                new = False

    def menu(self):
        screen = self.screen
        new = True
        pygame.display.set_caption(f"Signed in as {self.user.nickname}")

        search_img = pygame.image.load("AImages\Blue\search-button.png").convert_alpha()
        search_img_hover = pygame.image.load("AImages\Blue\search-hover.png").convert_alpha()
        search_button = inp.Button(500,500, search_img,search_img_hover, 18,screen)

        exit_img = pygame.image.load("AImages\Blue\exit-button.png").convert_alpha()
        exit_img_hover = pygame.image.load("AImages\Blue\exit-hover.png").convert_alpha()

        clear_img = pygame.image.load("AImages\Blue\clear-button.png").convert_alpha()
        clear_img_hover = pygame.image.load("AImages\Blue\clear-hover.png").convert_alpha()
        clear_button = inp.Button(850,500,clear_img,clear_img_hover,18,screen)

        exit_button = inp.Button(150,500, exit_img,exit_img_hover, 18,screen)

        search_box = inp.Textbox(None,80,"Search user to message",500,200,900,80,(255,255,255),(220,220,220),(0,0,0),(150,150,150),10,False,screen)
        boxes = [search_box]

        bottom_text = inp.Flash(50,720,None,50,(255,255,255),screen)
        flashes = [bottom_text]

        logo_img = pygame.image.load("AImages\Blue\logo.png").convert_alpha()
        logo = inp.image(500,230,logo_img,200,0,screen)
        images = [logo]



        run = True
        while run:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    for box in boxes:
                        box.active = False
                for box in boxes:
                    box.handle_event(event)
            for box in boxes:
                box.draw(screen)
            #for image in images:
            #    image.draw(screen)
            for flsh in flashes:
                flsh.draw(screen)

            if search_button.draw(screen):
                if not new:
                    username = search_box.get_text()
                    if U.check_username_exists(username,self.user):
                        self.messaging(username)
                        run = False
                    else:
                        bottom_text.show("Not an existing user",10)
            if clear_button.draw(screen):
                if not new:
                    search_box.clear()
            if exit_button.draw(screen):
                if not new:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            if pygame.mouse.get_pressed()[0] == 0:
                new = False


    def Test(self):
        screen = self.screen
        pygame.display.set_caption("Test")
        run = True
        while run:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
