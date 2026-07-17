from pydub import AudioSegment


def convert_to_mp3(file_path: str) -> None:
    audio = AudioSegment.from_file(file_path)
    audio.export(file_path, format="mp3", bitrate="320k")
