import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymcure",
    version="0.0.1.1.3",
    license='MIT',
    author="Vianney ADOU",
    author_mail="adoujmv@hmail.com",
    descripton="Mercure python module",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Ouleur/Pymcure",
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=[
        'grequests',
        'requests',
        'sseclient-py'
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    py_modules=['pymercure'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_rquires='>=3.6',
)