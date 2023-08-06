from json import dump, load
from pathlib import Path
from shutil import rmtree


class FileAdapter:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def create_dir(self) -> None:
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True)

    def delete_dir(self) -> None:
        rmtree(self.file_path.parent)

    def delete(self) -> None:
        self.file_path.unlink()

    def exists(self) -> bool:
        return self.file_path.exists()

    def load_file(self) -> str:
        with open(self.file_path) as file:
            return file.read()

    def save_file(self, data: str = "") -> None:
        with open(self.file_path, "w") as file:
            file.write(data)

    def load_json(self) -> dict:
        with open(self.file_path) as file:
            return load(file)

    def save_json(self, data: dict) -> None:
        with open(self.file_path, "w") as file:
            dump(data, file, indent=2)
