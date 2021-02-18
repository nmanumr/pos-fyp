import gc


class BatchQuerySetIterator:
    DEFAULT_BATCH_SIZE = 1000

    def __init__(self, queryset, batch_size=None, iter_queryset=None):
        if batch_size and (not isinstance(batch_size, int) or batch_size < 1):
            raise TypeError('Invalid batch_size')

        self.batch_size = batch_size or self.DEFAULT_BATCH_SIZE
        self.queryset = queryset
        self.iter_queryset = iter_queryset

    # noinspection PyProtectedMember
    def get_iter_queryset(self):
        if self.iter_queryset is None:
            qs = self.queryset.model.objects.all()
            qs.query = self.queryset.query.clone()
            qs.query.where = qs.query.where_class()

            qs._prefetch_related_lookups = self.queryset._prefetch_related_lookups
            qs._iterable_class = self.queryset._iterable_class
            qs._fields = self.queryset._fields
            qs._sticky_filter = self.queryset._sticky_filter
            self.iter_queryset = qs

        return self.iter_queryset

    def __len__(self):
        return self.queryset.count()

    def __iter__(self):
        # Acquire a distinct iterator of the primary keys within the queryset.
        # This will be maintained in memory (or a temporary table) within the
        # database and iterated over, i.e. we will not copy and store results.
        iterator = self.queryset.values_list('pk', flat=True).distinct().iterator()
        iter_queryset = self.get_iter_queryset()

        # Begin main logic loop. Will loop until iterator is exhausted.
        while True:
            pk_buffer = []
            try:
                # Consume queryset iterator until batch is reached or the
                # iterator has been exhausted.
                while len(pk_buffer) < self.batch_size:
                    pk_buffer.append(next(iterator))
            except StopIteration:
                # Break out of the loop once the queryset has been consumed.
                break
            finally:
                # Use the original queryset to obtain the proper results.
                # Once again using an iterator to keep memory footprint low.
                qs_chunk = iter_queryset.filter(pk__in=pk_buffer)
                for result in qs_chunk:
                    yield result

                # Delink results cache
                qs_chunk._result_cache = None

            # minimize memory footprints
            gc.collect()


def batched_queryset_iterator(queryset, batch_size=None, iter_queryset=None):
    return BatchQuerySetIterator(queryset, batch_size=batch_size, iter_queryset=iter_queryset)
