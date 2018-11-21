class Serializable:
    def _populate(self, source):
        for prop in source:
            setattr(self, prop, source[prop])