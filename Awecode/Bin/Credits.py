from math import pi
from xml.dom.minidom import parse
from bpy import ops as o
from bpy import context as ctx
from bpy import data
import os

workspace = os.getenv('AWECODE_WORKSPACE')

def getText ( nodes ):
    out = []
    for node in nodes:
        if node.TEXT_NODE == node.nodeType:
            out.append(node.data)
    return ''.join(out)

dom     = parse(workspace + 'Description.xml')
credits = dom.getElementsByTagName('credits')[0]
credit  = 'Authors\n'

for author in credits.getElementsByTagName('author'):
    credit += getText(author.childNodes) + '\n'

credit += '\nSoftware\n' + getText(
              credits.getElementsByTagName('software')[0].childNodes
          ) + '\n\n' + getText(
              credits.getElementsByTagName('copyright')[0].childNodes
          )

o.object.text_add()
o.object.editmode_toggle()
o.font.delete()
o.font.text_insert(text=credit)
o.object.editmode_toggle()

text                       = ctx.scene.objects.active
text.data.extrude          = 0.05
text.data.bevel_depth      = 0.02
text.data.bevel_resolution = 2
text.data.align            = 'CENTER'
text.rotation_euler        = (pi / 2, 0.0, 0.0)
text.location              = (0, 0, 0)
o.object.origin_set(type = 'GEOMETRY_ORIGIN', center = 'BOUNDS')
text.data.materials.append(data.materials['MAT'])

render                            = ctx.scene.render
render.filepath                   = workspace + 'Credits.avi'
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
