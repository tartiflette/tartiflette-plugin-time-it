import logging
from time import time
from tartiflette import Directive, Scalar, Resolver


_SDL = """
directive @timeIt(useLogger: Boolean! = true) on FIELD_DEFINITION | FIELD
"""


class TimeIt:
    def __init__(self, config):
        self._logger = config.get("logger", logging.getLogger(__name__))

    async def on_field_execution(
        self, directive_args, next_resolver, parent_result, args, ctx, info
    ):
        start = time()

        results = await next_resolver(parent_result, args, ctx, info)

        end = time()

        field_name = info.schema_field.name
        if info.schema_field.parent_type:
            field_name = f"{info.schema_field.parent_type.name}.{field_name}"
        else:
            field_name = f"[Root].{field_name}"

        prt = f"{next_resolver} (Field {field_name}) took {end - start} seconds to execute."

        if directive_args["useLogger"]:
            self._logger.debug(prt)
        else:
            print(prt)
        return results


async def bake(schema_name, config):
    Directive(name="timeIt", schema_name=schema_name)(TimeIt(config))
    return _SDL
