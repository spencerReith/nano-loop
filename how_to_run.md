# How to run

Run everything from the repo root. You need Docker running and `KEY=<openrouter key>` in `.env`.

## Control

```
uv run python -c "from control.main import Control; print(Control('ibm-granite/granite-4.2-8b', 'your question').start())"
```

## NanoLoop

Interactive:

```
uv run python -c "from nano_loop.main import NanoLoop; NanoLoop('ibm-granite/granite-4.2-8b', False).start()"
```

Headless:

```
uv run python -c "from nano_loop.main import NanoLoop; print(NanoLoop('ibm-granite/granite-4.2-8b', True, 'your question').start())"
```

## SimpleBench

```
uv run python -m simple_bench.benchmark [model ...]
```

Defaults to `ibm-granite/granite-4.2-8b`. Results go to `simple_bench/results/`, logs to `simple_bench/logs/`.
