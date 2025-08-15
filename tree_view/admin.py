from django.contrib import admin
from . import models
from .forms import NoArrowInp
from django.shortcuts import render
from django.urls import path  # ✅ Import path for URL routing

# from .forms import HsCodeForm  # ✅ Import the form
from .models import ExportFee,Stone_Farming,Commercial_Description, Image_Description, Chapter, Fee, ImportFee, Notes_chapter, Notes_fee, Notes_section, Notes_subchapter, Section, Sub_Chapter
from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import Fee, Finance, ImportFee, ExportFee, Stone_Farming, HsCode
from django.templatetags.static import static
from django.utils.html import format_html
from .resources import HSCodeResource
from import_export.admin import ImportExportModelAdmin  # ✅ Add this import

# Register your models here.



@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ['label', 'id']
    list_display = ['id', 'label', 'label_en', 'name','name_en', 'image', 'start', 'end']

@admin.register(models.Finance)
class FinanceAdmin(admin.ModelAdmin):
    search_fields = [ 'id', 'id_finance__id']
    list_display = ['id', 'id_finance']



class SubChapterInline(admin.TabularInline):
    min_num = 1
    max_num = 50
    model = Sub_Chapter
    extra = 0
class FeeInline(admin.TabularInline):
    min_num = 1
    max_num = 50
    model = Fee
    extra = 0


class FinanceInline(admin.StackedInline):
    model = Finance
    min_num = 1
    max_num = 50
    extra = 0
class ImportFeeInline(admin.StackedInline):
    model = ImportFee
    min_num = 1
    max_num = 50
    extra = 0

class ExportFeeInline(admin.StackedInline):
    model = ExportFee
    min_num = 1
    max_num = 50
    extra = 0


class StoneFarmingInline(admin.StackedInline):
    model = Stone_Farming
    min_num = 1
    max_num = 50  
    extra = 0

class NotesFeeInline(admin.StackedInline):
    min_num = 1
    max_num = 50
    model = Notes_fee
    extra = 0
    

@admin.register(models.Fee)
class FeeAdmin(admin.ModelAdmin):
    search_fields = ['label', 'id']
    list_display = ['id', 'label', 'id_parent_3']
    list_editable=['label']
    # inlines = [FinanceInline, ImportFeeInline, ExportFeeInline, StoneFarmingInline]

@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    search_fields = ['label', 'id']
    list_display = ['id', 'label', 'id_parent_1']
    inlines =[SubChapterInline]


@admin.register(models.Sub_Chapter)
class Sub_ChapterAdmin(admin.ModelAdmin):
    search_fields = ['label', 'id']
    list_display = ['id', 'label', 'id_parent_2', 'review']
    inlines = [FeeInline]

@admin.register(models.ExportFee)
class ExportFeeAdmin(admin.ModelAdmin):
    search_fields = ['id_exportfee__id','export', 'restriction_export','export_en','restriction_export_en']
    list_display = ['id_exportfee','export', 'restriction_export','export_en','restriction_export_en']
    list_editable = ['export', 'restriction_export','export_en','restriction_export_en']


@admin.register(models.ImportFee)
class ImportFeeAdmin(admin.ModelAdmin):
    search_fields = ['id', 'id_importfee__id', 'restriction_import_en', 'document_import_en',]
    list_display = ['id', 'id_importfee', 'restriction_import', 'document_import', 'restriction_import_en', 'document_import_en','import_allowed']
    autocomplete_fields = ['id_importfee']

    

@admin.register(models.Notes_section)
class Notes_sectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_section', 'note_a', 'note_b', 'note_c')
    search_fields = ('id', 'id_section__name', 'note_a', 'note_b', 'note_c')
    autocomplete_fields = ['id_section']


@admin.register(models.Notes_chapter)
class Notes_chapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_chapter', 'note_a', 'note_b', 'note_c', 'note_d', 'note_e')
    search_fields = ('id', 'id_chapter__name', 'note_a', 'note_b', 'note_c', 'note_d', 'note_e')
    autocomplete_fields = ['id_chapter']

@admin.register(models.Notes_subchapter)
class Notes_subchapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_subchapter', 'note_a',   'additional_note', 'name_a' , 'name_addition')
    search_fields = ('id', 'id_subchapter__name', 'note_a', 'additional_note', 'name_a' , 'name_addition')
    autocomplete_fields = ['id_subchapter']

@admin.register(models.Notes_fee)
class Notes_feeAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_fee', 'note_a', 'note_b', 'additional_note')
    search_fields = ('id', 'note_a', 'note_b' ,'additional_note')
    autocomplete_fields = ['id_fee']


@admin.register(Commercial_Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_desc', 'second_description')
    search_fields = ('id', 'id_desc__id', 'second_description')
    autocomplete_fields = ['id_desc']


@admin.register(models.Image_Description)
class Image_DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_desc', 'image')
    search_fields = ('id', 'id_desc__name', 'image')
    autocomplete_fields = ['id_desc']


@admin.register(models.Stone_Farming)
class Stone_FarmingAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_stone', 'ston_import', 'ston_import_notes', 'ston_export', 'ston_export_notes')
    search_field = ('id', 'id_stone__name', 'ston_import', 'ston_import_notes', 'ston_export', 'ston_export_notes')
    autocomplete_fields = ['id_stone']

    
@admin.register(HsCode)
class HsCodeAdmin(ImportExportModelAdmin):  # ✅ Inherit from ImportExportModelAdmin
    resource_class = HSCodeResource  # ✅ Connect your custom resource

    form = NoArrowInp 
    list_display = ('edit_link', 'parent_3', 'item', 'label', 'import_fee', 'ser_all', 'export_fee', 'FIFee', 'exp_ser_Fe', 'type', 'active', 'checking', 'new', 'test')
    search_fields = ('hs_code', 'label',)
    list_filter = ('id_parent_3', )
    ordering = ('hs_code',)
    list_editable = ('import_fee','type','ser_all','active','checking','new','exp_ser_Fe','export_fee','test')
    readonly_fields = ('review','review_en','review_value')
    inlines = [ImportFeeInline, ExportFeeInline, StoneFarmingInline, FinanceInline]
    list_per_page = 7

    def get_row_css_class(self, obj, index):
        return "row-checking-true" if obj.checking else ""
    
    def save_model(self, request, obj, form, change):
        for field in form.cleaned_data:
            value = form.cleaned_data.get(field)
            if value in [None, '']:
                setattr(obj, field, None)
        super().save_model(request, obj, form, change)
    def full_import_fee(self, obj):
        return obj.full_import_fee

    full_import_fee.short_description = "Full Import Fee"

    def item(self, HSCode):
        return HSCode.hs_code

    def SER_All(self, HSCode):
        return HSCode.ser_all

    def FIFee(self, HSCode):
        return HSCode.full_import_fee
    
    def get_related_stone_farming(self, obj):
        return ", ".join([str(stone) for stone in obj.stonefarms.all()])

    get_related_stone_farming.short_description = "Related Stone Farming"

    def parent_3(self, obj):
        return obj.id_parent_3

    class Media:
        css = {
            'all': (static('/admin/css/custom_admin.css'),)
        }
        js = (static('/admin/js/custom_admin.js'),)
        
    def edit_link(self, obj):
        edit_url = f"/admin/tree_view/hscode/{obj.id}/change/"
        return format_html(
            '<a href="{}" class="edit-pen" title="Edit">'
            '<img src="/static/admin/img/icon-changelink.svg" width="18" height="18"></a>',
            edit_url
        )

    edit_link.short_description = "Edit"