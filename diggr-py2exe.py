
from distutils.core import setup
import py2exe


setup(
  windows=[
        { "script": 'diggr.pyw', "icon_resources": [(1, "Rock-Collecting.ico")]},
        'diggr-replayer.pyw'],
  data_files=[('.', ['font.png', 
                     'libsound.dll', 'libdiggr.dll',
                     'diggr.cfg', 'GUIDE.txt'])],
  zipfile=None,
  options={"py2exe": {"includes": [], 
                      "optimize": 2, 
                      "bundle_files":2 } }
)
