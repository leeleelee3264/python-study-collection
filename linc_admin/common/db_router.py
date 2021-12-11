class BaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'qliq':
            return 'qliq'
        elif model._meta.app_label == 'ncs':
            return 'ncs'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'qliq':
            return 'qliq'
        elif model._meta.app_label == 'ncs':
            return 'ncs'
        return None
