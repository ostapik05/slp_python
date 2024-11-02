from labs.lab5.dal.Camera import CameraData

class SceneData:
    def __init__(self):
        self.figures = []
        self.selected_figure = None
        self.is_rotating = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.camera = CameraData()
        self.point_size=30
        self.line_width=10
        self.alpha=0.2
        self.highlight_color=(1, 1, 1)
        self.highlight_line_width=20


