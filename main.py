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
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, (111, 111, 222), (self.x, self.y), CELL_SIZE / 4)


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.draw_line = []
        self.paint_state = False
        self.last_m_pos_x = None
        self.last_m_pos_y = None

    def update(self):
        self.draw_elem()
        self.to_paint()

    def draw_elem(self):
        for block in self.grid:
            block.draw()
        for blob in self.draw_line:
            blob.draw()

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for y in r:
            for x in r:
                self.grid.append(Grid(x, y, self.screen))

    def to_paint(self):
        if self.paint_state:
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] != self.last_m_pos_x and m_pos[1] != self.last_m_pos_y:
                self.last_m_pos_x, self.last_m_pos_y = m_pos[0], m_pos[1]
                self.draw_line.append(Paint(m_pos[0], m_pos[1], self.screen))

    def transform_paint_to_pixel(self):
        if not self.paint_state:
            for block in self.grid:
                for blob in self.draw_line:
                    bx = block.x * CELL_SIZE
                    by = block.y * CELL_SIZE
                    if bx < blob.x < bx + CELL_SIZE and by < blob.y < by + CELL_SIZE:
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

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()


if __name__ == '__main__':
    main()
