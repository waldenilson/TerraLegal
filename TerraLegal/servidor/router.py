#Created on 30/08/2013 @author: eduardo
class GeneRouter(object):
    """A router to control all database operations on models in
    the genes application"""

    def db_for_read(self, model, **hints):
        "Point all operations on genes models to 'genes'"
        if model._meta.app_label == 'servidor':
            return 'dbControle'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on genes models to 'genes'"
        if model._meta.app_label == 'servidor':
            return 'dbControle'
        return None

    def allow_syncdb(self, db, model):
        "Make sure the genes app only appears on the 'genes' db"
        if model._meta.app_label in ['south']:
            return True
        if db == 'dbControle':
            return model._meta.app_label == 'servidor'
        elif model._meta.app_label == 'servidor':
            return False
        return None