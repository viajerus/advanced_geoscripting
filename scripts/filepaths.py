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

        # Subdirectories and files
        self.ROUTES_DIR = self.RAW_DIR / "01_routes"
        self.PREPROCESSED_ROUTES_FILE = self.INTERIM_DIR / "preprocessed_routes.gpkg"

    def create_dirs(self) -> None:
        """Creats sub directories :return:"""
        for var, path in self.__dict__.items():
            if str(var).endswith("_DIR"):
                path.mkdir(parents=False, exist_ok=True)


class ResultPaths:
    """Creates result directories for CSV files and plots"""

    def __init__(self, output_dir: str, name: str) -> None:
        """Init"""
        self.OUTPUT_DIR = Path(output_dir) / name
        self.CSV_RESULTS_DIR = self.OUTPUT_DIR / "csv_results"
        self.PLOTS_DIR = self.OUTPUT_DIR / "plots"

    def create_dirs(self) -> None:
        """Creates result directories"""
        for path in [self.CSV_RESULTS_DIR, self.PLOTS_DIR]:
            path.mkdir(parents=False, exist_ok=True)
