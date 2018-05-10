class Linq:
    def __init__(self, iterable):
        self.iterable = iterable

    def Select(self, func=lambda x: x):
        return Linq(map(func, self.iterable))

    def Flatten(self):
        def chain(*iterables):
            for it in iterables:
                for element in it:
                    yield element

        def from_iterable(iterables):
            for it in iterables:
                for element in it:
                    yield element

        return Linq(chain(from_iterable(self.iterable)))

    def Where(self, condition):
        def ifilter(predicate, iterable):
            for x in iterable:
                if predicate(x):
                    yield x

        return Linq(ifilter(condition, self.iterable))

    def Take(self, k):
        def islice(iterable, k):
            it = iter(range(k))
            next_i = next(it)
            for i, element in enumerate(iterable):
                if i == next_i:
                    yield element
                    next_i = next(it)

        return Linq(islice(self.iterable, k))

    def GroupBy(self, k):
        class groupby(object):
            def __init__(self, iterable, key):
                self.keyfunc = key
                self.it = iterable
                self.tgtkey = self.currkey = self.currvalue = object()

            def __iter__(self):
                return self

            def __next__(self):
                while self.currkey == self.tgtkey:
                    self.currvalue = next(self.it)  # Exit on StopIteration
                    self.currkey = self.keyfunc(self.currvalue)
                self.tgtkey = self.currkey
                return (self.currkey, self._grouper(self.tgtkey))

            def _grouper(self, tgtkey):
                while self.currkey == tgtkey:
                    yield self.currvalue
                    self.currvalue = next(self.it)  # Exit on StopIteration
                    self.currkey = self.keyfunc(self.currvalue)

        result = dict()
        for key, group in groupby(self.iterable, k):
            result.setdefault(key, list()).append(group)
        return Linq(((key, value) for key, value in result.items()))

    def OrderBy(self, key, reverse=False):
        return Linq(sorted(self.iterable, key=key, reverse=reverse))

    def ToList(self):
        return list(self.iterable)


if __name__ == '__main__':

    def fib():
        i, j = 0, 1
        while True:
            yield i
            i, j = j, i + j


    result = Linq(fib()) \
        .Where(lambda x: x % 3 == 0) \
        .Select(lambda x: x ** 2 if x % 2 == 0 else x) \
        .Take(5) \
        .ToList()
    print(result)

    with open('Реализация LINQ.txt', 'r', encoding='utf-8') as f:
        words = (word for line in f for word in line.split())
        result = Linq(words) \
            .GroupBy(lambda x: x) \
            .OrderBy(lambda x: len(x[1]), reverse=True) \
            .Select(lambda x: (x[0], len(x[1]))) \
            .ToList()
    print(result)

