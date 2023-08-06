from distutils.core import setup
setup(
  name = 'alanTools',         
  packages = ['alanTools'],   
  version = '1.2',
  license='MIT',
  description = 'Compilation of functions and modules',
  author = 'Alan Koterba',
  author_email = 'alankoterba12321@gmail.com',
  package_dir={'': 'src'},
  url = 'https://github.com/alannxq/alanTools',
  download_url = 'https://github.com/alannxq/alanTools/archive/refs/tags/0.2.tar.gz',    # I explain this later on
  keywords = ['nice', 'compilation', 'tools'],   # Keywords that define your package best
  install_requires=["random", "os", "platform", "qrcode"],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
