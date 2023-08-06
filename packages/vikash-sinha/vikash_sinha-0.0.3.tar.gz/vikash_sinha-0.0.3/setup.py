from setuptools import setup, find_packages


def adds(num1, num2):
    return num1 + num2


def subs(num1, num2):
    return num1 - num2


def mults(num1, num2):
    return num1 * num2


def divsd(num1, num2):
    return num1 / num2


class JaiMataDi:
    def __init__(self, name, age, roll):
        self.name = name
        self.age = age
        self.roll = roll

    def get_name(self):
        return self.name

    def get_all(self):
        return [self.name, self.roll, self.age]


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
    "Operating System :: MacOS :: MacOS 9",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: MS-DOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier",
    "Operating System :: Microsoft :: Windows :: Windows 7",
    "Operating System :: Microsoft :: Windows :: Windows 95/98/2000",
    "Operating System :: Microsoft :: Windows :: Windows CE",
    "Operating System :: POSIX :: BSD :: NetBSD",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: GNU Hurd",
    "Operating System :: POSIX :: HP-UX",
    "Operating System :: POSIX :: IRIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: Other",
    "Operating System :: POSIX :: SCO",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: Unix",
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
]

setup(
    name='vikash_sinha',
    version='0.0.3',
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
