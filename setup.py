from setuptools import setup

setup(
    name='longevity',
    version='1.2.0',
    packages=['tests', 'longevity'],
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'pytest',
        'requests',
    ],
    url='https://github.com/philhanna/longevity',
    license='MIT',
    author='saspeh',
    author_email='ph1204@gmail.com',
    description='Life expectancy according to the Social Security Administration'
)
