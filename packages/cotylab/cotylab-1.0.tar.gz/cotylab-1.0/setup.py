from setuptools import find_namespace_packages, setup

setup(
    name='cotylab',
    version='1.0',
    license='MIT',
    description='컴퓨팅 사고력 교육을 위한 오픈소스',
    author='cotylab',
    author_email='misoncorp@gmail.com',
    url='https://github.com/misoncorp/cotylab',
    packages=find_namespace_packages(where='src', include=['cotylab.*']),
    package_dir={'': 'src'},
    install_requires=[
    ]
)
