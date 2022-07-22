import sys
from click import option
from cx_Freeze import setup, Executable

base = sys.platform

executables = [
    Executable('app.py',)
]

include_files = ['data/', 'modulos/']
# packages = ['sqlite3']

setup (
    name = 'App Investimentos',
    version = '1.0.0',
    description = 'App para controle de investimentos',
    options = {'build_exe': {'include_files': include_files}},
    executables = executables
)
