from .environment import Environment


def _has_variable(env: Environment, variable: str) -> bool:
    return variable in env.variables


def _has_variable_recursively(env: Environment, name: str) -> bool:
    if _has_variable(env, name):
        return True

    if env.has_parent:
        return _has_variable_recursively(env.parent, name)

    return False


def _update_variable(env: Environment, name: str, value: str) -> None:
    env.variables[name] = value


def _update_variable_recursively(env: Environment, name: str, value: str) -> None:
    if name in env.variables:
        env.variables[name] = value

    if env.has_parent:
        _update_variable_recursively(env.parent, name, value)
