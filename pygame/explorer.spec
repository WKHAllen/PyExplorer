# -*- mode: python -*-

block_cipher = None


a = Analysis(['explorer.py'],
             pathex=['C:\\Users\\Will\\Desktop\\Programming\\Python\\Programs\\PyExplorer\\pygame'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PyExplorer',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
