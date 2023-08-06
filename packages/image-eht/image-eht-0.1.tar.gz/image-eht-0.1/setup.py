from setuptools import setup,find_packages


setup(name="image-eht",
      version="0.1",
      packages=find_packages(),
      description="image enhancement tool",
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "imgaug",
          "tqdm"
      ]
      )