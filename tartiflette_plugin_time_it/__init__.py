import logging

from time import time
from typing import Any, Coroutine, Dict, Optional

from tartiflette import Directive

_SDL = """
directive @timeIt(useLogger: Boolean! = true) on FIELD_DEFINITION | FIELD
"""


class TimeItDirective:
    """
    Directive that will print execution duration of a field.
    """

    def __init__(self, config: Optional[Dict[str, Any]]) -> None:
        """
        :param config: configuration of the directive
        :type config: Optional[Dict[str, Any]]
        """
        if config is None:
            config = {}

        self._logger = config.get("logger", logging.getLogger(__name__))

    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Coroutine,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        """
        Directive that will print execution duration of a field.
        :param directive_args: arguments passed to the directive
        :param next_resolver: next resolver to call
        :param parent: default root value or field parent value
        :param args: computed arguments related to the resolved field
        :param ctx: context passed to the query execution
        :param info: information related to the execution and resolved field
        :type directive_args: Dict[str, Any]
        :type next_resolver: Coroutine
        :type parent: Optional[Any]
        :type args: Dict[str, Any]
        :type ctx: Optional[Any]
        :type info: ResolveInfo
        :return: the computed field value
        :rtype: Any
        """
        start_time = time()
        result = await next_resolver(parent, args, ctx, info)

        prt = (
            f"{next_resolver} (Field "
            f"{info.parent_type.name}.{info.field_name}) took "
            f"{time() - start_time} seconds to execute."
        )
        if directive_args["useLogger"]:
            self._logger.debug(prt)
        else:
            print(prt)
        return result


async def bake(
    schema_name: str, config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Links the directive to the appropriate schema and returns the SDL
    related to the directive.
    :param schema_name: schema name to link with
    :param config: configuration of the directive
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the SDL related to the directive
    :rtype: str
    """
    Directive("timeIt", schema_name=schema_name)(TimeItDirective(config))
    return _SDL
