_solvers = dict()


def register(*, day):
    def decorator(fn):
        if day in _solvers:
            raise ValueError(f'Day {day} is already registered')
        _solvers[day] = fn
        return fn
    return decorator


def get_solver(day):
    return _solvers[day]
