from typing import Dict

import pytest

from app.photos.add_photo import add_photo


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "photo_id,description,result",
    [
        (1, "cat", {1: "cat", 2: "dog"}),
        (2, "0", {1: "cat", 2: "0"}),
        (3, "some", {1: "cat", 2: "0", 3: "some"}),
    ]
)
async def test_add_photo(photo_id: int, description: str, result: Dict[int, str]):
    res = await add_photo(photo_id, description)
    assert res == result
