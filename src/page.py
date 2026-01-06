import pygame
import ui

# Abstract class
class Page(ui.Renderable):
    def __init__(self):
        super().__init__(always_flag_buffer_update=True)
        self._layer_buffers: list[ui.LayerBuffer] = []
        self._construct()

    # Abstract method
    def _construct(self):
        raise NotImplementedError()
    
    def _destroy(self):
        for layer_buffer in self._layer_buffers:
            layer_buffer.destruct()

    def _render_to(self, root: pygame.Surface):
        for layer_buffer in self._layer_buffers:
            layer_buffer.update_buffer_update_flag()
            layer_buffer.render_to(root)