from import_export.widgets import ForeignKeyWidget


class NullableForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value):
        return self.model.objects.filter(name=value).first()
