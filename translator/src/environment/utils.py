from .environment import Environment


def _has_variable(env: Environment, variable: str) -> bool:
    return variable in env.variables


def _has_variable_recursively(env: Environment, name: str) -> bool:
    if _has_variable(env, name):
        return True

    if env.has_parent:
        return _has_variable_recursively(env.parent, name)

    return False


def _update_variable(env: Environment, variable: str, value: str) -> None:
    env.variables[variable] = value


def _update_variable_recursively(env: Environment, variable: str, value: str) -> None:
    if variable in env.variables:
        env.variables[variable] = value

    if env.has_parent:
        _update_variable_recursively(env.parent, variable, value)
