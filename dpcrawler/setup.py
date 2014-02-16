import setuptools


setuptools.setup(
    name='dpcrawler',
    version='1.0',
    url='http://www.geekie.com.br',
    maintainer='nic',
    maintainer_email='nwerneck@gmail.com',
    packages=['dpcrawler'],
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'dpcrawler = dpcrawler.tools.dpcrawler:main',
        ],
    },
)
