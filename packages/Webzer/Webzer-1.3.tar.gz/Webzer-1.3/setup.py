from distutils.core import setup
setup(
  name = 'Webzer',         # How you named your package folder (MyLib)
  packages = ['Webzer'],   # Chose the same as "name"
  version = '1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Websites made easy.',   # Give a short description about your library
  author = 'LJDev',                   # Type in your name
  author_email = 'lfwjohns@googlemail.com',      # Type in your E-Mail
  url = 'https://github.com/KodeyCode/Webzer',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/KodeyCode/Webzer/archive/v1.3.tar.gz',    # I explain this later on
  keywords = ['Web Module', 'EASY-TO-USE', 'Websites'],   # Keywords that define your package best
  install_requires=[''],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',
  ],
)
