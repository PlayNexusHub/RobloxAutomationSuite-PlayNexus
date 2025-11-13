# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\natha\\OneDrive\\Desktop\\Programs\\Roblox Automation Suite\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('config', 'config'), ('modules', 'modules'), ('core', 'core'), ('gui', 'gui')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RobloxAutomationSuite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
