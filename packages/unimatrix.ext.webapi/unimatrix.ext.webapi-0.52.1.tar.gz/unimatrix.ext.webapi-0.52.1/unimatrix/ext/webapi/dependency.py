# pylint: skip-file
import fastapi
import ioc


def inject(
    name: str,
    invoke: bool = False,
    default: object = None,
    *args, **kwargs
):
    """Injects the named dependency `name` into the :mod:`fastapi`
    dependency resolver.
    """
    async def provide():
        if not ioc.is_satisfied(name) and default is not None:
            dependency = default
        else:
            dependency = ioc.require(name)
        if not hasattr(dependency, '__aenter__'):
            yield dependency if not invoke else dependency(*args, **kwargs)
            return
        if invoke:
            dependency = dependency(*args, **kwargs)
        async with dependency:
            yield dependency
    return fastapi.Depends(provide)


def CurrentEntity(repository: str, auto_error: bool = True, dto: bool = False):
    """Lookup the entity that is identified by the request path parameters.

    Args:
        repository (str): the repository implementation to use, as injected
            through the :mod:`python-ioc` framework.
        auto_error (bool): indicates if the exception must be reraised if
            no entity was found given the request parameters.
        dto (bool): indicates if the entity should be returned as a Data
            Transfer Object (DTO). Default is ``True`` for ``GET`` requests
            and ``False`` for all other methods.

    Raises:
        :exc:`DoesNotExist` if `auto_error` is ``True`` and no entity could be
        found given the request parameters.

    Returns:
        The entity that was resolved based on the path parameters, or
        ``None`` if `auto_error` was ``False``.
    """
    async def lookup_entity(
        request: fastapi.Request,
        repository = inject(repository, True),
        dto: bool = dto
    ):
        if str.lower(request.method) == 'get':
            dto = True
        lookup = repository.transfer if dto else repository.get
        try:
            return await lookup(**request.path_params)
        except repository.DoesNotExist:
            if auto_error:
                raise
            return None
    return fastapi.Depends(lookup_entity)
