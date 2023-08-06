from setuptools import setup, find_packages


setup(
    name='alanTools',
    version='0.1',
    license='MIT',
    author="Alan Koterba",
    author_email='alankoterba@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/alannxq/alanTools/archive/refs/tags/0.1.tar.gz',
    keywords='tool multitool',
    install_requires=[
          'platform',
          'os',
          'qrcode',
          'random',
          'requests'
      ],

)
