import pathlib
import setuptools

setuptools.setup(
    name='django-classy-start',
    version='0.0.1',
    author='Mfon Eti-mfon',
    author_email='mfon@etimfon.com',
    description=(
        'A command line utility for starting Django projects and apps in '
        'a most classy manner'
    ),
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/mfonism/django-classy-start',
    packages=setuptools.find_packages(include=['classy_start', 'classy_start.*']),
    package_data={
        'classy_start': ['conf/*.py-tpl', 'conf/**/*.py-tpl', 'conf/**/**/*.py-tpl']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=['Django>=3.1', 'python-dotenv>=0.14.0'],
    tests_require=['pytest>=6.0.1', 'pytest-subprocess>=1.0.0'],
    entry_points={'console_scripts': ['classy-start=classy_start.cli:main']},
)
