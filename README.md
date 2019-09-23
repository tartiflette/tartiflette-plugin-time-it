# tartiflette-plugin-time-it

Allows you to view field time execution in your log as easily as :

```
type Example {
    aField: String @timeIt
}
```

By default the `timeIt` directive will use it's own logger retrieved by `logging.getLogger("__name__")`.

If called with `useLogger: false` it will use the print statement.

At init time, using the `create_engine` api, you can pass your own logger to the directive.

```python
engine = await create_engine(sdl, modules=[{"name": "tartiflette_plugin_time_it", "config": {"logger": myLogger()}}])
```