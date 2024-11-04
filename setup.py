from setuptools import setup, find_packages

setup(
    name='Demiurge',
    version='0.01 debug',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Podmasterye=Podmasterye.main:main',  # Замените `mycli` на имя команды, которое вы хотите использовать
        ],
    },
)