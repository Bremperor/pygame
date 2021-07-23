# Go nuts!
import pygame
from random import randrange

pygame.init()

def render_image(window, img_path, point):
    img = pygame.image.load(img_path)
    window.blit(img, (point.x, point.y))

def render_text(window, text, point):

    font = pygame.font.SysFont("arial", 20)
    text = font.render(text, True, (0, 0, 0))

    text_rect = text.get_rect()
    text_rect.center = (point.x, point.y)

    window.blit(text, text_rect)

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Button():

    def __init__(self, len, wid, position, color):
        self.len = len
        self.wid = wid
        self.position = position
        self.rect = pygame.Rect(position.x, position.y, len, wid)
        self.color = color

    def render(self, window):
        # (window, color, (tlx, tly, len, wid))
        pygame.draw.rect(window, self.color, self.rect)

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Write code in the main event loop if the button.on_click(event) is true
                return True

class Text_Box():

    def __init__(self, tl_point):
        # Positioning
        self.tl_point = tl_point
        self.input_rect = pygame.Rect(self.tl_point.x, self.tl_point.y, 140, 32)
        # Render colors
        self.surface = pygame.Surface((140, 32))
        self.surface.set_alpha(0)
        self.surface.fill((255,255,255))
        self.color_active = pygame.Color('darkgray')
        self.color_passive = pygame.Color('lightgray')
        self.color = self.color_passive
        self.active = False
        # Render text
        self.user_text = ""
        self.base_font = pygame.font.Font(None, 32)

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active and event.key == pygame.K_BACKSPACE:
                # Get text input from 0 to -1 i.e. end
                self.user_text = self.user_text[:-1]
            else:
                if self.active == True:
                    self.user_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            elif not self.input_rect.collidepoint(event.pos):
                self.active = False
                self.color = self.color_passive

    def render(self, window):
        # pygame.draw.rect(window, self.color, self.input_rect)
        window.blit(self.surface, (self.input_rect.left, self.input_rect.top))
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def get_current_text(self):
        return self.user_text

    def update_position(self, n_point):
        self.tl_point = n_point
        self.input_rect = pygame.Rect(self.tl_point.x, self.tl_point.y, 140, 32)

class Sticky_Note():

    def __init__(self):
        self.point = Point(randrange(500), randrange(300))
        self.rect = pygame.Rect(self.point.x, self.point.y, 200, 200)
        self.text_box_point = Point(self.point.x + 20, self.point.y + 20)
        self.text_box = Text_Box(self.text_box_point)
        self.color = self.get_rand_color()
        self.drag = False
        self.offset_x = 0
        self.offset_y = 0

    def render(self, window, user):
        # pygame.draw.rect(window, user.theme, self.rect)
        pygame.draw.rect(window, self.color, self.rect)
        self.text_box.render(window)
        # Generate a signature
        render_text(window, user.username, Point(self.text_box_point.x + 30, self.text_box_point.y + 150))

    def check_event(self, event):
        self.text_box.check_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # User is dragging the current sticky note
                self.drag = True
                # Move the sticky note relative to how much the user's cursor is offset from the sticky note
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            # User stopped dragging, stop everything
            self.drag = False
            self.offset_x = 0
            self.offset_y = 0
        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                # Move sticky note, text box, and signature relative to the user's cursor
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
                self.point.x = mouse_x + self.offset_x
                self.point.y = mouse_y + self.offset_y
                self.text_box_point = Point(self.point.x + 20, self.point.y + 20)
                self.text_box.update_position(self.text_box_point)

    def get_rand_color(self):
        return (randrange(256), randrange(256), randrange(256))

class User():

    def __init__(self, username, theme):
        self.username = username
        self.notes = []
        self.theme = theme
    
    def add_note(self, new_note):
        self.notes.append(new_note)

# Set up display and timer (timer is needed for the textbox)
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

user = User("ricozhu", (66, 135, 245))
new_note_button = Button(100, 50, Point(650, 500), (3, 252, 11))
new_note_button1 = Button(100, 50, Point(250, 500), (3, 57, 252))
new_note_button2 = Button(100, 50, Point(450, 500), (252, 3, 3))
new_note_button3 = Button(100, 50, Point(250, 75), (245, 252, 23))
j=0
i=0
run = True
while run:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        # Writes to the textbox is neccesary
        for sticky_note in user.notes:
            sticky_note.check_event(event)
        
        
        if new_note_button1.on_click(event) == True:
            j=j-1
        if new_note_button2.on_click(event) == True:
            j=j+1
        k=str(j)
        if new_note_button.on_click(event) == True:
            if i==0:
                k="don't show"
                i=1
            elif i==1:
                i=0

    # Render text box and sample button (delete this if you want to)
    for sticky_note in user.notes:
        sticky_note.render(window, user)

    new_note_button.render(window)
    render_text(window, "Green", Point(700, 525))
    new_note_button1.render(window)
    render_text(window, "Blue", Point(300, 525))
    new_note_button2.render(window)
    render_text(window, "Red", Point(500, 525))
    new_note_button3.render(window)
    render_text(window, k, Point(300, 100))
    # Update the screen display
    pygame.display.flip()
    # Update frames; necessary for the textbox to work
    clock.tick(60)

pygame.quit()