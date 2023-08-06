from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='evaluate_classification',
  version='0.0.01',
  description='finding Factors and basic sum',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='jupiter',
  author_email='npsjupiter@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='HCF/Factor', 
  packages=find_packages(),
  install_requires=[''] 
)