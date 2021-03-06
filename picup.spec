# -*- mode: python -*-

import picup

block_cipher = None


a = Analysis(['picup.py'],
             pathex=['c:\\Users\\pydep\\python\\picup'],
             hiddenimports=["sip"],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
ui_tree = Tree('picup/ui_files', prefix='ui_files')

name = 'picup_{}.exe'.format(picup.__version__)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          ui_tree,
          name=name,
          debug=False,
          strip=None,
          upx=True,
          console=False )
