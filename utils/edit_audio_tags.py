from mutagen.id3 import APIC, ID3, TIT2, TPE1


def edit_tags(file: str, title: str, artist: str) -> None:
    track_tags = ID3(file)
    track_tags["TIT2"] = TIT2(encoding=3, text=[title])
    track_tags["TPE1"] = TPE1(encoding=3, text=[artist])

    with open(file, "rb") as cover:
        track_tags.add(
            APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=cover.read(),
            )
        )

    track_tags.save()
