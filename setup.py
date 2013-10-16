"""
django-httpsiframecookiesetter
-----------------

A workaround for Safari\'s strict cookie policy when trying to write cookies from within an iframe under http

"""
from setuptools import setup, find_packages


setup(
    name='django-httpsiframecookiesetter',
    version='0.0.4',
    url='https://github.com/philroche/django-httpsiframecookiesetter',
    license='Public Domain',
    author='Philip Roche',
    author_email='phil@tinyviking.ie',
    description='A workaround for Safari\'s strict cookie policy when trying to write cookies from within an iframe under https',
    keywords = "django safari cookie https",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'django',
        'pyyaml',
        'ua-parser',
        'user-agents'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
