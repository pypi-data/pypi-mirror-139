# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='baas_web',  # 包的名字
    author='perilong',  # 作者
    version='1.0.1',  # 版本号
    #license='MIT',

    description='baas web project',  # 描述
    author_email='yeqianlong@mrray.cn',  # 你的邮箱**
    packages=["baas", "config"],

    # 依赖包
    install_requires=[
        'seleniumwebui >= 1.0.5',
        "lxml >= 3.7.1",
        "configparser"
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        # 'Operating System :: Microsoft'  # 你的操作系统  OS Independent      Microsoft
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3.7',  # python版本 。。。
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
