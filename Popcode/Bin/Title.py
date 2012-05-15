from math import pi
from xml.dom.minidom import parse
from bpy import ops as o
from bpy import context as ctx
from bpy import data
import os

workspace = os.getenv('POPCODE_WORKSPACE')

def getText ( nodes ):
    out = []
    for node in nodes:
        if node.TEXT_NODE == node.nodeType:
            out.append(node.data)
    return ''.join(out)

dom   = parse(workspace + 'Description.xml')
title = getText(dom.getElementsByTagName('title')[0].childNodes)

ctx.scene.objects.active = ctx.scene.objects.get('Text')
o.object.editmode_toggle()
o.font.delete()
o.font.text_insert(text=title)
o.object.editmode_toggle()
o.object.origin_set(type = 'GEOMETRY_ORIGIN', center = 'BOUNDS')

render                            = ctx.scene.render
render.filepath                   = workspace + 'Title.avi'
render.use_antialiasing           = True
render.antialiasing_samples       = '8'
render.fps                        = 24
render.image_settings.file_format = 'H264'
render.ffmpeg.codec               = 'H264'
render.ffmpeg.format              = 'H264'
render.pixel_filter_type          = 'CATMULLROM'
render.resolution_x               = 1280
render.resolution_y               = 720
render.resolution_percentage      = 100
o.render.render(animation = True)

# Only to render one image (skip render.*).
#data.images['Render Result'].save_render('/tmp/Title.jpg')
