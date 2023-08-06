from json import dump, load

from hartware_lib.adapters.file import FileAdapter


class JsonFileAdapter(FileAdapter):
    def load_json(self, filename: str) -> dict:
        with open(self.dir_path / filename) as file:
            return load(file)

    def save_json(self, filename: str, data: dict) -> None:
        with open(self.dir_path / filename, "w") as file:
            dump(data, file, indent=2)
