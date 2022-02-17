from os import walk
from csv import reader

import pygame


def csv_layout(path):
    """
    imports a map layout from a file
    """
    map = []
    with open(path) as f:
        layout = reader(f, delimiter=",")
        for row in layout:
            map.append(list(row))
    
    return map



def images_from_folder(path: str):
    """
    imports all images from folder into pygame
    """
    surfaces = []
    for _,__,images in walk(path):
        for image in images:
            surfaces.append(pygame.image.load(f"{path}/{image}").convert_alpha())

    return surfaces
    
    
if __name__ == "__main__":
    m = csv_layout("../../map/map_FloorBlocks.csv")
    
    
    g = images_from_folder("../../images/grass")