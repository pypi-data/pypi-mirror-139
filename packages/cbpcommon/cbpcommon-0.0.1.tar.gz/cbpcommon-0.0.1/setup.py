from setuptools import setup

setup(
    name='cbpcommon',
    version='0.0.1',
    url='https://github.com/Crypto-Bot-Platform/cbpcommon',
    license='MIT',
    author='Boris Tsekinovsky',
    author_email='t.boris@gmail.com',
    description='Common library for Crypto Bot Platform',
    packages=['.'],
    include_package_data=True,
    install_requires=["avro", "confluent_kafka", "setuptools", "elasticsearch", "jsonpickle"],
)
