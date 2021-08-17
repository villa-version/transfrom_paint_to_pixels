import pygame, sys

CELL_SIZE = 25
CELL_NUMBER = 25


class Object:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen


class Grid(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        for i in range(2):
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5 * i,
                              CELL_SIZE - 5 * i)
            pygame.draw.rect(self.screen, (111 * (i + 1), 213, 222), obj)


class Paint(Object):
    def __init__(self, x, y, screen, mass_colors):
        Object.__init__(self, x, y, screen)
        self.mass_colors = mass_colors

    def draw(self):
        pygame.draw.circle(self.screen, (self.mass_colors[0], self.mass_colors[1], self.mass_colors[2]), (self.x, self.y), CELL_SIZE / 4)


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.draw_line = []
        self.paint_state = False
        self.last_m_pos_x = None
        self.last_m_pos_y = None
        self.color_state = ''
        self.colors = [0, 0, 0]

    def update(self):
        self.draw_elem()
        self.to_paint()
        self.check_color()

    def draw_elem(self):
        for block in self.grid:
            block.draw()
        for blob in self.draw_line:
            blob.draw()
        #print(len(self.draw_line))

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for y in r:
            for x in r:
                self.grid.append(Grid(x, y, self.screen))

    def check_color(self):
        if self.color_state == 'RED':
            self.colors = [255, 0, 0]
        elif self.color_state == 'GREEN':
            self.colors = [0, 255, 0]
        elif self.color_state == 'BLUE':
            self.colors = [0, 0, 255]

    def to_paint(self):
        if self.paint_state:
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] != self.last_m_pos_x and m_pos[1] != self.last_m_pos_y:
                self.last_m_pos_x, self.last_m_pos_y = m_pos[0], m_pos[1]
                self.draw_line.append(Paint(m_pos[0], m_pos[1], self.screen, self.colors))

    def remove_paint(self):
        self.draw_line = self.draw_line[:-1]

    def remove_unnecessary_blobs(self):
        i = 0
        j = 0
        while i < len(self.draw_line):
            j = i+1
            while j < len(self.draw_line):
                if self.draw_line[i].x == self.draw_line[j].x and self.draw_line[i].y == self.draw_line[j].y:
                    del self.draw_line[j]
                else:
                    j += 1
            i += 1

    def transform_paint_to_pixel(self):
        if not self.paint_state:
            for block in self.grid:
                for blob in self.draw_line:
                    bx = block.x * CELL_SIZE
                    by = block.y * CELL_SIZE
                    if bx <= blob.x <= bx + CELL_SIZE and by <= blob.y <= by + CELL_SIZE:
                        blob.x = bx + CELL_SIZE / 2
                        blob.y = by + CELL_SIZE / 2


def main():
    name = "Paint"
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
    pygame.display.set_caption(name)

    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_controller.paint_state = not main_controller.paint_state
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_controller.transform_paint_to_pixel()
                    main_controller.remove_unnecessary_blobs()
                elif event.key == pygame.K_z:
                    main_controller.remove_paint()
                elif event.key == pygame.K_1:
                    main_controller.color_state = 'RED'
                elif event.key == pygame.K_2:
                    main_controller.color_state = 'GREEN'
                elif event.key == pygame.K_3:
                    main_controller.color_state = 'BLUE'

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()


if __name__ == '__main__':
    main()
