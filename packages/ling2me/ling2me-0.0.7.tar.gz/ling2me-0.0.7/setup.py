from setuptools import setup

setup(name='ling2me',
      version='0.0.7',
      description='A Python module to translate',
      long_description=open('README.rst').read(),
      long_description_content_type="text/x-rst",
      keywords=['api translate', 'translate', 'languages', ' translated', 'translating'],
      url='https://github.com/nicolasmarin/ling2me-python',
      download_url='https://github.com/nicolasmarin/ling2me-python/archive/refs/heads/main.zip',
      install_requires=[
          'requests',
      ],
      author='nicolasmarin',
      author_email='info@ling2me.com',
      license='GPLv3',
      packages=['ling2me'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          ])
