from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


if __name__ == "__main__":
    setup(
        name='TodoList',
        description='Todo List Web Server',
        license='MIT',
        url='dfsco.com',
        version='0.1.0.dev0',
        author='Raphael Goyran',
        author_email='raphael@dfsco.com',  # hey, I'm an optimist :)
        maintainer='Raphael Goyran',
        maintainer_email='raphael@dfsco.com',
        keywords='todo list Donnelley Financial Solutions',
        long_description='A basic Todo List server',
        packages=['todo'],
        include_package_data=True,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=['flask==1.0.2'],
    )

