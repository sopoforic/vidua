from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='vidua',
      description='Apply patches to ROMs and other files',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/sopoforic/vidua',
      author='Tracy Poff',
      author_email='tracy.poff@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      packages=['vidua'],
      entry_points={
        'console_scripts': [
            'vidua = vidua.scripts:main',
        ],
      },
      setup_requires=['setuptools_scm', 'pytest-runner'],
      tests_require=['pytest'],
      use_scm_version=True,
      zip_safe=True)
