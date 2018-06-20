from admin_export.exporter import getExporter
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import lookup_field, display_for_value, display_for_field, label_for_field
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import JsonResponse, Http404, HttpResponseNotAllowed
from django.urls import path
from django.utils.safestring import mark_safe
from django.views import View

from .urls import urlpatterns


def result_headers(cl):
    displays = []

    for i, field_name in enumerate(cl.list_display):
        if field_name == 'action_checkbox':
            continue

        text, attr = label_for_field(
            field_name, cl.model,
            model_admin=cl.model_admin,
            return_attr=True
        )

        displays.append(text)

    return displays


def items_for_result(cl, item):
    results = []

    for field_index, field_name in enumerate(cl.list_display):
        if field_name == 'action_checkbox':
            continue

        empty_value_display = cl.model_admin.get_empty_value_display()

        try:
            f, attr, value = lookup_field(field_name, item, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(attr, 'empty_value_display', empty_value_display)
            if f is None or f.auto_created:
                boolean = getattr(attr, 'boolean', False)
                result_repr = display_for_value(value, empty_value_display, boolean)
            else:
                if isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(item, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    result_repr = display_for_field(value, f, empty_value_display)

        results.append(result_repr)

    return results


def view_wrapper(model, admin_cls, file_type):
    if not issubclass(admin_cls, ModelAdmin):
        raise AssertionError('admin_export decorator must be used with ModelAdmin')

    class ExportView(View):
        def get(self, request):
            app_label = model._meta.app_label

            if not request.user.has_module_perms(app_label):
                return HttpResponseNotAllowed

            model_admin = admin_cls(model, admin.site)
            cl = model_admin.get_changelist_instance(request)
            cl.formset = None

            headers = result_headers(cl)
            results = [items_for_result(cl, item) for item in cl.result_list]

            file_name = '{}_{}_list'.format(app_label, model._meta.object_name)
            exporter_cls = getExporter(file_type)
            exporter = exporter_cls(file_name, headers, results)
            return exporter.export()

    return ExportView


# ModelAdmin class decorator with parameter Model Class and output file type
def dae_export(model_cls, file_type='xls'):
    def outer(admin_cls):
        # do url register
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.object_name

        urlpatterns.insert(
            0,
            path('{}/{}/export'.format(app_label, model_name), view_wrapper(model_cls, admin_cls, file_type).as_view())
        )

        class wrapper(admin_cls):
            change_list_template = 'admin_export/admin/change_list.html'

        return wrapper

    return outer
