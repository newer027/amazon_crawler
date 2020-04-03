# The following code is tested on Django 1.7
import django
import sys
import logging

from django.apps import apps
from django.db.migrations.recorder import MigrationRecorder
from django.core.serializers import sort_dependencies


LOG_FORMAT = '%(asctime)s|%(levelname)s|%(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def copy(model):
    table_name = model._meta.db_table
    logger.info('Start import %s into new_db' % table_name)

    table_objects = model.objects.all()
    for t in table_objects:
        t.save(using='new_db')

    logger.info('Successfuly imported %s into new_db' % table_name)

'''
Please note that the id for many to many objects might be diffrent from source table.
This is because id is not specified in the add method.
'''
def copy_m2m(model, m2m_field):
    table_name = m2m_field.rel.through._meta.db_table
    field_name = m2m_field.name
    to_model = m2m_field.rel.to
    pk_name = model._meta.pk.name
    child_pk_name = to_model._meta.pk.name

    logger.info('Start import %s into new_db' % table_name)

    for o in model.objects.all():
        pk_value = getattr(o, pk_name)
        new_o = model.objects.using('new_db').get(**{pk_name: pk_value})
        for child in getattr(o, field_name).all():
            child_pk_value = getattr(child, child_pk_name)
            new_child = to_model.objects.using('new_db').get(**{child_pk_name: child_pk_value})
            getattr(new_o, field_name).add(new_child)

    logger.info('Successfuly imported %s into new_db' % table_name)


def run():
    logger.info('Start move data into new_db')

    app_configs = apps.get_app_configs()
    app_list = [(a, None) for a in app_configs]
    models = sort_dependencies(app_list)
    models_with_m2m = []

    for m in models:
        copy(m)
        if m._meta.many_to_many:
            models_with_m2m.append(m)

    # Migration model needs to copy separately as it is not in the INSTALLED_APPS
    copy(MigrationRecorder.Migration)

    # re-create object in ManyToManyField
    for m in models_with_m2m:
        for field in m._meta.many_to_many:
            # data for field that has specific through model should have been copied in earlier steps
            if field.rel.through._meta.auto_created:
                copy_m2m(m, field)

    logger.info('Successfully moved data into new_db')
