from django.db import models
from Fee_calculator.models import Fees

# Create your models here.

class Section(models.Model):
    number = models.IntegerField(default=77)
    id = models.CharField( primary_key=True,max_length=10)
    label = models.CharField(max_length=512, null=True)
    label_en = models.CharField(max_length=512, null=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    image = models.FileField(upload_to='media/fees/images',null=True)
    start = models.CharField(max_length=8, null=True)
    end = models.CharField(max_length=8, null=True)
    is_have_note = models.BooleanField(max_length=512, null=True, blank=True)
    def __str__(self):
        return f"Section {self.number}"

class Chapter(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    label = models.CharField(max_length=926, null=True)
    label_en = models.CharField(max_length=926, null=True)
    id_parent_1 = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    is_have_note = models.BooleanField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.id

class Sub_Chapter(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    label = models.CharField(max_length=926, null=True)
    label_en = models.CharField(max_length=926, null=True)
    review = models.CharField(max_length=512, null=True, blank=True)
    review_en = models.CharField(max_length=512, null=True, blank=True)
    id_parent_2 = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    review_value = models.CharField(max_length=2, null=True, blank=True)
    def __str__(self):
        return self.id

class HsCode(models.Model):
    UNIT_CHOICES = [
        ('number', 'Number'),
        ('weight', 'Weight'),
    ]
    active=models.BooleanField(default=True, blank=True)
    checking=models.BooleanField(default=True, blank=True)
    new=models.BooleanField(default=False, blank=True)
    hs_code= models.CharField(max_length=50,verbose_name='Band')
    id_parent_3 = models.ForeignKey(Sub_Chapter, on_delete=models.CASCADE, null=True,blank=True)
    image = models.FileField(upload_to='media/items/image',null=True,blank=True)
    label = models.CharField(max_length=926, null=True,verbose_name='Name')
    label_en = models.CharField(max_length=926, null=True)
    review = models.CharField(max_length=512, null=True, blank=True)
    review_en= models.CharField(max_length=512, null=True, blank=True)
    review_value = models.CharField(max_length=2, null=True, blank=True)
    import_fee = models.FloatField(null=True, blank=True, verbose_name='Price Import')  
    export_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Clearance Fee Export' ) 
    ser_all = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='Clearance Fee')  # ✅ Numbers only
    full_import_fee=models.CharField(max_length=926, null=True,blank=True,verbose_name='Price Full')
    exp_ser_Fe= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='Price Export')
    type=models.CharField(max_length=926, null=True, blank=True)

    test= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='number',  # Default value set to "number"
    )   
    @property
    def full_import_fee(self):
        """Ensure numeric addition, not string concatenation."""
        return (float(self.import_fee) if self.import_fee else 0) + (float(self.ser_all) if self.ser_all else 0)
    def __str__(self) -> str:
        return self.label

    def get_stone_farming(self):
        try:
            return Stone_Farming.objects.get(id_stone=self.id)
        except Stone_Farming.DoesNotExist:
            return None
    def get_ExportFee(self):
        try:
            return ExportFee.objects.get(id_exportfee=self.id)
        except ExportFee.DoesNotExist:
            return None
    def get_ImportFee(self):
        try:
            return ImportFee.objects.get(id_importfee=self.id)
        except ImportFee.DoesNotExist:
            return None
    def get_Finance(self):
        try:
            return Finance.objects.get(id_finance=self.id)
        except Finance.DoesNotExist:
            return None
    def get_Commercial_Description(self):
        try:
            return Commercial_Description.objects.get(id_desc=self.id)
        except Commercial_Description.DoesNotExist:
            return None

    def get_Fees(self):
        try:
            return Fees.objects.get(id=self.id)
        except Fees.DoesNotExist:
            return None
  
    class Meta:
        ordering = ['hs_code', 'id_parent_3']  # Ensures parent_3 appears right after hs_code in queries

    def __str__(self):
        return self.hs_code

class Stone_Farming(models.Model):
    id_stone = models.ForeignKey(
        "HsCode",
  # Explicitly reference hs_code instead of id
        on_delete=models.CASCADE,
        null=True,
        related_name='stonefarms'
    )
    # id_stone = models.ForeignKey('HsCode', on_delete=models.CASCADE, null=True, related_name='stonefarms')
    ston_import = models.TextField(null=True, blank=True)
    ston_import_notes = models.TextField(null=True, blank=True)
    ston_export = models.TextField(null=True, blank=True)
    ston_export_notes = models.TextField(null=True, blank=True)
    ston_import_en = models.TextField(null=True, blank=True)
    ston_import_notes_en = models.TextField(null=True, blank=True)
    ston_export_en = models.TextField(null=True, blank=True)
    ston_export_notes_en = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.id_stone)

class ExportFee(models.Model):
    id_exportfee = models.ForeignKey(
        "HsCode",
       # to_field='hs_code',  # Explicitly reference hs_code instead of id
        on_delete=models.CASCADE,
        null=True,
        related_name='exportfees'
    )
    export_allowed=models.BooleanField(default=True, null=False, blank=True)
    export = models.CharField(max_length=1024, null=True, blank=True)
    restriction_export = models.CharField(max_length=1024,null=True, blank=True)
    export_en = models.CharField(max_length=512, null=True, blank=True)
    restriction_export_en = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        verbose_name_plural = "ExportAll"

    def __str__(self):
        return str(self.id_exportfee)

class Finance(models.Model):
    id_finance = models.ForeignKey('HsCode',  on_delete=models.CASCADE, null=True,  related_name='financefees')
    finance = models.TextField(null=True, blank=True)
    finance_en = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return str(self.id_finance)

class Commercial_Description(models.Model):
    id = models.CharField(max_length=8, unique=False, primary_key=True)
    id_desc =models.ForeignKey('HsCode',  on_delete=models.CASCADE, null=True)
    second_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.id

class Fee(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    label = models.CharField(max_length=926, null=True)
    label_en = models.CharField(max_length=926, null=True)
    id_parent_3 = models.ForeignKey(Sub_Chapter, on_delete=models.CASCADE, null=True)
    review = models.CharField(max_length=512, default="Nill", blank=True)
    review_en= models.CharField(max_length=512, default="Nill", blank=True)
    review_value = models.CharField(max_length=2, default="Nill", blank=True)

    def __str__(self) -> str:
        return self.label

    def get_stone_farming(self):
        try:
            return Stone_Farming.objects.get(id_stone=self.id)
        except Stone_Farming.DoesNotExist:
            return None
    def get_ExportFee(self):
        try:
            return ExportFee.objects.get(id_exportfee=self.id)
        except ExportFee.DoesNotExist:
            return None
    def get_ImportFee(self):
        try:
            return ImportFee.objects.get(id_importfee=self.id)
        except ImportFee.DoesNotExist:
            return None
    def get_Finance(self):
        try:
            return Finance.objects.get(id_finance=self.id)
        except Finance.DoesNotExist:
            return None
    def get_Commercial_Description(self):
        try:
            return Commercial_Description.objects.get(id_desc=self.id)
        except Commercial_Description.DoesNotExist:
            return None

    def get_Fees(self):
        try:
            return Fees.objects.get(id=self.id)
        except Fees.DoesNotExist:
            return None

class ImportFee(models.Model):
    id_importfee = models.ForeignKey(HsCode,
    on_delete=models.CASCADE,
    null=True, 
    related_name='importfees')
    import_allowed=models.BooleanField(default=True, null=False, blank=True)
    restriction_import = models.TextField(max_length=512, null=True, blank=True)
    document_import = models.CharField(max_length=512, null=True, blank=True)
    restriction_import_en = models.TextField(max_length=512, null=True, blank=True)
    document_import_en = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name_plural = "ImportAll"

    def __str__(self):
        return str(self.id_importfee)

class Notes_section(models.Model):
    id = models.CharField(max_length=8, unique=False, primary_key=True)
    id_section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    note_a = models.TextField(null=True, blank=True)
    note_b = models.TextField(null=True, blank=True)
    note_c = models.TextField(null=True, blank=True)
    note_num = models.CharField(max_length=35, null=True)
    note_a_en = models.TextField(null=True, blank=True)
    note_b_en = models.TextField(null=True, blank=True)
    note_c_en = models.TextField(null=True, blank=True)
    note_num_en = models.CharField(max_length=35, null=True)

    def __str__(self):
        return str(self.id_section)

class Notes_chapter(models.Model):
    id = models.IntegerField(primary_key=True)
    id_chapter =models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    note_a = models.TextField(null=True, blank=True)
    note_b = models.TextField(null=True, blank=True)
    note_c = models.TextField(null=True, blank=True)
    note_d = models.TextField(null=True, blank=True)
    note_e = models.TextField(null=True, blank=True)
    note_num = models.CharField(max_length=35, null=True)
    note_a_en = models.TextField(null=True, blank=True)
    note_b_en = models.TextField(null=True, blank=True)
    note_c_en = models.TextField(null=True, blank=True)
    note_d_en = models.TextField(null=True, blank=True)
    note_e_en = models.TextField(null=True, blank=True)
    note_num_en = models.CharField(max_length=35, null=True)


    def __str__(self):
        return str(self.id_chapter)

class Notes_subchapter(models.Model):
    id = models.CharField(max_length=8, unique=False, primary_key=True)
    id_subchapter =models.ForeignKey(Sub_Chapter, on_delete=models.CASCADE, null=True)
    note_a = models.TextField(blank=True, null=True)
    additional_note = models.TextField(blank=True, null=True)
    name_a = models.TextField(blank=True, null=True)
    name_addition = models.TextField(blank=True, null=True)
    note_a_en = models.TextField(blank=True, null=True)
    additional_note_en = models.TextField(blank=True, null=True)
    name_a_en = models.TextField(blank=True, null=True)
    name_addition_en = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id

class Notes_fee(models.Model):
    id = models.CharField(max_length=8, unique=False, primary_key=True)
    id_fee =models.ForeignKey("HsCode",  on_delete=models.CASCADE, null=True)
    note_a = models.TextField(null=True, blank=True)
    note_b = models.TextField(null=True, blank=True)
    additional_note = models.TextField(null=True, blank=True)
    name_a = models.TextField(blank=True, null=True)
    name_b = models.TextField(blank=True, null=True)
    name_addition = models.TextField(blank=True, null=True)
    note_a_en = models.TextField(null=True, blank=True)
    note_b_en = models.TextField(null=True, blank=True)
    additional_note_en = models.TextField(null=True, blank=True)
    name_a_en = models.TextField(blank=True, null=True)
    name_b_en = models.TextField(blank=True, null=True)
    name_addition_en = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id

class Image_Description(models.Model):
    id = models.CharField(max_length=8, unique=False, primary_key=True)
    id_desc =models.ForeignKey("HsCode", on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to='media/fees/images_desc',null=True)


    def __str__(self):
        return self.id
