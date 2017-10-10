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
        'Django',
        'django-appconf',
        'django-model-utils',
        'django-multi-email-field',
        'django-recaptcha',
        'wagtail'
    ],
    include_package_data=True,
    keywords=['accent', 'design'],
    classifiers=[
    ],
)
