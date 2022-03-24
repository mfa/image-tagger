from pathlib import Path

import click
import pygame

from utils import load_image_tags, load_tagset, save_image_tags


class ImageTagger:
    def __init__(self, tagset_filename, images, data, extension):
        self._running = True
        self._active = True

        self.tagset = load_tagset(tagset_filename)
        self.images = list(Path(images).glob(f"*{extension}"))
        self.image_index = 0
        self.data_folder = Path(data)
        self.image_tags = load_image_tags(self.data_folder) or {}
        self.new_image = False

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

        font = (
            "sourcecodepro"
            if "sourcecodepro" in pygame.font.get_fonts()
            else "Helvetica"
        )
        self.font = pygame.font.SysFont(font, 25)

        self.update()

    def get_tags(self, image_index):
        image_name = self.images[self.image_index]
        _t = self.image_tags.get(image_name.name) or {}
        self.new_image = not bool(_t)
        for i in self.tagset:
            if i not in _t:
                _t[i] = False
        return _t

    def show_tagset(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (1, 1, 400, 300))
        for index, (tag, state) in enumerate(self.tagset_state.items()):
            s = f" {index+1} | {tag}: {state}"
            _tag = self.font.render(s, True, (255, 255, 255))
            self.screen.blit(_tag, (10, 10 + (30 * index)))

        if self.new_image:
            s = self.font.render("new image", True, (255, 255, 255))
            self.screen.blit(s, (10, 10 + (30 * index) + 40))
        pygame.display.update()

    def show_image(self):
        x, y = 1333, 1000
        image_name = self.images[self.image_index]
        image = pygame.transform.scale(pygame.image.load(image_name), (x, y))
        self.screen.blit(image, (self.max_x - x - 10, 10))

        pygame.draw.rect(self.screen, (0, 0, 0), (1, 400, 500, 400))
        _s = f"{image_name.name}: {self.image_index}"
        s = self.font.render(_s, True, (255, 255, 255))
        self.screen.blit(s, (10, 400))

        pygame.display.flip()

    def tag_key_pressed(self, key):
        self.keys_down[key] = True
        self.tagset_state[self.tagset[key - 1]] = not self.tagset_state[
            self.tagset[key - 1]
        ]
        self.show_tagset()

    def show_help(self):
        for index, (key, text) in enumerate(
            [
                ("->", "next image (state is saved)"),
                ("<-", "previous image"),
                (" n", "next NEW image"),
                (" q", "quit"),
            ]
        ):
            s = self.font.render(f"{key} | {text}", True, (255, 255, 255))
            self.screen.blit(s, (10, 510 + (30 * index)))
        pygame.display.update()

    def save(self):
        self.image_tags[self.images[self.image_index].name] = self.tagset_state
        save_image_tags(self.data_folder, self.image_tags)

    def update(self):
        self.show_image()
        self.tagset_state = self.get_tags(self.image_index)
        self.show_tagset()
        self.show_help()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self._running = False
            if event.key == pygame.K_RIGHT:
                self.save()
                self.image_index += 1
                if self.image_index == len(self.images):
                    self.image_index = 0
                self.update()
            if event.key == pygame.K_LEFT:
                self.image_index -= 1
                if self.image_index < 0:
                    self.image_index = len(self.images) - 1
                self.update()
            if event.key == pygame.K_n:
                while True:
                    self.image_index += 1
                    if self.image_index == len(self.images):
                        self.image_index = 0
                        break
                    # use tags to detect new images
                    self.get_tags(self.image_index)
                    if self.new_image:
                        break
                self.update()

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
@click.option("--tagset", type=click.Path(exists=True), help="yaml file with tagset")
@click.option("--images", type=click.Path(exists=True), help="folder with images")
@click.option("--data", type=click.Path(exists=True), help="folder to store saved tags")
@click.option("--extension", help="extension of images", default="JPG")
def main(tagset, images, data, extension):
    app = ImageTagger(
        tagset_filename=tagset, images=images, data=data, extension=extension
    )
    app.on_execute()


if __name__ == "__main__":
    main()
