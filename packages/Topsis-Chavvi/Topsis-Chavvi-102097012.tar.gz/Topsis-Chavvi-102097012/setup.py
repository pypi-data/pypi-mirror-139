from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Topsis-Chavvi',
  version='102097012',
  description='A TOPSIS calculator',
  long_description=open('README.txt').read(),
  url='',  
  author='Chavvi Bhatia',
  author_email='chavvibhatia23@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  install_requires=[''] 
)
