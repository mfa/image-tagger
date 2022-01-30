import click
import pygame

from utils import load_tags


class ImageTagger:
    def __init__(self, tagset_filename):
        self._running = True
        self._active = True

        self.tagset = load_tags(tagset_filename)
        self.tagset_state = {i: False for i in self.tagset}
        self.images = ["G0035540.JPG", "G0036927.JPG", "G0036930.JPG"]
        self.image_index = 0

        # remember key downs for toggles
        self.keys_down = [False] * (len(self.tagset) + 1)

        # list of keys (1..9) for tags
        self.tagkeys = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
        ]
        # limit to the used ones
        self.tagkeys = self.tagkeys[: len(self.tagset)]

        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("image tagger")

        self.screen = pygame.display.set_mode((1900, 800), pygame.RESIZABLE)
        self.max_x, self.max_y = pygame.display.get_window_size()

        self.font = pygame.font.SysFont("Helvetica", 25)

        self.show_image()
        self.show_tagset()

    def show_tagset(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (1, 10, 200, 200))
        for index, (tag, state) in enumerate(self.tagset_state.items()):
            s = f"{index+1} | {tag}: {state}"
            _tag = self.font.render(s, True, (255, 255, 255))
            self.screen.blit(_tag, (10, 10 + (30 * index)))
        pygame.display.update()

    def show_image(self):
        x, y = 1333, 1000
        image_name = self.images[self.image_index]
        image = pygame.transform.scale(pygame.image.load(image_name), (x, y))
        self.screen.blit(image, (self.max_x - x - 10, 10))
        pygame.display.flip()

    def tag_key_pressed(self, key):
        self.keys_down[key] = True
        self.tagset_state[self.tagset[key - 1]] = not self.tagset_state[
            self.tagset[key - 1]
        ]
        self.show_tagset()

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
            if event.key == pygame.K_LEFT:
                self.image_index -= 1
                if self.image_index < 0:
                    self.image_index = len(self.images) - 1
                self.show_image()

            for index, key in enumerate(self.tagkeys, start=1):
                if event.key == key and not self.keys_down[index]:
                    self.tag_key_pressed(index)

        if event.type == pygame.KEYUP:
            for index, key in enumerate(self.tagkeys, start=1):
                if event.key == key and self.keys_down[index]:
                    self.keys_down[index] = False

    def on_loop(self):
        # redraw frame when window gets active again after loosing focus
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
            # limit to 30 fps -- limit CPU usage
            self.clock.tick(30)
        self.on_cleanup()


@click.command()
@click.option("--tagset", type=click.Path(exists=True))
def main(tagset):
    app = ImageTagger(tagset_filename=tagset)
    app.on_execute()


if __name__ == "__main__":
    main()
