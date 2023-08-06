from distutils.core import setup
import setuptools
setup(
  name = 'Topsis-Aryaman-101903495',
  packages = ['Topsis-Aryaman-101903495'],
  version = '0.1',
  license='MIT',
  description = 'This is a package for python where user has to input the csv file and weight and impacts and get the topsis ranking as a csv file output',
  author = 'Aryaman Choudhary',
  author_email = 'aryaman.choudhary01@gmail.com',
  url = 'https://github.com/aryamanchoudhary123/Topsis-Aryaman-101903495',
  download_url = 'https://github.com/aryamanchoudhary123/Topsis-Aryaman-101903495/archive/v_01.tar.gz',
  keywords = ['Topsis', 'Ranking',],
  install_requires=[
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
