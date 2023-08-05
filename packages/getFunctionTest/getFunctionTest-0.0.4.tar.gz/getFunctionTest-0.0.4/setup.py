from setuptools import setup, find_packages

setup(
    name='getFunctionTest',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'getFileTest = src.functionTest:getFunction'
        ]
    },
    author_email='email@gmail.com',
    version='0.0.4',
    description='Test buat library python',
    author='sinbad',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
)
