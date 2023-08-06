import inspect
import logging
from functools import partial

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .handlers import BaseExtraHandler

logger = logging.getLogger(__name__)

IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS

NOTSET = object()


class ActionFailed(Exception):
    pass


def confirm_action(modeladmin, request,
                   action, message,
                   success_message='',
                   description='',
                   pk=None,
                   extra_context=None,
                   template='admin_extra_buttons/confirm.html',
                   error_message=None):
    opts = modeladmin.model._meta
    context = modeladmin.get_common_context(request,
                                            message=message,
                                            description=description,
                                            pk=pk,
                                            **(extra_context or {}))
    if request.method == 'POST':
        ret = None
        try:
            ret = action(request)
            modeladmin.message_user(request, success_message, messages.SUCCESS)
        except Exception as e:
            modeladmin.message_user(request, error_message or str(e), messages.ERROR)

        return ret or HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    return TemplateResponse(request, template, context)


class ExtraUrlConfigException(RuntimeError):
    pass


class DummyAdminform:
    def __init__(self, **kwargs):
        self.prepopulated_fields = []
        self.__dict__.update(**kwargs)

    def __iter__(self):
        yield


class ExtraButtonsMixin:
    """
    Allow to add new 'url' to the standard ModelAdmin
    """
    if IS_GRAPPELLI_INSTALLED:  # pragma: no cover
        change_list_template = 'admin_extra_buttons/grappelli/change_list.html'
        change_form_template = 'admin_extra_buttons/grappelli/change_form.html'
    else:
        change_list_template = 'admin_extra_buttons/change_list.html'
        change_form_template = 'admin_extra_buttons/change_form.html'

    def __init__(self, model, admin_site):
        self.extra_button_handlers = []
        super().__init__(model, admin_site)

    def message_error_to_user(self, request, exception):
        self.message_user(request, f'{exception.__class__.__name__}: {exception}', messages.ERROR)

    @classmethod
    def check(cls, **kwargs):
        from admin_extra_buttons.utils import check_decorator_errors
        errors = []
        errors.extend(check_decorator_errors(cls))
        return errors

    def get_common_context(self, request, pk=None, **kwargs):
        opts = self.model._meta
        app_label = opts.app_label
        self.object = None

        context = {
            **self.admin_site.each_context(request),
            **kwargs,
            'opts': opts,
            'add': False,
            'change': True,
            'save_as': False,
            'extra_buttons': self.extra_button_handlers,
            'has_delete_permission': self.has_delete_permission(request, pk),
            'has_editable_inline_admin_formsets': False,
            'has_view_permission': self.has_view_permission(request, pk),
            'has_change_permission': self.has_change_permission(request, pk),
            'has_add_permission': self.has_add_permission(request),
            'app_label': app_label,
            'adminform': DummyAdminform(model_admin=self),
        }
        context.setdefault('title', '')
        context.update(**kwargs)
        if pk:
            self.object = self.get_object(request, pk)
            context['original'] = self.object
        return context

    def get_urls(self):
        self.extra_button_handlers = []
        extra_urls = {}
        extras = []
        info = self.model._meta.app_label, self.model._meta.model_name
        original = super().get_urls()
        for cls in inspect.getmro(self.__class__):
            for method_name, method in cls.__dict__.items():
                if callable(method) and isinstance(method, BaseExtraHandler):
                    extra_urls[method_name] = method.get_instance()

        for __, handler in extra_urls.items():
            handler.url_name = f'%s_%s_{handler.func.__name__}' % info
            if handler.url_pattern:
                extras.append(path(handler.url_pattern,
                                   partial(getattr(self, handler.func.__name__), self),
                                   name=handler.url_name))
            if hasattr(handler, 'button_class'):
                self.extra_button_handlers.append(handler)
        return extras + original

    def get_changeform_buttons(self, context):
        return [h for h in self.extra_button_handlers if h.change_form in [True, None]]

    def get_changelist_buttons(self, context):
        return [h for h in self.extra_button_handlers if h.change_list in [True, None]]

    def get_action_buttons(self, context):
        return []
