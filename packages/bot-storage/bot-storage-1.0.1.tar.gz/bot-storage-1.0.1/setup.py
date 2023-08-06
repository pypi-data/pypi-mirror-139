import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="bot-storage",
	version="1.0.1",
	author="Daniil Marchenko, Ivan Romanchenko",
	author_email="vanvanych789@gmail.com",
	description="Storage for bots that allows you to save the states and data of users.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/IvanRomanchenko/bot-storage",
	packages=["bot_storage", ],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.6",
	install_requires=[
		"redis==4.1.4",
		"ujson==5.1.0",
	]
)
