from distutils.core import setup
setup(
  name = 'ez_pd',         # How you named your package folder (MyLib)
  packages = ['ez_pd'],   # Chose the same as "name"
  version = '1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a package to make it easier to use pandas for bundling',   # Give a short description about your library
  author = 'Fabian Matus',                   # Type in your name
  author_email = 'fabiax.e.m10@gmail.com',      # Type in your E-Mail
  url = 'https://https://github.com/fabi-ignacio',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/fabi-ignacio/ez-pandas/archive/refs/tags/v1.4.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
      ],
  classifiers=[
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10',
  ],
)