import pygame, sys

CELL_SIZE = 25
CELL_NUMBER = 25


class Object:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen


class Grid(Object):
    def __init__(self, x, y, screen, mass_blob):
        Object.__init__(self, x, y, screen)
        self.mass_blob = mass_blob

    def draw(self):
        for i in range(2):
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5 * i,
                              CELL_SIZE - 5 * i)
            pygame.draw.rect(self.screen, (111 * (i + 1), 213, 222), obj)


class Point(Object):
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
        for row in self.grid:
            for block in row:
                block.draw()
        for blob in self.draw_line:
            blob.draw()

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for _ in r:
            self.grid.append([])
        for y in r:
            for x in r:
                self.grid[y].append(Grid(x, y, self.screen, []))

    def check_color(self):
        if self.color_state == 'RED':
            self.colors = [255, 0, 0]
        elif self.color_state == 'GREEN':
            self.colors = [0, 255, 0]
        elif self.color_state == 'BLUE':
            self.colors = [0, 0, 255]

    def to_paint(self):
        if self.paint_state:
            mx, my = pygame.mouse.get_pos()
            if mx != self.last_m_pos_x and my != self.last_m_pos_y:
                block_x = mx//CELL_SIZE
                block_y = my//CELL_SIZE
                bx = block_x * CELL_SIZE
                by = block_y * CELL_SIZE
                if bx <= int(mx) <= bx + CELL_SIZE and by <= int(my) <= by + CELL_SIZE:
                    point = Point(mx, my, self.screen, self.colors)
                    self.draw_line.append(point)
                    self.grid[block_y][block_x].mass_blob.append(point)
                self.last_m_pos_x, self.last_m_pos_y = mx, my

    def remove_paint(self):
        last_point = self.draw_line[-1]
        x = last_point.x//CELL_SIZE
        y = last_point.y//CELL_SIZE
        self.grid[y][x].mass_blob.remove(last_point)
        self.draw_line = self.draw_line[:-1]

    def remove_unnecessary_blobs(self):
        for row in self.grid:
            for block in row:
                for point in block.mass_blob[1:]:
                    self.draw_line.remove(point)
                block.mass_blob = block.mass_blob[0:1]

    def transform_paint_to_pixel(self):
        if not self.paint_state:
            for row in self.grid:
                for block in row:
                    for blob in block.mass_blob:
                        blob.x = block.x * CELL_SIZE + CELL_SIZE // 2
                        blob.y = block.y * CELL_SIZE + CELL_SIZE // 2


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
                    main_controller.remove_unnecessary_blobs()
                    main_controller.transform_paint_to_pixel()
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
