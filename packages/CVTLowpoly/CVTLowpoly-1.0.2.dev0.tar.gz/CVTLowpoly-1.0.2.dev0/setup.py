import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CVTLowpoly",
    version="1.0.2.dev",
    author="Cong.Xie",
    author_email="xiconxi@gmail.com",
    description="A fast library for image lowpoly generation based on centroid voronoi diagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anapupa/PyCVTLowpoly",
    project_urls={
        "Bug Tracker": "https://github.com/anapupa/PyCVTLowpoly/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['taichi', 'taichi_glsl', 'scipy', 'opencv-python', 'numpy'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)