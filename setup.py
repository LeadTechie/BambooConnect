from distutils.core import setup
setup(
  name = 'bamboo_connect',         # How you named your package folder (MyLib)
  packages = ['bamboo_connect','extractors','loaders','samples','support','transformers'],   # Chose the same as "name"
  version = '0.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Bamboo Connect is a lightweight ETL (Extract, Transform, Load) library with examples and templates. It enables developers to quickly extract, transform, reconcile and then load resulting data securely. This avoids time consuming manual error prone tasks.',   # Give a short description about your library
  author = 'Chris Rowe',                   # Type in your name
  author_email = 'leadtechie@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/LeadTechie/BambooConnect',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LeadTechie/BambooConnect/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ETL', 'PANDAS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'pandas',
    'google_spreadsheet',
    'google-auth-oauthlib',
    'gspread',
    'requests',
    'jira',
    'coverage',
    'ruamel-yaml',
    'tabulate'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9'
  ],
)
