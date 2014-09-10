# -*- mode: python -*-
a = Analysis(['picup.py'],
             pathex=['c:\\Users\\pydep\\python\\picup'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=['pyinstaller_hook/pyqt4_runtime_hook.py'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='picup.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='picup')
