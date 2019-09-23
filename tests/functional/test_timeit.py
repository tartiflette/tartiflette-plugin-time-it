import asyncio

from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_timeit_ok():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.bob", schema_name="test_timeit_ok")
    async def bob_resolver(*_args, **_kwargs):
        return {}

    @Resolver("Ninja.name", schema_name="test_timeit_ok")
    async def bob_name_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OuiOui"

    engine = await create_engine(
        sdl="""
        type Ninja {
            name: String @timeIt(useLogger: true)
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
        schema_name="test_timeit_ok",
    )

    assert await engine.execute("query a { bob { name } } ") == {
        "data": {"bob": {"name": "OuiOui"}}
    }

    assert logger.debug.called


@pytest.mark.asyncio
async def test_timeit_false():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.bob", schema_name="test_timeit_false")
    async def bob_resolver(*_args, **_kwargs):
        return {}

    @Resolver("Ninja.name", schema_name="test_timeit_false")
    async def bob_name_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OuiOui"

    engine = await create_engine(
        sdl="""
        type Ninja {
            name: String @timeIt(useLogger: false)
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
        schema_name="test_timeit_false",
    )

    assert await engine.execute("query a { bob { name } } ") == {
        "data": {"bob": {"name": "OuiOui"}}
    }

    assert not logger.debug.called


@pytest.mark.asyncio
async def test_timeit_default():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.bob", schema_name="test_timeit_default")
    async def bob_resolver(*_args, **_kwargs):
        return {}

    @Resolver("Ninja.name", schema_name="test_timeit_default")
    async def bob_name_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OuiOui"

    engine = await create_engine(
        sdl="""
        type Ninja {
            name: String @timeIt
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
        schema_name="test_timeit_default",
    )

    assert await engine.execute("query a { bob { name } } ") == {
        "data": {"bob": {"name": "OuiOui"}}
    }

    assert logger.debug.called


@pytest.mark.asyncio
async def test_timeit_no_config():
    @Resolver("Query.bob", schema_name="test_timeit_no_config")
    async def bob_resolver(*_args, **_kwargs):
        return {}

    @Resolver("Ninja.name", schema_name="test_timeit_no_config")
    async def bob_name_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OuiOui"

    engine = await create_engine(
        sdl="""
        type Ninja {
            name: String @timeIt
        }

        type Query {
            bob: Ninja
        }
        """,
        modules=["tartiflette_plugin_time_it"],
        schema_name="test_timeit_no_config",
    )

    assert await engine.execute("query a { bob { name } } ") == {
        "data": {"bob": {"name": "OuiOui"}}
    }
