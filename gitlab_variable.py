'''Representation of a Gitlab CI variable'''
class GitlabVariable:
    '''Representation of a Gitlab CI variable'''
    def __init__(self, data):
        self.data = self.default()

        if not isinstance(data, dict):
            return

        for key in self.keys():
            value = data.get(key, self.data[key])
            if isinstance(self.data[key], bool):
                value = value in ("true", "True", "TRUE", True)
            if value is None:
                value = ""
            self.data[key] = value

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.data == other.data

    def __repr__(self):
        return str(self.data)

    @classmethod
    def keys(cls):
        '''Get data keys'''
        return cls.default().keys()

    @classmethod
    def default(cls):
        '''Get default values'''
        return {
            "variable_type": "env_var",
            "key": "",
            "value": "",
            "protected": False,
            "masked": False,
            "raw": False,
            "environment_scope": "*",
            "description": "",
        }

    @property
    def uid(self):
        '''Get unique id'''
        return self.data["environment_scope"] + " // " + self.data["key"]
