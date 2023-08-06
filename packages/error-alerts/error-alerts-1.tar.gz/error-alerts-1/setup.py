from setuptools import setup

setup(
    name = 'error-alerts',
    packages = ['alerts'],
    version = '1',
    description = 'Error alerts via Telegram',
    url = 'https://github.com/xjxckk/error-alerts/',
    download_url = 'https://github.com/xjxckk/error-alerts/archive/refs/tags/v1.tar.gz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )