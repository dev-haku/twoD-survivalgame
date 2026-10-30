import pygame

def split_sprite_sheet(image_path: str, cut_size: tuple[int,int]) -> list[pygame.Surface]:

    frames = []
    sheet = pygame.image.load(image_path)
    sheet_size = sheet.get_size()
    for y in range(sheet_size[1]//cut_size[1]):
        for x in range(sheet_size[0]//cut_size[0]):
            w, h = cut_size
            crop_area = pygame.Rect(x*w, y*h, w, h)
            cropped_surface = sheet.subsurface(crop_area)
            frames.append(cropped_surface)

    return frames