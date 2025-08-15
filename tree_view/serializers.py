from rest_framework import serializers
from .models import ExportFee, Finance,Stone_Farming,Commercial_Description, Image_Description, Fee, ImportFee, Notes_chapter, Notes_fee, Notes_section, Notes_subchapter, Section, Chapter, Sub_Chapter
from Fee_calculator.models import Fees, Dolar, Taxes, Extra
from django.db.models import Sum 



class DolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolar
        fields =  '__all__'

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'


class TotalTaxesSerializer(serializers.ModelSerializer):
    total_tax = serializers.SerializerMethodField()
    partial_tax = serializers.SerializerMethodField()
    arabic_stamp = serializers.SerializerMethodField()

    class Meta:
        model = Taxes
        fields = ['total_tax', 'partial_tax', 'arabic_stamp']

    def get_total_tax(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[1, 3, 4, 5, 6])
        total_tax = specific_taxes.aggregate(total_tax=Sum('price'))['total_tax']
        return total_tax

    def get_partial_tax(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[1, 4, 5, 6, 8])
        partial = specific_taxes.aggregate(partial_tax=Sum('price'))['partial_tax']
        return partial

    def get_arabic_stamp(self, obj):
        specific_taxes = Taxes.objects.filter(id__in=[8])
        arabic_stamp = specific_taxes.aggregate(arabic_stamp=Sum('price'))['arabic_stamp']
        return arabic_stamp


class Fees_sari_Serializer(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True)
    dolar = DolarSerializer()
    total_taxes = TotalTaxesSerializer()
    
    class Meta:
        model = Fees
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        label_field = 'label' if lang_header == 'ar' else 'label_en'

        data = super().to_representation(instance)
        data['label'] = data[label_field]
        del data['label_en']  
        return data


class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        label_field = 'label' if lang_header == 'ar' else 'label_en'

        data = super().to_representation(instance)
        data['label'] = data[label_field]
        del data['label_en']  
        return data

class SectionSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Section
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        label_field = 'label' if lang_header == 'ar' else 'label_en'
        name_field = 'name' if lang_header == 'ar' else 'name_en'

        data = super().to_representation(instance)
        data['label'] = data[label_field]
        data['name'] = data[name_field]
        del data['name_en']  
        del data['label_en']  
        return data

class ChapterSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        label_field = 'label' if lang_header == 'ar' else 'label_en'

        data = super().to_representation(instance)
        data['label'] = data[label_field]
        del data['label_en']  
        return data


class Sub_ChapterSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Sub_Chapter
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['label'] = data['label_en']
            data['review'] = data['review_en']

            # Remove the redundant English fields
            data.pop('label_en', None)
            data.pop('review_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('label_en', None)
            data.pop('review_en', None)

        return data

class ImportFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportFee
        fields = '__all__'
        
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['restriction_import'] = data['restriction_import_en']
            data['document_import'] = data['document_import_en']

            # Remove the redundant English fields
            data.pop('restriction_import_en', None)
            data.pop('document_import_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('restriction_import_en', None)
            data.pop('document_import_en', None)

        return data

class ExportFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportFee
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['export'] = data['export_en']
            data['restriction_export'] = data['restriction_export_en']

            # Remove the redundant English fields
            data.pop('export_en', None)
            data.pop('restriction_export_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('export_en', None)
            data.pop('restriction_export_en', None)

        return data


class StoneFarmingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stone_Farming
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['ston_import'] = data['ston_import_en']
            data['ston_import_notes'] = data['ston_import_notes_en']
            data['ston_export'] = data['ston_export_en']
            data['ston_export_notes'] = data['ston_export_notes_en']

            # Remove the redundant English fields
            data.pop('ston_import_en', None)
            data.pop('ston_import_notes_en', None)
            data.pop('ston_export_en', None)
            data.pop('ston_export_notes_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('ston_import_en', None)
            data.pop('ston_import_notes_en', None)
            data.pop('ston_export_en', None)
            data.pop('ston_export_notes_en', None)

        return data
    
class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')
        finance_field = 'finance' if lang_header == 'ar' else 'finance_en'

        data = super().to_representation(instance)
        data['finance'] = data[finance_field]
        del data['finance_en']  
        return data
    

class FeeSerializer(serializers.ModelSerializer):
    import_fees = ImportFeeSerializer(many=True, read_only=True)
    stone_farming = StoneFarmingSerializer(many=True, read_only=True)
    finance = FinanceSerializer(many=True, read_only=True)
    fees = FeesSerializer(many=True, read_only=True)

    class Meta:
        model = Fee
        fields = '__all__'

    # def to_representation(self, instance):
    #     lang_header = self.context['request'].headers.get('Language', 'ar')
    #     label_field = 'label' if lang_header == 'ar' else 'label_en'

    #     data = super().to_representation(instance)
    #     data['label'] = data[label_field]
    #     del data['label_en']  
    #     return data



class NotesSectionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Notes_section
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['note_a'] = data['note_a_en']
            data['note_b'] = data['note_b_en']
            data['note_c'] = data['note_c_en']
            data['note_num'] = data['note_num_en']

            # Remove the redundant English fields
            data.pop('note_a_en', None)
            data.pop('note_b_en', None)
            data.pop('note_c_en', None)
            data.pop('note_num_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('note_a_en', None)
            data.pop('note_b_en', None)
            data.pop('note_c_en', None)
            data.pop('note_num_en', None)

        return data


class NotesChapterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Notes_chapter
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['note_a'] = data['note_a_en']
            data['note_b'] = data['note_b_en']
            data['note_c'] = data['note_c_en']
            data['note_d'] = data['note_d_en']
            data['note_e'] = data['note_e_en']
            data['note_num'] = data['note_num_en']

            # Remove the redundant English fields
            data.pop('note_a_en', None)
            data.pop('note_b_en', None)
            data.pop('note_c_en', None)
            data.pop('note_d_en', None)
            data.pop('note_e_en', None)
            data.pop('note_num_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('note_a_en', None)
            data.pop('note_b_en', None)
            data.pop('note_c_en', None)
            data.pop('note_d_en', None)
            data.pop('note_e_en', None)
            data.pop('note_num_en', None)

        return data

class NotesSubChapterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Notes_subchapter
        fields = '__all__'


class NotesFeeSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Notes_fee
        fields = '__all__'

class CustomSectionSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Section
        fields = '__all__'
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['label'] = data['label_en']
            data['name'] = data['name_en']

            # Remove the redundant English fields
            data.pop('label_en', None)
            data.pop('name_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('label_en', None)
            data.pop('name_en', None)

        return data
    

class CustomChapterSerializer(serializers.ModelSerializer):
    id_parent_1 = CustomSectionSerializer()

    class Meta:
        model = Chapter
        fields = "__all__"
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['label'] = data['label_en']
          

            # Remove the redundant English fields
            data.pop('label_en', None)
           
        else:
            # If language is Arabic, remove English fields
            data.pop('label_en', None)
           

        return data

class CustomSubChapterSerializer(serializers.ModelSerializer):
    id_parent_2 = CustomChapterSerializer()

    class Meta:
        model = Sub_Chapter
        fields = "__all__"
    def to_representation(self, instance):
        lang_header = self.context['request'].headers.get('Language', 'ar')

        data = super().to_representation(instance)

        if lang_header == 'en':
            # If language is English, replace Arabic fields with English fields
            data['label'] = data['label_en']
            data['review'] = data['review_en']

            # Remove the redundant English fields
            data.pop('label_en', None)
            data.pop('review_en', None)
        else:
            # If language is Arabic, remove English fields
            data.pop('label_en', None)
            data.pop('review_en', None)

        return data
class CommercialDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commercial_Description
        fields = "__all__"

class CustomFeeSerializer(serializers.ModelSerializer):
    import_fees = ImportFeeSerializer(source='importfees', many=True, read_only=True)
    stone_farming = StoneFarmingSerializer(source='stonefarms', many=True, read_only=True)
    finance = FinanceSerializer(source='financefees', many=True, read_only=True)
    export_fees = ExportFeeSerializer(source='exportfees', many=True, read_only=True)
    commercial_descriptions = serializers.SerializerMethodField()  # Use SerializerMethodField for custom method
    fees = FeesSerializer(source='get_Fees', many=False, read_only=True)
    id_parent_3 = CustomSubChapterSerializer(read_only=True)
    
    class Meta:
        model = Fee
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang_header = self.context['request'].headers.get('Language', 'ar')
    
        if lang_header == 'en':
            data['label'] = data['label_en']
            data['review'] = data['review_en']
            data.pop('label_en', None)
            data.pop('review_en', None)
        else:
            data.pop('label_en', None)
            data.pop('review_en', None)
    
        return data
    
    def get_commercial_descriptions(self, obj):
        commercial_descriptions = obj.get_Commercial_Description()
        if commercial_descriptions:
            serializer = CommercialDescriptionSerializer(commercial_descriptions)
            return serializer.data
        return []
    



class ImageDescriptionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    class Meta:
        model = Image_Description
        fields = "__all__"




class CombinedResultSerializer(serializers.Serializer):
    model_name = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_model_name(self, obj):
        return obj.__class__.__name__

    def get_data(self, obj):
        data = []

        if isinstance(obj, Chapter):
            data = [CustomChapterSerializer(obj, context={'request': self.context.get('request')}).data]
            if 'id_parent_1' in data[0]:
                id_parent_1_data = data[0].pop('id_parent_1')
                data[0]['id_parent_1'] = id_parent_1_data
        elif isinstance(obj, Sub_Chapter):
            data = [CustomSubChapterSerializer(obj, context={'request': self.context.get('request')}).data]
            if 'id_parent_2' in data[0]:
                id_parent_2_data = data[0].pop('id_parent_2')
                id_parent_1_data = id_parent_2_data.pop('id_parent_1')
                data[0]['id_parent_2'] = id_parent_2_data
                data[0]['id_parent_2']['id_parent_1'] = id_parent_1_data
        elif isinstance(obj, Fee):
            data = [CustomFeeSerializer(obj, context={'request': self.context.get('request')}).data]

        # Rearrange the data based on the model type
        if 'id_parent_3' in data[0]:
            id_parent_3_data = data[0].pop('id_parent_3')
            id_parent_2_data = id_parent_3_data.pop('id_parent_2')
            id_parent_1_data = id_parent_2_data.pop('id_parent_1')

            data[0]['id_parent_3'] = id_parent_3_data
            data[0]['id_parent_3']['id_parent_2'] = id_parent_2_data
            data[0]['id_parent_3']['id_parent_2']['id_parent_1'] = id_parent_1_data

        return data


class ImageDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Description
        fields = '__all__'
class CombinedDescriptionSerializer(serializers.Serializer):
    commercial_descriptions = CommercialDescriptionSerializer(many=True)
    image_descriptions = ImageDescriptionSerializer(many=True)




