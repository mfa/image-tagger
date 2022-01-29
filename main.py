import pygame


class ImageTagger:
    def __init__(self):
        self._running = True
        self._active = True

        self.tagset = ("blured", "forest", "fields", "houses", "humans")
        self.tagset_state = {i: False for i in self.tagset}
        self.images = ["G0035540.JPG", "G0036927.JPG", "G0036930.JPG"]
        self.image_index = 0

        # remember key downs for toggles
        self.keys_down = [False] * (len(self.tagset) + 1)

        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("image tagger")

        self.screen = pygame.display.set_mode((1900, 800), pygame.RESIZABLE)
        self.max_x, self.max_y = pygame.display.get_window_size()

        self.font = pygame.font.SysFont("Helvetica", 20)

        self.show_image()
        self.show_tagset()

    def show_tagset(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (1, 10, 200, 200))
        for index, (tag, state) in enumerate(self.tagset_state.items()):
            s = f"{index+1} | {tag}: {state}"
            _tag = self.font.render(s, True, (255, 255, 255))
            self.screen.blit(_tag, (10, 10 + (25 * index)))
        pygame.display.update()

    def show_image(self):
        x, y = 1333, 1000
        image_name = self.images[self.image_index]
        image = pygame.transform.scale(pygame.image.load(image_name), (x, y))
        self.screen.blit(image, (self.max_x - x - 10, 10))
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self._running = False
            if event.key == pygame.K_n or event.key == pygame.K_RIGHT:
                self.image_index += 1
                if self.image_index == len(self.images):
                    self.image_index = 0
                self.show_image()

            if event.key == pygame.K_1 and not self.keys_down[1]:
                self.keys_down[1] = True
                self.tagset_state[self.tagset[0]] = not self.tagset_state[
                    self.tagset[0]
                ]
                self.show_tagset()
            if event.key == pygame.K_2 and not self.keys_down[2]:
                self.keys_down[2] = True
                self.tagset_state[self.tagset[1]] = not self.tagset_state[
                    self.tagset[1]
                ]
                self.show_tagset()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1 and self.keys_down[1]:
                self.keys_down[1] = False
            if event.key == pygame.K_2 and self.keys_down[2]:
                self.keys_down[2] = False

    def on_loop(self):
        if pygame.display.get_active() != self._active:
            self._active = pygame.display.get_active()
            if pygame.display.get_active():
                pygame.display.update()

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = ImageTagger()
    theApp.on_execute()
