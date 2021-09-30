from typing import Dict

from .data import my_photos


async def add_photo(photo_id: int, description: str) -> Dict[int, str]:
    my_photos[photo_id] = description
    return my_photos
