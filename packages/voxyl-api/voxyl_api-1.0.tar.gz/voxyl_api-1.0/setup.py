from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='voxyl_api',
  version='1.0',
  description='An easy wrapper for https://api.voxyl.net/ written in Python',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Davey Adams',
  author_email='davey.adams.three@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='voxyl api', 
  packages=find_packages(),
  install_requires=['requests'] 
)