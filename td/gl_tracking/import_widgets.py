from import_export.widgets import ForeignKeyWidget


class NullableForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value):
        super(ForeignKeyWidget, self).clean(value)
        return self.model.objects.filter(name=value).first()
