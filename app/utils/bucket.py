class BucketSingleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BucketSingleton, cls).__new__(
                cls, *args, **kwargs)
        cls._instance.x = 10
        return cls._instance
