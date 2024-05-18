from setuptools import setup, find_packages

setup(
    name='sh1106_framework',
    version='0.0.2',
    author='Dan Convey',
    description='A state manager, graphics, image, and custom font drawing package for the SH1106 OLED screen based on the luma.oled package. It works with Raspberry Pi and other Linux-based single-board computers.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Other OS"
    ],
    install_requires=["luma.oled", "pillow"],
    entry_points={
        'console_scripts': [
            'sh1106_image_generator=sh1106_framework.sh1106_image_generator:main',
            'sh1106_font_generator=sh1106_framework.sh1106_font_generator:main'
        ]
    },
    python_requires='>=3.10',
)