import mimetypes

from mutagen.id3 import APIC, ID3, TIT2, TPE1, Encoding, PictureType


class Track:
    @staticmethod
    def add_cover(track_path: str, image_path: str) -> None:
        track_tags = ID3(track_path)
        image_filename = image_path
        image_mime_type = mimetypes.guess_file_type(image_filename)[0]

        with open(image_filename, "rb") as image:
            cover = image.read()

        track_tags.setall(
            "APIC",
            [
                APIC(
                    mime=image_mime_type,
                    type=PictureType.COVER_FRONT,
                    data=cover,
                    encoding=Encoding.UTF8,
                )
            ],
        )

        track_tags.save()

    @staticmethod
    def add_artist(track_path: str, artist: str) -> None:
        track_tags = ID3(track_path)
        track_tags["TPE1"] = TPE1(encoding=Encoding.UTF8, text=artist)
        track_tags["TIT2"] = TIT2(encoding=Encoding.UTF8, text="ТЕКСТ")

        track_tags.save()

    @staticmethod
    def add_title(track_path: str, title: str) -> None:
        track_tags = ID3(track_path)
        track_tags["TIT2"] = TIT2(encoding=Encoding.UTF8, text=title)

        track_tags.save()
