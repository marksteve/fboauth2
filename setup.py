"""
========
fboauth2
========

Bare minimum Facebook OAuth2 client


-----
Usage
-----

::

    from fboauth2 import FBClient
    fbclient = FBClient(CLIENT_ID, CLIENT_SECRET, scope='publish_stream',
                        redirect_uri='http://example.com/callback')
    # Point users to auth url
    redirect(fbclient.get_auth_url())
    # Pass code to get access token
    code = params['code']
    access_token = fbclient.get_access_token(code)
    # Make graph requests
    me = fbclient.graph_request('me')
    print me['name']


-------
License
-------

http://marksteve.mit-license.org/
"""

from setuptools import setup


setup(
    name='fboauth2',
    version='0.1.1',
    url='https://github.com/marksteve/fboauth2',
    license='MIT',
    author='Mark Steve Samson',
    author_email='hello@marksteve.com',
    description='Bare minimum Facebook OAuth2 client',
    long_description=__doc__,
    py_modules=['fboauth2'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests>=0.14',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
