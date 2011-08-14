
from distutils.core import setup
import py2exe


setup(
  windows=['diggr.pyw', 'diggr-replayer.pyw'],
  data_files=[('.', ['terminal10x16_gs_ro.png', 'SDL.dll',
                     'libtcod-gui-mingw.dll', 'libtcod-mingw.dll',
                     'GUIDE.txt'])],
  zipfile=None,
  options={"py2exe": {"includes": ['libtcodpy'], "optimize": 2, "bundle_files":2 } }
)