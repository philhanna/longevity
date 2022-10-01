from setuptools import setup

setup(
    name='longevity',
    version='1.0.0',
    packages=['tests', 'longevity'],
    install_requires=[
        'beautifulsoup4==4.11.1',
        'bs4==0.0.1',
        'certifi==2022.9.24',
        'charset-normalizer==2.1.1',
        'idna==3.4',
        'requests==2.28.1',
        'soupsieve==2.3.2.post1',
        'urllib3==1.26.12',
    ],
    url='https://github.com/philhanna/longevity',
    license='MIT',
    author='saspeh',
    author_email='ph1204@gmail.com',
    description='Life expectancy according to the Social Security Administration'
)
