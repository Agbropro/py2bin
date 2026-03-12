"""py2bin – Python-to-native-binary compiler library.

Typical usage
-------------
::

    from pathlib import Path
    from py2bin import Py2BinConfig, Py2BinPipeline
    from py2bin import PyzPackager, XxdConverter, CCompiler

    config = Py2BinConfig(
        project_dir=Path("./myapp"),
        entry_script="__main__.py",
        output_dir=Path("./build"),
        app_name="myapp",
    )

    pipeline = Py2BinPipeline(
        packager=PyzPackager(),
        converter=XxdConverter(),
        compiler=CCompiler(),
    )

    result = pipeline.run(config)
    if result.success:
        print(f"Binary: {result.binary_path}")
"""

from py2bin.infrastructure.compiler import CCompiler
from py2bin.infrastructure.converter import XxdConverter
from py2bin.infrastructure.packager import PyzPackager
from py2bin.interfaces.interfaces import ICompiler, IConverter, IPackager
from py2bin.pipeline import Py2BinPipeline
from py2bin.schemas.schemas import BuildResult, Py2BinConfig

__all__ = [
    # Config & result
    "Py2BinConfig",
    "BuildResult",
    # Pipeline
    "Py2BinPipeline",
    # Concrete implementations
    "PyzPackager",
    "XxdConverter",
    "CCompiler",
    # Interfaces (for custom implementations)
    "IPackager",
    "IConverter",
    "ICompiler",
]

__version__ = "0.1.0"
