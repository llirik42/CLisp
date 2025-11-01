# CLisp — Lisp-интерпретатор, написанный на C

## Подготовительные действия

- установить [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#installation)
- сгенерировать парсер для Lisp:

```bash
cd translator/
```

```bash
cd translator/
```

```bash
uv venv
```

```bash
source .venv/bin/activate
```

```bash
antlr4 -Dlanguage=Python3 Lisp.g4
```

```bash
uv sync
```

(необязательно)
```bash
deactivate
```

Предпоследняя команда нужна, чтобы при сборке каждый раз не создавать виртуальное окружение python, а использовать то, которое создастся `uv venv` со всеми нужными зависимостями

## Запуск интерпретатора

```bash
./clisp example.clj
```
