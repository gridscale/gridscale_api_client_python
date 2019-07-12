class ApiRegistry:
    _index = {}

    def register(self, name, api_class):
        self._index[name] = api_class        

    def get(self, name):
        return self._index[name]

    def __iter__(self):
        for name, api_class in self._index.items():
            yield name, api_class
