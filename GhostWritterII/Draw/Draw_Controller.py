from Draw.Cv2_Draw import Open_CV as Ocv
from Draw.Pygame_Draw import PyGame as Pg


def draw_on_window(d_type):
    if d_type == 1:
        return Pg
    else:
        return Ocv
