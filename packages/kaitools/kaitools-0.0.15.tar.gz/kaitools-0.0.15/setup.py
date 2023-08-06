import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaitools",  # 包名  pypi的网址后缀 也是 pip install [包名]命令用到的
    version="0.0.15",  # 版本号  pip install 或者 xx upgrade xx
    author="Example Author",  # 作者名
    author_email="author@example.com",  # 作者邮箱
    description="A small example package",  # 简介
    long_description=long_description,   # 读取README.md的内容, 在pypi里包主页显示
    long_description_content_type="text/markdown",
    url="https://github.com/xxx/xxx",  # 包主页显示的链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
