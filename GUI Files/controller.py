class Controller:
    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view

    def upload(self, _filename, _filepath):
        self.model.filename = _filename
        self.model.filepath = _filepath

        self.model.initiate_upload()
