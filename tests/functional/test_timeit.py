import asyncio
from unittest.mock import Mock

import pytest
from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_timeit():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.bob")
    async def bob_resolver(*_args, **_kwargs):
        return {}

    @Resolver("Ninja.name")
    async def bob_name_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OuiOui"

    engine = await create_engine(
        sdl="""
        type Ninja {
            name: String @timeIt(userLogger: True)
        }

        type Query {
            bob: Ninja
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_time_it",
                "config": {"logger": logger},
            }
        ],
    )

    assert await engine.execute("query a { bob { name } } ") == {
        "data": {"bob": {"name": "OuiOui"}}
    }

    assert logger.debug.called
