from django.contrib import admin
from . import models


# Register your models here.
# admin.site.register(models.Fees)
class ExtraInline(admin.TabularInline):

    min_num = 1
    max_num = 20
    model = models.Extra
    extra = 0


@admin.register(models.Fees)
class FeesAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['id', 'label', 'price','decision', 'fees_group_labels', 'extra_labels', 'placeholder']
    list_editable = ['label','price','decision']

    def fees_group_labels(self, obj):
        return ", ".join([group.label for group in obj.feesGroup.all()])
    fees_group_labels.short_description = "Fees groups"

    def extra_labels(self, obj):
        return ", ".join([extra.label or "N/A" for extra in obj.extras.all()])
    extra_labels.short_description = "Extra labels"

    inlines = [ExtraInline]

@admin.register(models.FeesGroup)
class FeesGroupAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label']

@admin.register(models.CountryGroup)
class CountryGroupAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label','id', ]

@admin.register(models.Export_Price)
class Export_PriceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name','fees_id']
    autocomplete_fields = ['fees_id']

@admin.register(models.Port)
class PortAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name','countries_code','port_code', ]



@admin.register(models.Origin)
class OriginAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['id', 'label', 'label_ar', 'ImageURL', 'countries_code', 'country_groups']
    list_editable = ['label_ar','label']

    def country_groups(self, obj):
        return ", ".join([group.label for group in obj.countryGroups.all()])

    country_groups.short_description = 'Country Groups'

@admin.register(models.Taxes)
class TaxesAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label','id', 'price']


@admin.register(models.Dolar)
class DolartaxesAdmin(admin.ModelAdmin):
    list_display = ['price']


@admin.register(models.Atom)
class AtomAdmin(admin.ModelAdmin):
    list_display = ['categories','price']
