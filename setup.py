from setuptools import setup

setup(
    name='wagtail_streamforms',
    version='0.0.0',
    description='wagtail_streamforms',
    long_description=open('README.md').read(),
    author='',
    author_email='',
    url='',
    download_url='',
    license='MIT',
    packages=[
        'wagtail_streamforms'
    ],
    install_requires=[
        'Django>=1.8.1,<1.12',
        'django-appconf>=1.0.2',
        'django-model-utils>=3.0.0',
        'django-multi-email-field>=0.5.1',
        'django-recaptcha>=1.3.1',
        'wagtail>=1.12,<2'
    ],
    include_package_data=True,
    keywords=['accent', 'design'],
    classifiers=[
    ],
)
