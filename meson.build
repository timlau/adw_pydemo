project('adwpydemo',  
          version: '0.2.0',
    meson_version: '>= 0.50.0'
)

python = import('python')
project_id = 'dk.rasmil.AdwPyDemo'

message('Looking for dependencies')
py_installation = python.find_installation('python3')
if not py_installation.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif

python_dir = join_paths(get_option('prefix'), py_installation.get_install_dir())
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
bindir = join_paths(get_option('prefix'), get_option('bindir'))

conf = configuration_data()
conf.set('DATA_DIR', DATA_DIR)
conf.set('PYTHON_DIR', python_dir)
conf.set('VERSION', meson.project_version())
conf.set('APPID', project_id)
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))


install_subdir(
  'adwpydemo',
  install_dir: python_dir
)

message('Preparing bin file')
configure_file(
  input: 'adwpydemo.in',
  output: 'adwpydemo',
  configuration: conf,
  install_dir: bindir
)

subdir('data')