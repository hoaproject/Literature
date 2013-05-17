from xml.dom.minidom import parse
from bpy import ops as o
from bpy import context as ctx
import os

workspace  = os.getenv('AWECODE_WORKSPACE')
out        = os.getenv('AWECODE_OUT')
#dom        = parse(workspace + 'Description.xml')
#main_strip = dom.getElementsByTagName('source')[0].getAttribute('href')

transition_padding = 20
strips             = dict() # of bpy.types.Sequence

def after ( id ):
    return strips[id].frame_final_end

def add_movie ( id, filepath, frame_start, transition ):

    o.sequencer.movie_strip_add(
        filepath     = filepath,
        filter_movie = True,
        frame_start  = frame_start,
        channel      = len(strips) + 1,
        overlap      = True,
        sound        = True
    )
    strips[id]        = ctx.selected_sequences[0]
    strips[id].select = False

    if False == transition:
        return

    strips[id].frame_start    -= transition_padding
    strips[transition].select  = True
    strips[id].select          = True
    o.sequencer.effect_strip_add(
        filepath    = '',
        frame_start = frame_start - transition_padding,
        frame_end   = frame_start + transition_padding,
        channel     = len(strips) + 1,
        type        = 'CROSS'
    )
    strips[transition].select                        = False
    strips[id].select                                = False
    strips['transition_' + id + '_to_' + transition] = ctx.selected_sequences[0]

    return


# Here we go.
add_movie(
    id          = 'cinematic',
    #filepath    = workspace + 'Title.avi',
    filepath    = '/tmp/compil/Final_720p.mov',
    frame_start = 0,
    transition  = False
)

add_movie(
    id          = 'screencast',
    #filepath    = main_strip,
    filepath    = '/tmp/compil/Screencast.mov',
    frame_start = after('cinematic'),
    #transition  = 'cinematic',
    transition  = False
)

#add_movie(
#    id          = 'credits',
#    filepath    = workspace + 'Credits.avi',
#    frame_start = after('screencast'),
#    transition  = 'screencast'
#)

# Cross fingers.
scene                             = ctx.scene
scene.frame_start                 = 0
#scene.frame_end                   = after('credits')
scene.frame_end                   = after('screencast')
render                            = scene.render
#render.filepath                   = out
render.filepath                   = '/tmp/compil/Out-'
render.use_antialiasing           = True
render.antialiasing_samples       = '16'
render.fps                        = 30

render.image_settings.file_format = 'H264'
render.image_settings.color_mode  = 'RGB'
render.image_settings.compression = 0
render.image_settings.quality     = 100
render.ffmpeg.format              = 'AVI'
#render.ffmpeg.use_lossless_output = True
render.ffmpeg.codec               = 'H264'
render.ffmpeg.gopsize             = 0
render.ffmpeg.video_bitrate       = 8000
render.ffmpeg.audio_channels      = 'STEREO'
render.ffmpeg.audio_codec         = 'MP3'
render.ffmpeg.audio_volume        = 1.0
render.ffmpeg.audio_bitrate       = 320

render.pixel_filter_type          = 'CATMULLROM'
render.resolution_x               = 1280
render.resolution_y               = 720
render.resolution_percentage      = 100
render.threads                    = 4
render.threads_mode               = 'FIXED'
o.render.render(animation = True)


###
# Misc
###

#ctx.scene.sequence_editor.active_strip

# Add an image.
#o.sequencer.image_strip_add(
#    directory   = '/tmp',
#    files       = [{'name': 'Title.jpg'}],
#    frame_start = 0,
#    frame_end   = 48,
#    channel     = 1,
#    overlap     = True
#)
