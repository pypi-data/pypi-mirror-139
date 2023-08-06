import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rosetta-easycache",# Replace with your own username
    version="0.0.4",
    author="Zhiyuan Zhang",
    author_email="zhangzhiyuan1@joyy.com",
    description="一个快速使用异步redis优化数据库查询项目",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.duowan.com/ai/nlp/easy-cache",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)