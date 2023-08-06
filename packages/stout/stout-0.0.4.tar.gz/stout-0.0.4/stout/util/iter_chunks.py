def iter_chunks(_list, _chunk_size):
    for i in range(0, len(_list), _chunk_size):
        yield _list[i:i+_chunk_size]