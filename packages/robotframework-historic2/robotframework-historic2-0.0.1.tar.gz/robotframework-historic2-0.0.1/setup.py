from setuptools import find_packages, setup

setup(
      name='robotframework-historic2',
      version="0.0.1",
      description='Custom report to display robotframework historical execution records',
      long_description='Robotframework Historic is custom report to display historical execution records using MySQL + Flask',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework historical execution report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-historic',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'robotframework',
          'config',
          'flask',
          'flask-mysqldb'
      ],
      entry_points={
          'console_scripts': [
              'rfhistoric2=robotframework_historic2.app:main',
              'rfhistoricparser2=robotframework_historic2.parserargs:main',
              'rfhistoricreparser2=robotframework_historic2.reparserargs:main',
              'rfhistoricsetup2=robotframework_historic2.setupargs:main',
          ]
      },
)
