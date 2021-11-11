import pygame as pg
import globals

pg.init()
FONT = pg.font.Font(None, 16)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
COLOR_TEXT = pg.Color('white')


class InputBox:

    def __init__(self, x, y, w, h, text_func = None, update_func = None):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text_func = text_func
        self.text = self.text_func()
        self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)
        self.active = False
        self.update_func = update_func

    def set_active(self, rel_pos):
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(rel_pos):
            # Toggle the active variable.
            self.active = True
            self.text = ''
        else:
            self.active = False
            self.text = self.text_func()
                # Change the current color of the input box.
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def handle_event(self, event):
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    if self.text == '':
                        self.text = self.text_func()
                    self.update_func(self.text)
                    self.active = False
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)