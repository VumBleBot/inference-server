from pydantic import BaseModel


class Song(BaseModel):
    artist: str
    song_name: str
