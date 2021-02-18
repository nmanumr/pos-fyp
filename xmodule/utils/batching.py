from typing import Iterator, Generator, Union, Iterable


def iter_chunks(iterator: Union[Iterator, Iterable], n: int) -> Generator:
    """
    :param iterator: An iterator/iterable
    :param n: Chunk-size
    :return: Generator w/chunks of `iterator`.
    """
    if not hasattr(iterator, '__next__'):
        iterator = iter(iterator)

    chunk = []
    try:
        while True:
            for _ in range(n):
                chunk.append(next(iterator))

            yield chunk
            chunk = []
    except StopIteration:
        pass

    if chunk:
        yield chunk
