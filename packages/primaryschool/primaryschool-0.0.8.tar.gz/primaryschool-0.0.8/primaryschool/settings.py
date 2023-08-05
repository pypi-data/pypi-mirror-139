
import os
import sys

app_name = 'primaryschool'
app_version = '0.0.8'
app_author = 'larryw3i'
app_author_email = 'larryw3i@163.com'
app_maintainer = app_author
app_maintainer_email = app_author_email
app_description = "primary school knowledge games"
app_url = "https://github.com/larryw3i/primaryschool"
app_contributors = [
    app_author,
    '',
]

install_prefix = 'python -m pip install '
requirements = [
    # product
    [  # ('requirement_name','version','project_url','License','license_url')
        (
            'pygame', '', 'https://github.com/pygame/pygame',
            'LGPL v2',
            'https://github.com/pygame/pygame/blob/main/docs/LGPL.txt'
        ),
        (
            'pygame-menu', '', 'https://github.com/ppizarror/pygame-menu',
            'MIT',
            'hhttps://github.com/ppizarror/pygame-menu/blob/master/LICENSE'
        ),
        (
            'xpinyin', '', 'https://github.com/lxneng/xpinyin',
            'BSD',
            'https://github.com/lxneng/xpinyin/blob/master/setup.py#L37'
        ),
        (
            'appdirs', '', 'https://github.com/ActiveState/appdirs',
            'MIT',
            'https://github.com/ActiveState/appdirs/blob/master/LICENSE.txt'
        ),
    ],
    [
        (  # dev
            'isort', '', 'https://github.com/pycqa/isort',
            'MIT', 'https://github.com/PyCQA/isort/blob/main/LICENSE'
        ),
        (
            'autopep8', '', 'https://github.com/hhatto/autopep8',
            'MIT', 'https://github.com/hhatto/autopep8/blob/master/LICENSE'
        ),
        (
            'nose2', '', 'https://github.com/nose-devs/nose2',
            'BSD License',
            'https://github.com/nose-devs/nose2/blob/main/setup.py#L57'
        )
    ]
]


def get_requirements_product():
    install_requires = []
    for r in requirements[0]:
        install_requires.append(r[0] + r[1])
    return install_requires


def install_requirements_product():
    requirements_product = get_requirements_product()
    os.system(install_prefix + requirements_product)


def get_requirements_dev():
    install_requires = ''
    for r in requirements:
        for _r in r:
            install_requires += ' ' + _r[0] + _r[1]
    return install_requires


def install_requirements_dev():
    requirements_dev = get_requirements_dev()
    os.system(install_prefix + requirements_dev)


def get_requirements_dev_u():
    install_requires = '-U'
    for r in requirements:
        for _r in r:
            install_requires += ' ' + _r[0]
    return install_requires


def install_requirements_dev_u():
    requirements_dev_u = get_requirements_dev_u()
    os.system(install_prefix + requirements_dev_u)
