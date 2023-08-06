from setuptools import setup

setup(
    name='x509generator',
    version='0.3',
    packages=['x509generator'],
    url='https://github.com/codinlikewilly/py-certgenerator',
    license='MIT ',
    author='will',
    author_email='will@theapiguys.com',
    description='Generates SSL x509 certificates',
    download_url="https://github.com/codinlikewilly/x509generator/archive/refs/tags/v_03.tar.gz",
    keywords=['x509', 'SSL', 'OpenSSL'],
    install_requires=[
        'pyopenssl',
    ],
)
