from setuptools import setup

setup(name='varipatch',
      description='Apply patches to ROMs and other files',
      url='http://github.com/sopoforic/varipatch',
      author='Tracy Poff',
      author_email='tracy.poff@gmail.com',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Topic :: Utilities',
      ],
      packages=['varipatch'],
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      zip_safe=True)
