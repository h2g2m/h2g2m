class Container:
    def __init__(self):
        self.providers = {}

    def provide(self, feature, provider, *args, **kwargs):
        assert not self.providers.has_key(feature), "Duplicate feature: %r" % feature
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        self.providers[feature] = call

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError, "Unknown feature named %r" % feature
        return provider()
