from setuptools import setup, find_packages

setup(
    name='yixsoft-ezmysql',
    version='0.0.2',
    author='yixsoft',
    author_email='davepotter@163.com',
    url='https://gitee.com/yixsoft/python-ezymysql',
    packages=find_packages(),
    description=u'Auto scan table structure and generate sql & execute by dict',
    install_requires=['mysql-connector']
)
