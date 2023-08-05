from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='graph-svg',
  version='0.0.1',
  description='Svg visualisation for graph data structure',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Adem PELIT',
  author_email='apelit55@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='graph', 
  packages=find_packages(),
  install_requires=['IPython'] 
)