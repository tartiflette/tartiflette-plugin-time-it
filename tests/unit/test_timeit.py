import pytest


@pytest.mark.asyncio
async def test_timeit_bake():
    from tartiflette_plugin_time_it import bake, _SDL

    assert await bake("a", {}) == _SDL
