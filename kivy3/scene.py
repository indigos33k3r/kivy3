
"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from kivy.uix.widget import Widget
from kivy.graphics.fbo import Fbo
from kivy.resources import resource_find

from .camera import Camera


class Renderer(Fbo):
    
    def __init__(self, *args, **kw):
        kw.setdefault('with_depthbuffer', True)
        kw.setdefault('compute_normal_mat', True)
        

class Scene(Widget):
    """ Core class which allows you to use 3D graphics in
    Kivy application.
    
    Parameters:
        camera_cls: Camera by default, but you may use your own class
        clear_color: to make transparent background set value to (0., 0., 0., 0.)
        shader_file: path to your shader file
    """
    
    def __init__(self, camera_cls=Camera, renderer_cls=Renderer, **kw):
        
        self.objects = []
        
        # get clear color 
        self.clear_color = kw.pop('clear_color', (0., 0., 0., 1.))
        self.shader_file = kw.pop('shader_file', resource_find('default.glsl'))
         
        super(Scene, self).__init__(**kw)
        self.camera = camera_cls(self)
        
        # create FBO where all drawing is going
        with self.canvas:
            self.renderer = Renderer(size=self.size, clear_color=self.clear_color)
            self.renderer.shader.source = self.shader_file 
    
    def add(self, *objs):
        """ Add objects to 3D scene """
        for obj in objs:
            self._add_obj(obj)
    
    def _add_obj(self, obj):
        self.objects.append(obj)
    
 