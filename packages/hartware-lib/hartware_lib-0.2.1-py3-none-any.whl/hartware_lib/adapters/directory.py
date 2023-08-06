from glob import glob
from json import dump, load
from pathlib import Path
from shutil import rmtree
from typing import List


class DirectoryAdapter:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path

    def create_dir(self) -> None:
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)

    def delete(self, filename: str) -> None:
        (self.dir_path / filename).unlink()

    def delete_dir(self) -> None:
        rmtree(self.dir_path)

    def search(self, filename: str = "*") -> List[Path]:
        return [
            self.dir_path / path
            for path in glob(str(self.dir_path / "**" / filename), recursive=True)
        ]

    def exists(self, filename: str) -> bool:
        return (self.dir_path / filename).exists()

    def load_file(self, filename: str) -> str:
        with open(self.dir_path / filename) as file:
            return file.read()

    def save_file(self, filename: str, data: str = "") -> None:
        with open(self.dir_path / filename, "w") as file:
            file.write(data)

    def load_json(self, filename: str) -> dict:
        with open(self.dir_path / filename) as file:
            return load(file)

    def save_json(self, filename: str, data: dict) -> None:
        with open(self.dir_path / filename, "w") as file:
            dump(data, file, indent=2)
