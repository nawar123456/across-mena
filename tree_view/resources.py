# resources.py
from import_export import resources, fields
from .models import HsCode

class HSCodeResource(resources.ModelResource):
    hs_code = fields.Field(attribute='hs_code', column_name='band')
    label = fields.Field(attribute='label', column_name='name')
    import_fee = fields.Field(attribute='import_fee', column_name='priceImport')
    ser_all = fields.Field(attribute='ser_all', column_name='clearanceFee')
    fifee = fields.Field(attribute='fifee', column_name='priceFull')
    review_en = fields.Field(attribute='review_en', column_name='material')
    export_fee = fields.Field(attribute='exp_ser_Fe', column_name='clearanceFeeExport')


    class Meta:
        model = HsCode
        import_id_fields = ['hs_code']  # Use this field to uniquely identify records
