from django.db import models

# ====================== MAIN STRUCTURE ====================== #

class Section(models.Model):
    number = models.CharField(max_length=2, unique=True)
    image = models.ImageField(upload_to='tariffa/section/', blank=True, null=True)
    test = models.CharField(max_length=2, blank=True)
    test2 = models.CharField(max_length=2, blank=True)


    def __str__(self):
        return f"Section {self.number}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

class Chapter(models.Model):
    number = models.CharField(max_length=8, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        return f"Chapter {self.number}"

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

class SubChapter(models.Model):
    number = models.CharField(max_length=8, unique=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='sub_chapters')

    def __str__(self):
        return f"Sub-Chapter {self.number}"

    class Meta:
        verbose_name = "Sub-Chapter"
        verbose_name_plural = "Sub-Chapters"

class Item(models.Model):
    hs_code = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='tariffa/item/', blank=True, null=True)
    unit = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=False)
    sub_chapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"Item {self.hs_code}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

# class HsCode(models.Model):
#     id = models.CharField(max_length=10, primary_key=True)
#     label = models.CharField(max_length=926, null=True)
#     label_en = models.CharField(max_length=926, null=True)
#     id_parent_3 = models.ForeignKey(Sub_Chapter, on_delete=models.CASCADE, null=True)
#     review = models.CharField(max_length=512, null=True, blank=True)
#     review_en= models.CharField(max_length=512, null=True, blank=True)
#     review_value = models.CharField(max_length=2, null=True, blank=True)
#     import_fee =models.CharField(max_length=926, null=True)
#     export_fee =models.CharField(max_length=926, null=True)
#     services_allowance =models.CharField(max_length=926, null=True)
#     full_import_fee=models.CharField(max_length=926, null=True)
#     unit=models.CharField(max_length=926, null=True)
#     def __str__(self) -> str:
#         return self.label

#     def get_stone_farming(self):
#         try:
#             return Stone_Farming.objects.get(id_stone=self.id)
#         except Stone_Farming.DoesNotExist:
#             return None
#     def get_ExportFee(self):
#         try:
#             return ExportFee.objects.get(id_exportfee=self.id)
#         except ExportFee.DoesNotExist:
#             return None
#     def get_ImportFee(self):
#         try:
#             return ImportFee.objects.get(id_importfee=self.id)
#         except ImportFee.DoesNotExist:
#             return None
#     def get_Finance(self):
#         try:
#             return Finance.objects.get(id_finance=self.id)
#         except Finance.DoesNotExist:
#             return None
#     def get_Commercial_Description(self):
#         try:
#             return Commercial_Description.objects.get(id_desc=self.id)
#         except Commercial_Description.DoesNotExist:
#             return None

#     def get_Fees(self):
#         try:
#             return Fees.objects.get(id=self.id)
#         except Fees.DoesNotExist:
#             return None

# ====================== TRANSLATION MODELS ====================== #

class SectionTranslation(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=255,null=True)  # e.g., 'en', 'ar', 'fr'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Section {self.section.number} - {self.language}"

    class Meta:
        unique_together = ('section', 'language')
        verbose_name = "Section Translation"
        verbose_name_plural = "Section Translations"

class ChapterTranslation(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=255,null=True)  # e.g., 'en', 'ar', 'fr'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Chapter {self.chapter.number} - {self.language}"

    class Meta:
        unique_together = ('chapter', 'language')
        verbose_name = "Chapter Translation"
        verbose_name_plural = "Chapter Translations"

class SubChapterTranslation(models.Model):
    sub_chapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=255,null=True)  # e.g., 'en', 'ar', 'fr'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sub-Chapter {self.sub_chapter.number} - {self.language}"

    class Meta:
        unique_together = ('sub_chapter', 'language')
        verbose_name = "Sub-Chapter Translation"
        verbose_name_plural = "Sub-Chapter Translations"

class ItemTranslation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=255,null=True)  # e.g., 'en', 'ar', 'fr'
    title = models.CharField(max_length=255,null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Item {self.item.hs_code} - {self.language}"

    class Meta:
        unique_together = ('item', 'language')
        verbose_name = "Item Translation"
        verbose_name_plural = "Item Translations"

class AdditionalConditions(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255,null=True)  # e.g., 'en', 'ar', 'fr'
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='add_conditions')

    def __str__(self):
        return f"Condition for {self.item.hs_code} - {self.language}"

    class Meta:
        verbose_name = "Additional Condition"
        verbose_name_plural = "Additional Conditions"

# ====================== EXPORT MODELS ====================== #

class Export(models.Model):
    value = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Export {self.value}"

class Import(models.Model):
    value = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Import {self.value}"

class ExpensesFee(models.Model):  # FIXED: Changed `models.Models` to `models.Model`
    import_fee = models.CharField(max_length=255, null=True)
    export_fee = models.CharField(max_length=255, null=True)
    full_import_fee = models.CharField(max_length=255, null=True)
    full_export_fee = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Expenses Fee (Import: {self.import_fee}, Export: {self.export_fee})"
