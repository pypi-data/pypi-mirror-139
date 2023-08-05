
from setuptools import setup, find_packages

setup(
    name = "nonebot-plugin-read_60s",
    version = "0.2.0",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
    description = "time and path tool",
    long_description = "time and path tool",
    license = "MIT Licence",

    url = "https://github.com/fengmm521/pipProject",
    author = "mage",
    author_email = "mage@woodcol.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    zip_safe = False,
    install_requires = ['requests',
                        'Config',
                        'require',
                        'AsyncIOScheduler',
                        'json',
                        'nonebot',
                        'Message',
                        'BaseSettings',
                        'Extra',
                        'Field'
                        ]
)