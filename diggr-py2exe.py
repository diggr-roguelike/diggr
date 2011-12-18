
from distutils.core import setup
import py2exe


setup(
  windows=[
        { "script": 'diggr.pyw', "icon_resources": [(1, "Rock-Collecting.ico")]},
        'diggr-replayer.pyw'],
  data_files=[('.', ['font.png', 'terminal10x16_gs_ro.png', 'SDL.dll',
                     'libtcod-mingw.dll',
                     'GUIDE.txt'])],
  zipfile=None,
  options={"py2exe": {"includes": ['libtcodpy'], 
                      "optimize": 2, 
                      "bundle_files":2 } }
)
