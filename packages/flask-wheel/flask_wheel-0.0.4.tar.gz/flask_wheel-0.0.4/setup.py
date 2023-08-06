from setuptools import setup,find_packages

with open("README.md","r",encoding="utf-8")as f:
    long_ = f.read()

setup(
    name="flask_wheel",
    version="0.0.4",
    packages=find_packages(),
    description="basic flask project",
    long_description=long_,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "waitress",
        "flask-sqlalchemy",
        "flask-migrate",
        "python-dotenv",
        "flask-apscheduler",
    ]
)