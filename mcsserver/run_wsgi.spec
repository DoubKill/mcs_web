# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['run_wsgi.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
    'mcs.custom_log',
    'mcs.paginations',
    'mcs.common_code',
    'mcs.derorators',
    'mcs.middlewares',
    'mcs.prod_conf',
    'agv', 'agv.apps', 'agv.urls', 'agv.models',
    'basics', 'basics.apps', 'basics.urls', 'basics.models',
    'basics.management','basics.management.commands','basics.management.tasks','basics.management.utils',
    'basics.management.commands.runapscheduler','basics.management.tasks.collect_wcs_data',
    'basics.management.tasks.mcs_dispatch','basics.management.tasks.send_order',
    'basics.management.tasks.sync_location', 'basics.management.tasks.stock_info',
    'basics.management.tasks.env_check',
    'monitor', 'monitor.apps', 'monitor.urls', 'monitor.models',
    'openapi', 'openapi.apps', 'openapi.models',
    'user', 'user.apps', 'user.urls', 'user.models','user.models.User',
    'user.management','user.management.commands',
    'user.management.commands.db_init','user.management.commands.upgrade_permission',
    'rest_framework', 'rest_framework.apps', 'rest_framework_jwt',
    'rest_framework.authentication', 'rest_framework.parsers', 'rest_framework.permissions',
    'rest_framework.negotiation','rest_framework.metadata', 'rest_framework_jwt.utils',
    'rest_framework_jwt.authentication', 'rest_framework.schemas',
    'coreschema', 'corsheaders','corsheaders.apps',
    'gunicorn.glogging','gunicorn.workers.sync'
    ],
    hookspath=[],
    #hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_wsgi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mcs_web',
)
