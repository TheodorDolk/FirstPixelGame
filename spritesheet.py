import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale):
        image = self.sheet.subsurface(frame * width, 0, width, height)
        image = pygame.transform.scale_by(image, scale)
        return image
