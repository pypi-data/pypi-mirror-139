from distutils.core import setup

setup(
    name = "HypixelWrapper",
    packages = ["HypixelWrapper"],
    version = "0.0.1",
    license = "MIT",
    description = "Hypixel API Wrapper",
    author = "LoserEXE",
    url = "https://github.com/Loser-EXE/HypixPY",
    keywords = ["Minecraft", "Hypixel"],
    install_requires = [
        "requests",
        "mojang",
        "requests_html"
    ],
      classifiers=[
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
  ],
)