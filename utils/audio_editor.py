import music_tag


class AudioEditor:
    def __init__(self, file: str):
        self.__file = music_tag.load_file(file)

    def edit_cover(self, cover_file: str) -> None:
        with open(cover_file, "rb") as cover:
            self.__file["artwork"] = cover.read()

    def edit_title(self, title: str) -> None:
        self.__file["title"] = title

    def edit_artist(self, artist: str) -> None:
        self.__file["artist"] = artist

    def save_file(self) -> None:
        self.__file.save()
