from django.contrib import admin
from .models import *
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'image')  # Columns shown in the list
    search_fields = ('number',)  # Enable search

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'section')
    search_fields = ('number',)
    list_filter = ('section',)  # Filter by section

class SubChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'chapter')  # Show ID, Number, and Chapter
    search_fields = ('number',)  #  Allow searching by number
    list_filter = ('chapter',)  #  Filter by

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'hs_code', 'is_active', 'sub_chapter')
    list_filter = ('is_active',)  # Add filter in Django Admin


class SectionTranslationAdmin(admin.ModelAdmin):
    list_display = ('section', 'language', 'title')
    list_filter = ('language', 'section')

class ChapterTranslationAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'language', 'title','chapter',)
    list_filter = ('language', 'chapter')

class SubChapterTranslationAdmin(admin.ModelAdmin):
    list_display = ('sub_chapter', 'language', 'title',)
    list_filter = ('language', 'sub_chapter')

class ItemTranslationAdmin(admin.ModelAdmin):
    list_display = ('item', 'language', 'title')
    list_filter = ('language', 'item')

class AdditionalConditionsAdmin(admin.ModelAdmin):
    list_display = ('item', 'language', 'title')
    list_filter = ('language', 'item')

# ==================== New Models (Export, Import, ExpensesFee) ==================== #

class ExportAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'is_active')
    search_fields = ('value',)
    list_filter = ('is_active',)

class ImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'is_active')
    search_fields = ('value',)
    list_filter = ('is_active',)

class ExpensesFeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'import_fee', 'export_fee', 'full_import_fee', 'full_export_fee')
    search_fields = ('import_fee', 'export_fee')  # Allow searching by import/export fee


# Register with custom admin options
admin.site.register(Section, SectionAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(SubChapter,SubChapterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SectionTranslation,SectionTranslationAdmin)
admin.site.register(ChapterTranslation,ChapterTranslationAdmin)
admin.site.register(SubChapterTranslation,SubChapterTranslationAdmin)
admin.site.register(ItemTranslation,ItemTranslationAdmin)
admin.site.register(AdditionalConditions,AdditionalConditionsAdmin)
admin.site.register(Export, ExportAdmin)
admin.site.register(Import, ImportAdmin)
admin.site.register(ExpensesFee, ExpensesFeeAdmin)