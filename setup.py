from setuptools import setup, find_packages

setup(
    name             = 'pyPlaylistManager',
    version          = '0.1',
    description      = 'Music playlist manage library',
    author           = 'ParkJeongseop',
    author_email     = 'parkjeongseop@parkjeongseop.com',
    url              = 'https://github.com/ParkJeongseop/PlaylistManager',
    install_requires = [ 'selenium' ],
    keywords         = ['music playlist', 'playlist manage'],
    python_requires  = '>=3',
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)