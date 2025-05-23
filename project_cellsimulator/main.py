import pygame
import sys
import json
import time
from requirements import *
from bioclasses import Cell, ExtracellularSpace, CellContact
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button


def draw_text(surface, color, text, where, font_name="Arial", font_size=16):
    """Нарисовать текст на экране"""
    font = pygame.font.SysFont(font_name, font_size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if isinstance(where, pygame.Rect):
        text_rect.center = where.center
    else:
        text_rect.topleft = where
    surface.blit(text_surf, text_rect)


class Game:
    """Главный класс приложения Ion Transport Simulator"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ion Transport Simulator")
        self.clock = pygame.time.Clock()
        
        btn_x = SCREEN_WIDTH - 200
        self.start_button = Button(self.screen, btn_x, 50, 150, 40,
                                   text='Start', onClick=lambda: self.set_running(True))
        self.pause_button = Button(self.screen, btn_x, 100, 150, 40,
                                   text='Pause', onClick=lambda: self.set_running(False))
        self.reset_button = Button(self.screen, btn_x, 150, 150, 40,
                                   text='Reset', onClick=self.reset_game)
        self.save_button = Button(self.screen, btn_x, 200, 150, 40,
                                  text='Save', onClick=self.save_state)
        self.load_button = Button(self.screen, btn_x, 250, 150, 40,
                                  text='Load', onClick=self.load_state)

        self.running = False
        self.time = 0.0
        self.cells = []             # клетки
        self.spaces = []            # внеклеточные пространства
        self.contacts = []          # контакты транспорта
        self.upd_queue = [[] for _ in range(100)] # очередь пересчёта

    def make_contacts(self):
        """Пересоздать контакты между смежными клетками и пространствами"""
        self.upd_queue.clear()
        for i in range(100):
            self.upd_queue.append([])
        self.contacts.clear()
        for cell in self.cells:
            cell.contacts.clear()

        cell_map = {(c.x, c.y): c for c in self.cells}
        spaces_map = {(c.x, c.y): c for c in self.spaces}
        cell_map = {**cell_map, **spaces_map}

        self.cells[0].delta = 0
        for cell in self.cells:
            neighbours = [(cell.x+1, cell.y), (cell.x-1, cell.y), (cell.x, cell.y+1), (cell.x, cell.y-1)]
            for nx, ny in neighbours:
                if (nx, ny) in cell_map:
                    other = cell_map[(nx, ny)]
                    other.delta = min(cell.delta + 10, 1000)
                    if not any(c.target is other for c in cell.contacts):
                        self.connect(cell, other, cell.delta)



    def set_running(self, running):
        """Запустить или приостановить симуляцию"""
        self.running = running
        self.make_contacts()

    def reset_game(self):
        """Сбросить состояние симуляции"""
        self.running = False
        self.time = 0.0
        self.cells.clear()
        self.spaces.clear()
        self.contacts.clear()
        self.upd_queue = [[] for _ in range(100)]

    def add_cell(self, gx, gy):
        """Добавить клетку на сетку"""
        cell = Cell(gx, gy)
        self.cells.append(cell)

    def add_space(self, gx, gy):
        """Добавить внекл. пространство на сетку"""
        space = ExtracellularSpace(gx, gy)
        self.spaces.append(space)

    def connect(self, source, target, delta):
        """создать контакт"""
        contact = CellContact(source, target, delta)
        self.contacts.append(contact)
        self.upd_queue[0].append(contact)

    def save_state(self, filename='state.json'):
        """Сохранить текущее состояние в файл JSON"""
        data = {
            'time': self.time,
            'cells': [c.to_dict() for c in self.cells],
            'spaces': [s.to_dict() for s in self.spaces]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_state(self, filename='state.json'):
        """Загрузить состояние из файла JSON"""
        with open(filename) as f:
            data = json.load(f)
        self.time = data.get('time', 0.0)
        self.cells.clear()
        for cd in data.get('cells', []):
            cell = Cell(cd['x'], cd['y'])
            cell.K, cell.Na, cell.ATP = cd['K'], cd['Na'], cd['ATP']
            self.cells.append(cell)
        self.spaces.clear()
        for sd in data.get('spaces', []):
            space = ExtracellularSpace(sd['x'], sd['y'])
            space.K, space.Na = sd['K'], sd['Na']
            self.spaces.append(space)

    def handle_events(self, events):
        """Обработка событий pygame"""
        for e in events:
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < SCREEN_WIDTH - 250:
                    gx, gy = mx // CELL_SIZE, my // CELL_SIZE
                    if e.button == 1:
                        self.add_cell(gx, gy)
                    elif e.button == 3:
                        self.add_space(gx, gy)

    def update(self, dt):
        """Обновление симуляции за шаг dt"""
        if not self.running:
            return
        self.time += dt
        queue = self.upd_queue.pop(0)
        self.upd_queue.append([])
        for contact in queue:
            contact.transport(dt)
            self.upd_queue[contact.delta - 1].append(contact)

    def draw(self):
        """Отрисовка всех объектов на экране"""
        self.screen.fill(WHITE)
        for cell in self.cells:
            r = max(min(int(10000 * 255 * (DEFAULT_NA - cell.Na)/DEFAULT_NA), 255), 0)
            b = max(min(int(10000 * 255 * (cell.K - DEFAULT_K)/DEFAULT_K), 255), 0)
            pygame.draw.rect(self.screen, (r, 0, b),
                             (cell.x*CELL_SIZE, cell.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for space in self.spaces:
            r = max(min(int(255 * space.Na / (DEFAULT_NA*1.5)), 255), 0)
            b = max(min(int(255 * space.K / (DEFAULT_K*1.5)), 255), 0)
            pygame.draw.circle(self.screen, (r, 0, b),
                               (space.x*CELL_SIZE + CELL_SIZE//2, space.y*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2)
        self.start_button.draw()
        self.pause_button.draw()
        self.reset_button.draw()
        self.save_button.draw()
        self.load_button.draw()
        draw_text(self.screen, BLACK, f"Time: {self.time:.2f}", (SCREEN_WIDTH - 240, 320))
        pygame.display.flip()

    def run(self):
        """Главный цикл приложения"""
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            self.handle_events(events)
            self.update(dt)
            self.draw()
            pygame_widgets.update(events)


if __name__ == '__main__':
    game = Game()
    game.run()
