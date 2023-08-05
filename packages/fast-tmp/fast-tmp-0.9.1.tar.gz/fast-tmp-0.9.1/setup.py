# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_tmp',
 'fast_tmp.admin',
 'fast_tmp.admin.schema',
 'fast_tmp.admin.schema.forms',
 'fast_tmp.conf',
 'fast_tmp.jinja_extension',
 'fast_tmp.models',
 'fast_tmp.site',
 'fast_tmp.utils',
 'fastapi_cli',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.tests',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps.api',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps.api.endpoints']

package_data = \
{'': ['*'],
 'fast_tmp.admin': ['static/css/*',
                    'static/img/*',
                    'static/js/*',
                    'templates/*'],
 'fastapi_cli': ['tpl/project/*', 'tpl/static/*', 'tpl/static/static/*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

extras_require = \
{'cli': ['cookiecutter>=1.7.2,<2.0.0']}

entry_points = \
{'console_scripts': ['fast-tmp = fastapi_cli:main']}

setup_kwargs = {
    'name': 'fast-tmp',
    'version': '0.9.1',
    'description': '',
    'long_description': '# fast-tmp\n\n[![Python package](https://github.com/Chise1/fast-tmp/actions/workflows/test.yml/badge.svg)](https://github.com/Chise1/fast-tmp/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/Chise1/fast-tmp/branch/main/graph/badge.svg?token=7CZE532R0H)](https://codecov.io/gh/Chise1/fast-tmp)\n[![Documentation Status](https://readthedocs.org/projects/fast-tmp/badge/?version=latest)](https://fast-tmp.readthedocs.io/?badge=latest)\n![GitHub](https://img.shields.io/github/license/Chise1/fast-tmp)\n\n# 介绍\n\nfast-tmp项目受django-admin的影响，旨在实现一个基于sqlalchemy+fastapi+amis的通用后台管理平台。\n\n- sqlalchemy:python最受欢迎的数据库操作工具。\n- fastapi:新版本python最受欢迎的web框架之一。\n- amis:一款利用json数据生成页面的前端低代码项目。\n\n笔者前端能力比较弱，从实用主义出发，利用amis搭建后台管理的页面。这也为未来页面的功能拓展提供了无限可能。并摆脱前端开发的影响。（由于偷懒，登陆页面用的taber构建的。以后有时间了修改）\n更多内容查看[教程](https://fast-tmp.readthedocs.io/)\n## 示例\n\nurl:                http://124.222.119.206:8000/admin\n\nusername/password:  admin/admin\n\n## 该项目的存在意义\n\nfastapi是一款非常优秀的web框架，long2ice基于异步数据库访问库（tortoise-orm）构建了fastapi-admin项目，使用fastapi+tortoise-orm。\n笔者新项目需要使用到sqlalchemy，也没有找到合适的库，所以决定自己动手来实现自己需要的功能。\n\n## 页面展示\n\n![登陆](./docs/static/img/login.png)\n![主页](./docs/static/img/home.png)\n![userinfo](./docs/static/img/userinfo.png)\n![create](./docs/static/img/create.png)\n\n## 入门\n\n### 安装\n\n通过pip进行安装：\n\n```shell\npip install fast-tmp\n```\n\n如果使用poetry,则\n\n```shell\npoetry add fast-tmp\n```\n\n## 快速教程\n\n在项目启动的根目录先创建一个.env文件,主要内容如下：\n\n```text\nDATABASE_URL=sqlite:///example.db # 数据库\nSECRET_KEY=rtbhwaergvqerg # user加密用的密码\nDEBUG=False # 是否启动debug模式，debug模式会打印所有访问数据的的操作\n```\n\n如果你有这么一个model:\n\n```python\n# models.py\nfrom sqlalchemy import String, Boolean, Integer, DateTime, DECIMAL, Float, JSON, Text, Column\nfrom fast_tmp.models import Base\n\n\nclass UserInfo(Base):\n    __tablename__ = "userinfo"\n    id = Column(Integer, primary_key=True)\n    name = Column(String(128), unique=True)\n    age = Column(Integer, default=10, )\n    birthday = Column(DateTime)\n    money = Column(DECIMAL(scale=3))\n    height = Column(Float)\n    info = Column(JSON)\n    tag = Column(Text)\n    is_superuser = Column(Boolean(), default=True)\n\n```\n\n那么，你只需要构建一个页面model:\n\n```python\n# admin.py\nfrom fast_tmp.site import ModelAdmin\nfrom .models import UserInfo\n\n\nclass UserInfoAdmin(ModelAdmin):\n    model = UserInfo\n    create_fields = [UserInfo.name, UserInfo.age, UserInfo.birthday, UserInfo.money, UserInfo.height, UserInfo.info,\n                     UserInfo.tag, UserInfo.is_superuser]\n    update_fields = create_fields\n    list_display = [UserInfo.id, UserInfo.name, UserInfo.age, UserInfo.birthday, UserInfo.money, UserInfo.height,\n                    UserInfo.info,\n                    UserInfo.tag, UserInfo.is_superuser]\n```\n\n然后进行注册：\n\n```python\n# main.py\nfrom fast_tmp.site import register_model_site\nfrom example.admin import UserInfoAdmin\n\nregister_model_site({"Example": [UserInfoAdmin]})  # example是页面上标签名，对应是一个列表。\n```\n\n可以把admin功能单独启动或者注册到现有项目上： 注册到项目上\n\n```python\nfrom fastapi import FastAPI\n\nfrom fast_tmp.admin.server import admin\nfrom fast_tmp.site import register_model_site\nfrom example.admin import UserInfoAdmin\n\nregister_model_site({"Example": [UserInfoAdmin]})  # 注册页面\napp = FastAPI()\napp.mount("/admin", admin, name="admin", )  # 注册admin的app，注意暂时只能为/admin，以后会进行修改\n\nif __name__ == \'__main__\':  # 调试模式启动\n    import uvicorn\n\n    uvicorn.run(app, debug=True, port=8000, lifespan="on")\n```\n\n### 创建超级用户\n\n```shell\nfast-tmp createsuperuser username password\n```\n\n### 自定义指令\n\n在settings里面配置```EXTRA_SCRIPT```参数，就像配置django的参数一样，把脚本的相对导入路径写到这个字段列表里面，即可通过fast-tmp进行执行。\n\n可以通过```fast-tmp --help```查看当前有哪些执行指令\n',
    'author': 'Chise1',
    'author_email': 'chise123@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Chise1/fast-tmp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
