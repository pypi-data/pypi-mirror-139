from setuptools import setup

setup(
    name='py-certificategenerator',
    version='0.1',
    packages=['py-certificategenerator'],
    url='https://github.com/codinlikewilly/py-certgenerator',
    license='MIT ',
    author='will',
    author_email='will@theapiguys.com',
    description='Generates SSL x509 certificates',
    download_url="https://github.com/codinlikewilly/py-certificategenerator/archive/refs/tags/v_01.tar.gz",
    keywords=['x509', 'SSL', 'OpenSSL'],
    install_requires=[
        'pyopenssl',
    ],
)
