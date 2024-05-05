import constants as con
import os, sys
import random

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def talk_dialog(screen, text, font, width_offset, height_offset, line_length=32, color=(0,0,0)):
    text_list = []
    if type(text) == type("bla"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        for line in text:
            temp = separate_text_into_lines(line, line_length)
            text_list += temp
    else:
        s = "That type of data shouldn't be here!"
        raise ValueError(s)
    text_height = top_height(text_list, font)
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))

if __name__ == "__main__":
    filepath = os.path.join("data", "quizes")
    get_directories()