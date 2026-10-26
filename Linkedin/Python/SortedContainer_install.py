import pip;
import sys, subprocess;
pip.main(['install', 'sortedcontainers'])

# subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', 'sortedcontainers'])
subprocess.run([sys.executable, '-m', 'pip', 'install', 'sortedcontainers'])
