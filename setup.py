from setuptools import setup

setup(
    name='wagtail_streamforms',
    version='1.0.0',
    description='wagtail_streamforms',
    long_description=open('README.md').read(),
    author='Stuart George',
    author_email='stuart@accentdesign.co.uk',
    url='https://github.com/AccentDesign/wagtail_streamforms/',
    download_url='https://pypi.python.org/pypi/wagtail_streamforms',
    license='MIT',
    packages=[
        'wagtail_streamforms'
    ],
    install_requires=[
        'Django>=1.11,<1.12',
        'django-appconf>=1.0.2',
        'django-model-utils>=3.0.0',
        'django-multi-email-field>=0.5.1',
        'django-recaptcha>=1.3.1',
        'wagtail>=1.12,<2'
    ],
    include_package_data=True,
    keywords=['wagtail', 'streamfield', 'forms', 'accent', 'design'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
