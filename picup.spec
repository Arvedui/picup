# -*- mode: python -*-
a = Analysis(['picup.py'],
             pathex=['c:\\Users\\pydep\\python\\picup'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=['pyinstaller_hook/pyqt4_runtime_hook.py'])
# small hack for avoiding warning on startup
for d in a.datas:
  if 'include' in d[0]:
    a.datas.remove(d)


pyz = PYZ(a.pure)
ui_tree = Tree('picup/ui_files', prefix='ui_files')
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          ui_tree,
          name='picup.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False)
