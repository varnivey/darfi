from distutils.core import setup
import py2exe, sys, os

import skimage
import PyQt4

sys.argv.append('py2exe')
sys.path.append(os.path.join('..','engine'))

rootdir = os.path.dirname(os.getcwd())
script = os.path.join(rootdir, 'simple_gui', 'simple_gui.py')
icon = os.path.join(rootdir, 'misc', 'darfi.ico')

#Mydata_files = [('images', ['D:\Users\Vanya\Python_win32\Ksenia\gui\smile_icon_2.jpg'])]

qt_if_dlls_path = os.path.join(os.path.dirname(PyQt4.__file__), u'plugins', u'imageformats')
qt_if_dlls = [os.path.join(qt_if_dlls_path, dll) for dll in os.listdir(qt_if_dlls_path)]

orb_descriptor = os.path.join(skimage.data_dir, 'orb_descriptor_positions.txt')

setup(
#    options = {'py2exe': {'bundle_files': 1}},
#    windows=[{'script':script, "icon_resources":[(1, icon)]}],
    windows=[{'script':script}],
#    data_files = Mydata_files,
    data_files = [
            ('imageformats', \
              qt_if_dlls
              ),\
              (os.path.join('skimage', 'data'), [\
              orb_descriptor,
              ]),\
              ('misc', [icon,])
              ],
    options={"py2exe":{"includes":[\
            "sip",\
#            "pic_an",\
            "scipy.special._ufuncs_cxx",\
            "skimage.filter.rank.core_cy",\
            "scipy.sparse.csgraph._validation",\
            "skimage._shared.geometry",\
            "skimage",\
            "PIL.TiffImagePlugin"
            ]}},
#    console = [{'script': script}],
    zipfile = None,
)

raw_input()
