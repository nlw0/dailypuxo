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
        'retrying',
        'simplejson',
        'python-dateutil',
    ],
    entry_points={
        'console_scripts': [
            'dpcrawler = dpcrawler.tools.dpcrawler:main',
            'gen_dart_data = dpcrawler.tools.gen_dart_data:main',
        ],
    },
)
