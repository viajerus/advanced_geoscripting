#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class to define output file names and folders"""

from pathlib import Path


class FilePaths:
    """Stores paths for output files"""

    def __init__(self, output_dir: str, name: str) -> None:
        """Init"""

        self.OUTPUT_DIR = Path(output_dir) / name

        # Top level directories
        self.RAW_DIR = self.OUTPUT_DIR / "01_raw"
        self.INTERIM_DIR = self.OUTPUT_DIR / "02_interim"
        self.FINAL_DIR = self.OUTPUT_DIR / "03_final"

        self.ROUTES_DIR = self.RAW_DIR / "01_routes"
        self.PREPROCESSED_ROUTES_FILE = self.INTERIM_DIR / "preprocessed_routes.gpkg"

    def create_dirs(self) -> None:
        """
        Creats sub directories
        :return:
        """
        for var, path in self.__dict__.items():
            if str(var).endswith("_DIR"):
                path.mkdir(parents=False, exist_ok=True)