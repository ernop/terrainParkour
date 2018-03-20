from django.contrib import admin
from django.forms.models import BaseModelFormSet
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.views.main import SuspiciousOperation, ImproperlyConfigured, IncorrectLookupParameters
from django.db.models import Q, Count

from django.conf import settings
from pytz import timezone as pytz_timezone

def construct_querystring_without_field(request, field):
    q = request.GET.copy()
    del q[field]
    return q

def make_untoggle_link(request, field):
    qs = construct_querystring_without_field(request, field)
    newqs = qs.urlencode()
    return '<a href=%s?%s>X</a>' % (request.path, newqs)

class OverriddenModelAdmin(admin.ModelAdmin):
    """normal, except overrides some widgets."""
    formfield_overrides = {
    }

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    created_tz.admin_order_field='created'

    def updated_tz(self, obj):
        dt = obj.updated.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    updated_tz.admin_order_field='updated'

    def changelist_view(self, request, extra_context=None):
        '''rewriting this to sometimes kill the "ID" filter when you click on another one.'''
        if request.GET.get('id'):
            #delete id parameter if there are other filters! yes!
            real_keys = [k for k in request.GET.keys() if k not in getattr(self, 'not_count_filters', [])]
            if len(real_keys) != 1:
                q = request.GET.copy()
                del q['id']
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
        if request.method == 'GET':
            '''re-create a changelist, get the filter specs, and put them into the
            request somewhere to be picked up by a future edit to the change list template,
            which would allow them to be displayed for all normal changelist_view pages'''
            #this is so that I can display filters on the top of the page for easy cancelling them.

            if request.GET.get('_changelist_filters'):
                qq = request.GET.copy()
                del qq['_changelist_filters']
                log.info('killed extraneous weird filter thingie which would have caused a 500 error.')
                request.GET = qq

            ChangeList = self.get_changelist(request)
            list_display = self.get_list_display(request)
            list_display_links = self.get_list_display_links(request, list_display)
            from django.contrib.admin import options
            list_filter = self.get_list_filter(request)
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
            used_filters = [xx for xx in cl.filter_specs if xx.used_parameters]
            filter_descriptions = []
            from django.contrib.admin.filters import BooleanFieldListFilter
            if 'id' in request.GET:
                desc = ('id', request.GET['id'], make_untoggle_link(request, 'id'))
                filter_descriptions.append(desc)
            for key in request.GET.keys():
                if key.endswith('__id'):
                    desc = ('%s id' % key.split('__')[0], request.GET[key], make_untoggle_link(request, key))
                    filter_descriptions.append(desc)
            for uf in used_filters:
                if type(uf) == BooleanFieldListFilter:
                    current_val = bool(int(uf.used_parameters.values()[0]))
                    if current_val:
                        desc = (uf.title, current_val, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                    else:
                        desc = (uf.title, current_val, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                    filter_descriptions.append(desc)
                else:
                    try:
                        current_val = uf.used_parameters.values()[0]
                        choice = None
                        if getattr(uf, 'lookup_choices', False):
                            got = False
                            #looking up the "descriptive" way to describe the value.
                            for choice in uf.lookup_choices:
                                if choice[0] == current_val:
                                    choice = choice[1]
                                    break
                                try:
                                    int(current_val)
                                    if choice[0] == int(current_val):
                                        choice = choice[1]
                                        break
                                except ValueError:
                                    pass
                                try:
                                    float(current_val)
                                    if choice[0] == float(current_val):
                                        choice = choice[1]
                                        break
                                except ValueError:
                                    pass
                            if not choice:
                               pass
                        else:
                            choice = uf.used_parameters.keys()[0]
                            choice = current_val
                        desc = (uf.title, choice, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                        filter_descriptions.append(desc)
                    except Exception as e:
                        pass
            if request.GET and 'q' in request.GET:
                desc = ('Searching for', "\"%s\"" % request.GET['q'], make_untoggle_link(request, 'q'))
                filter_descriptions.append(desc)
            request.filter_descriptions = filter_descriptions
        sup=super(OverriddenModelAdmin,self)
        return sup.changelist_view(request, extra_context=extra_context)

def adminify(*args):
    for func in args:
        name=None
        if not name:
            if func.__name__.startswith('my'):
                name=func.__name__[2:]
            else:
                name=func.__name__
            name = name.replace('_', ' ')
        func.allow_tags=True
        func.short_description=name


def make_null_filter(field, title=None, param_name=None, include_empty_string=True):
    if not title:
        title = 'null filter for %s' % field
    if not param_name:
        param_name = 'has_'+''.join([c for c in field if c.isalpha()])
    '''rather than making a whole class for these, just make them on the fly...'''
    bb = title
    if include_empty_string:
        use_klass = BaseNullEmptyFilter
    else:
        use_klass = BaseNullFilter

    class InnerFilter(use_klass):
        title= bb
        parameter_name= param_name
        args={field:None}

    return InnerFilter

class BaseNullEmptyFilter(SimpleListFilter):
    '''an easy way to construct filters that are like __isnull'''
    def lookups(self, request, model_admin):
        return (
            ('null', 'null'),
            ('not null', 'not null'),
        )
    def queryset(self, request, queryset):
        sargs=self.args
        if self.value()=='not null':
            for k in self.args.keys():
                queryset = queryset.exclude(**{k: '',})
                queryset = queryset.exclude(**{k: None,})
            return queryset
        if self.value()=='null':
            for k in self.args.keys():
                queryset = queryset.filter(**{k: '',}) | queryset.filter(**{k: None,})
            return queryset

class BaseNullFilter(SimpleListFilter):
    '''an easy way to construct filters that are like __isnull'''
    def lookups(self, request, model_admin):
        return (
            ('null', 'null'),
            ('not null', 'not null'),
        )
    def queryset(self, request, queryset):
        sargs=self.args
        if self.value()=='null':
            return queryset.filter(**self.args)
        if self.value()=='not null':
            return queryset.exclude(**self.args)
