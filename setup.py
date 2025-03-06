from setuptools import setup, find_packages

setup(
    name="pulse",  # Name of your package
    version="0.3",
    packages=find_packages(),
    install_requires=["click"],  # Add any other dependencies you may have
    entry_points={
        "console_scripts": [
            "pulse = pulse.pulse:cli",  # CLI entry point
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
