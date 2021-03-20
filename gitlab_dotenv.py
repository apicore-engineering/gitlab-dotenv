'''Gitlab CI variable manager'''
from copy import deepcopy
from gitlab_dotenv_api import GitlabDotenvAPI
from gitlab_variable import GitlabVariable

class GitlabDotenv:
    '''Gitlab CI variable manager'''
    def __init__(self, url, token):
        self.api = GitlabDotenvAPI(url, token)
        self.data = {}
        self.api_data = {}
        self._pull()

    def all(self):
        '''Get every variable'''
        return self.data.values()

    def created(self):
        '''Get variables not present on the API'''
        return [v for k, v in self.data.items() if k not in self.api_data]

    def deleted(self):
        '''Get variables present on the API but not locally'''
        return [v for k, v in self.api_data.items() if k not in self.data]

    def changed(self):
        '''Get variables that are changed compared to the API'''
        return [v for k, v in self.data.items() if k in self.api_data and v != self.api_data[k]]

    def _pull(self):
        self.api_data = {v.uid: v for v in [GitlabVariable(d) for d in self.api.get_all()]}

    def _push_created(self):
        for var in self.created():
            print("Create: " + str(var))
            self.api.create(var.data)

    def _push_changed(self):
        for var in self.changed():
            print("Update: " + str(var))
            self.api.update(var.data["key"], var.data, var.data["environment_scope"])

    def _push_deleted(self):
        for var in self.deleted():
            print("Delete: " + str(var))
            self.api.delete(var.data["key"], var.data["environment_scope"])

    def pull(self, fresh=False):
        '''Update local data from the API'''
        if fresh is True:
            self._pull()
        self.data = {k: deepcopy(v) for k, v in self.api_data.items()}

    def push(self, allow_create=True, allow_update=False, allow_delete=False):
        '''Push local changes to API'''
        if allow_create is True:
            self._push_created()
        if allow_update is True:
            self._push_changed()
        if allow_delete is True:
            self._push_deleted()

    def add(self, var: GitlabVariable):
        '''Add new variable to collection'''
        self.data[var.uid] = var

    def remove(self, var: GitlabVariable):
        '''Remove variable from collection'''
        if var.uid in self.data:
            self.data.pop(var.uid)
