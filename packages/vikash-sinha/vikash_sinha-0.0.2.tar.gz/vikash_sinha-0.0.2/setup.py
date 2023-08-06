from setuptools import setup, find_packages

long_description = ""
try:
    long_description += open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read()
except:
    pass
try:
    long_description += '\n\n' + open('CHANGELOG.txt').read()
except:
    pass

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
]

setup(
    name='vikash_sinha',
    version='0.0.2',
    description="A very basic program",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Vikash Kumar',
    author_email='vikashsinha0rns@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='vikash_sinha',
    packages=find_packages(),
    install_requires=['']
)
