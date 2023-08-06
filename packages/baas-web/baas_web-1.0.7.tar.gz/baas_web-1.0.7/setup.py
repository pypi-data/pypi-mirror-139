# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='baas_web',  # 包的名字
    author='perilong',  # 作者
    version='1.0.7',  # 版本号
    #license='MIT',

    description='baas web project',  # 描述
    author_email='yeqianlong@mrray.cn',  # 你的邮箱**
    packages=["baasWeb"],

    # 依赖包
    install_requires=[
        'seleniumwebui >= 1.0.5',
    ],

)
