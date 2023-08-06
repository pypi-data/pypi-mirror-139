import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jenkins-plugins-auto-update",
    version="1.0.1",
    author="ThePotatoCamera",
    author_email="alex0xela@outlook.com",
    description="Updates Jenkins plugins with the magic of automation... and Selenium. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThePotatoCamera/JenkinsPluginsAutoUpdate",
    project_urls={
        "Bug Tracker": "https://github.com/ThePotatoCamera/JenkinsPluginsAutoUpdate/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
