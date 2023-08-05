from distutils.core import setup
from distutils import util
from pathlib import Path
import sys

if __name__ == "__main__":
    
    # check python version
    if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 8): 
        sys.exit("tcheasy needs at least python version 3.8!") 
    
    # package paths
    tcheasyPath = util.convert_path("tcheasy")

    # get version file
    versionPath = Path().cwd() / "tcheasy/version.py"

    main_ns = {}

    with open(str(versionPath)) as ver_file:
        exec(ver_file.read(), main_ns)

    # get long description
    longDescription = (Path().cwd() / "README.md").read_text()

    # running setup
    setup(
        name="tcheasy",
        version=main_ns['__version__'],
        description="A python decorator which checks types & restrictions for user inputs",
        long_description=longDescription,
        long_description_content_type="text/markdown",
        author="Daniel Kiermeier",
        author_email="d.kiermeier@layers-of-life.com",
        url="https://github.com/No9005/tcheasy",
        download_url="https://github.com/No9005/tcheasy/archive/refs/tags/v.1.1.0.tar.gz",
        license="MIT",
        package_dir={
            "tcheasy":tcheasyPath
        },
        packages=["tcheasy"]
    )