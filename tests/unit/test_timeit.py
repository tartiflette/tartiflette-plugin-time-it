import pytest


@pytest.mark.asyncio
async def test_timeit_bake():
    from tartiflette_plugin_time_it import _SDL, bake

    assert await bake("a", {}) == _SDL
