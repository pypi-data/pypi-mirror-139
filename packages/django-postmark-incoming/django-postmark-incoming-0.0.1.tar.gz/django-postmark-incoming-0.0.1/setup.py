import setuptools

setuptools.setup(
    name="django-postmark-incoming",
    author="Harry Khanna",
    author_email="harry@khanna.cc",
    description="Django conveniences for Postmark Incoming Emails",
    license="MIT",
    url="https://github.com/hkhanna/django-postmark-incoming",
    packages=setuptools.find_packages(),
    install_requires=["Django"],
    python_requires=">=3.8",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
    ],
)
