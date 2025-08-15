from django.shortcuts import render

# Create your views here.
import re
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.db.models import Q,Prefetch
from rest_framework import viewsets, filters
from rest_framework import generics
from .models import ExportFee, Finance,Stone_Farming,Commercial_Description, Image_Description, Chapter, Fee,HsCode, ImportFee, Notes_chapter, Notes_fee, Notes_section, Notes_subchapter, Section, Sub_Chapter
from .serializers import ExportFeeSerializer, Fees_sari_Serializer,FeesSerializer,FinanceSerializer,StoneFarmingSerializer,CommercialDescriptionSerializer, ImageDescriptionSerializer, CustomFeeSerializer,ChapterSerializer,  CombinedResultSerializer, FeeSerializer, ImportFeeSerializer, NotesChapterSerializer, NotesFeeSerializer, NotesSectionSerializer, NotesSubChapterSerializer, SectionSerializer, Sub_ChapterSerializer
from django.conf import settings
from Fee_calculator.models import Fees
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.translation import activate


class Pagination(PageNumberPagination):
    page_size = 450
    page_size_query_param = 'page_size'
    max_page_size = 10
    
    
class SectionList(generics.ListAPIView):
    queryset = Section.objects.all().order_by('number')
    serializer_class = SectionSerializer

class SectionDetailView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'id'

class ChapterList(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChapterSectionDetailView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    lookup_field = 'id'

class Sub_ChapterList(generics.ListAPIView):
    queryset = Sub_Chapter.objects.all()
    serializer_class = Sub_ChapterSerializer
    pagination_class = Pagination


class FeeList(generics.ListAPIView):
    queryset = HsCode.objects.all()
    serializer_class = FeeSerializer

class NoteSectionList(generics.ListAPIView):
    queryset = Notes_section.objects.all()
    serializer_class = NotesSectionSerializer

class NoteChapterList(generics.ListAPIView):
    queryset = Notes_chapter.objects.all()
    serializer_class = NotesChapterSerializer

class NoteSubChapterList(generics.ListAPIView):
    queryset = Notes_subchapter.objects.all()
    serializer_class = NotesSubChapterSerializer

class NoteFeeList(generics.ListAPIView):
    queryset = Notes_fee.objects.all()
    serializer_class = NotesFeeSerializer




@api_view(['GET'])
def get_chapters_for_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
        chapters = Chapter.objects.filter(id_parent_1=section)
        section_serializer = SectionSerializer(section, context={'request': request})
        chapter_serializer = ChapterSerializer(chapters, many=True, context={'request': request})
        response_data = {
            'section': section_serializer.data,
            'chapters': chapter_serializer.data
        }
        return Response(response_data)
    except Section.DoesNotExist:
        return Response({'error': 'Section not found'}, status=404)



@api_view(['GET'])
def get_sub_chapters_for_chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        sub_chapters = Sub_Chapter.objects.filter(id_parent_2=chapter)

        # Pass the context to serializers
        chapter_serializer = ChapterSerializer(chapter, context={'request': request})
        sub_chapter_serializer = Sub_ChapterSerializer(sub_chapters, many=True, context={'request': request})

        response_data = {
            'chapter': chapter_serializer.data,
            'sub_chapters': sub_chapter_serializer.data
        }
        return Response(response_data)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=404)


@api_view(['GET'])
def get_fees_for_sub_chapter(request, sub_chapter_id):
    try:
        sub_chapter = Sub_Chapter.objects.get(id=sub_chapter_id)
        fees = HsCode.objects.filter(id_parent_3=sub_chapter)
        sub_chapter_serializer = Sub_ChapterSerializer(sub_chapter)
        fee_serializer = FeeSerializer(fees, many=True)
        response_data = {
            'sub_chapter': sub_chapter_serializer.data,
            'fees': fee_serializer.data
        }
        return Response(response_data)
    except Sub_Chapter.DoesNotExist:
        return Response({'error': 'Sub_Chapter not found'}, status=404)
    


@api_view(['GET'])
def get_fees_and_import_fees_for_sub_chapter(request, sub_chapter_id):
    try:
        sub_chapter = Sub_Chapter.objects.get(id=sub_chapter_id)
        fees = HsCode.objects.filter(id_parent_3=sub_chapter)
        
        # Ensure that the request object is not None before accessing headers
        if request:
            lang_header = request.headers.get('Language', 'ar')  
            activate(lang_header)  
        else:
            lang_header = 'en'

        sub_chapter_serializer = Sub_ChapterSerializer(sub_chapter, context={'request': request, 'lang_header': lang_header})
        fee_serializer = FeeSerializer(fees, many=True, context={'request': request, 'lang_header': lang_header})

        response_data = {
            'sub_chapter': sub_chapter_serializer.data,
            'fees': fee_serializer.data
        }

        for fee_data in response_data['fees']:
            fee_id = fee_data['id']
            import_fees = ImportFee.objects.filter(id_importfee=fee_id)
            import_fee_serializer = ImportFeeSerializer(
                import_fees,
                many=True,
                context={'request': request, 'lang_header': lang_header}
            )
            fee_data['import_fees'] = import_fee_serializer.data

            export_fees = ExportFee.objects.filter(id_exportfee=fee_id)
            export_fee_serializer = ExportFeeSerializer(
                export_fees,
                many=True,
                context={'request': request, 'lang_header': lang_header}
            )
            fee_data['export_fees'] = export_fee_serializer.data

            stone_farming = Stone_Farming.objects.filter(id_stone=fee_id)
            stone_farming_serializer = StoneFarmingSerializer(stone_farming, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['stone_farming'] = stone_farming_serializer.data


            fees = Fees.objects.filter(id=fee_id)
            Fees_Serializer = FeesSerializer(fees, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['fees'] = Fees_Serializer.data

            finance = Finance.objects.filter(id_finance=fee_id)
            finance_serializer = FinanceSerializer(finance, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['finance'] = finance_serializer.data

        return Response(response_data)
    except Sub_Chapter.DoesNotExist:
        return Response({'error': 'Sub_Chapter not found'}, status=404)
    
@api_view(['GET'])
def get_fees_and_import_fees_for_sub_chapter_to_sari(request, sub_chapter_id):
    try:
        sub_chapter = Sub_Chapter.objects.get(id=sub_chapter_id)
        fees = HsCode.objects.filter(id_parent_3=sub_chapter)
        if request:
            lang_header = request.headers.get('Language', 'ar')  
            activate(lang_header)  
        else:
            lang_header = 'en'

        sub_chapter_serializer = Sub_ChapterSerializer(sub_chapter, context={'request': request, 'lang_header': lang_header})
        fee_serializer = FeeSerializer(fees, many=True, context={'request': request, 'lang_header': lang_header})

        response_data = {
            'sub_chapter': sub_chapter_serializer.data,
            'fees': fee_serializer.data
        }

        for fee_data in response_data['fees']:
            fee_id = fee_data['id']
            import_fees = ImportFee.objects.filter(id_importfee=fee_id)
            import_fee_serializer = ImportFeeSerializer(import_fees, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['import_fees'] = import_fee_serializer.data

            
            export_fees = ExportFee.objects.filter(id_exportfee=fee_id)
            export_fee_serializer = ExportFeeSerializer(
                export_fees,
                many=True,
                context={'request': request, 'lang_header': lang_header}
            )
            fee_data['export_fees'] = export_fee_serializer.data

            stone_farming = Stone_Farming.objects.filter(id_stone=fee_id)
            stone_farming_serializer = StoneFarmingSerializer(stone_farming, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['stone_farming'] = stone_farming_serializer.data


            fees = Fees.objects.filter(id=fee_id)
            Fees_Serializer = Fees_sari_Serializer(fees, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['fees'] = Fees_Serializer.data

            finance = Finance.objects.filter(id_finance=fee_id)
            finance_serializer = FinanceSerializer(finance, many=True, context={'request': request, 'lang_header': lang_header})
            fee_data['finance'] = finance_serializer.data
            
        return Response(response_data)
    except Sub_Chapter.DoesNotExist:
        return Response({'error': 'Sub_Chapter not found'}, status=404)

   


class NotesBySectionAPIView(APIView):
    def get(self, request, section_id):
        try:
            if request:
                lang_header = request.headers.get('Language', 'ar')  
                activate(lang_header)  
            else:
                lang_header = 'en'
            notes = Notes_section.objects.filter(id_section=section_id)
            serializer = NotesSectionSerializer(notes, many=True, context={'request': request, 'lang_header': lang_header})
            return Response(serializer.data)
        except Notes_section.DoesNotExist:
            return Response(
                {"message": "Section ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    
class NotesByChapterAPIView(APIView):
    def get(self, request, chapter_id):
        try:
            if request:
                lang_header = request.headers.get('Language', 'ar')  
                activate(lang_header)  
            else:
                lang_header = 'en'
            notes = Notes_chapter.objects.filter(id_chapter=chapter_id)
            serializer = NotesChapterSerializer(notes, many=True, context={'request': request, 'lang_header': lang_header})
            return Response(serializer.data)
        except Notes_chapter.DoesNotExist:
            return Response(
                {"message": "Chapter ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class NotesBySubChapterAPIView(APIView):
    def get(self, request, subchapter_id):
        try:
            notes = Notes_subchapter.objects.filter(id_subchapter=subchapter_id)
            serializer = NotesSubChapterSerializer(notes, many=True)
            return Response(serializer.data)
        except Notes_subchapter.DoesNotExist:
            return Response(
                {"message": "Subchapter ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class NotesByFeeAPIView(APIView):
    def get(self, request, fee_id):
        try:
            notes = Notes_fee.objects.filter(id_fee=fee_id)
            serializer = NotesFeeSerializer(notes, many=True)
            return Response(serializer.data)
        except Notes_fee.DoesNotExist:
            return Response(
                {"message": "Fee ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

class SectionsWithNotesAPIView(APIView):
    def get(self, request):
        sections = Section.objects.all()
        serialized_sections = SectionSerializer(sections, many=True).data

        for section in serialized_sections:
            notes = Notes_section.objects.filter(id_section=section['id'])
            serialized_notes = NotesSectionSerializer(notes, many=True).data
            section['notes'] = serialized_notes

        return Response(serialized_sections)
    

class ChaptersWithNotesAPIView(APIView):
    def get(self, request):
        chapters = Chapter.objects.all()
        serialized_chapters = ChapterSerializer(chapters, many=True).data

        for chapter in serialized_chapters:
            notes = Notes_chapter.objects.filter(id_chapter=chapter['id'])
            serialized_notes = NotesChapterSerializer(notes, many=True).data
            chapter['notes'] = serialized_notes

        return Response(serialized_chapters)
    
class SubChaptersWithNotesAPIView(APIView):
    def get(self, request):
        subchapters = Sub_Chapter.objects.all()
        serialized_subchapters = Sub_ChapterSerializer(subchapters, many=True).data

        for subchapter in serialized_subchapters:
            notes = Notes_subchapter.objects.filter(id_subchapter=subchapter['id'])
            serialized_notes = NotesSubChapterSerializer(notes, many=True).data
            subchapter['notes'] = serialized_notes

        return Response(serialized_subchapters)


@api_view(['GET'])
def get_fees_and_import_fees_for_sub_chapter_with_notes(request, sub_chapter_id):
    try:
        sub_chapter = Sub_Chapter.objects.get(id=sub_chapter_id)
        fees = HsCode.objects.filter(id_parent_3=sub_chapter)
        sub_chapter_serializer = Sub_ChapterSerializer(sub_chapter)
        fee_serializer = FeeSerializer(fees, many=True)

        response_data = {
            'sub_chapter': sub_chapter_serializer.data,
            'fees': fee_serializer.data
        }

        for fee_data in response_data['fees']:
            fee_id = fee_data['id']
            notes = Notes_fee.objects.filter(id_fee=fee_id)
            notes_serializer = NotesFeeSerializer(notes, many=True)
            fee_data['notes'] = notes_serializer.data

            import_fees = ImportFee.objects.filter(id_importfee=fee_id)
            import_fee_serializer = ImportFeeSerializer(import_fees, many=True)
            fee_data['import_fees'] = import_fee_serializer.data

        return Response(response_data)
    except Sub_Chapter.DoesNotExist:
        return Response({'error': 'Sub_Chapter not found'}, status=404)
    

class SearchView(APIView):
    def get(self, request):
        search_string = request.query_params.get('search', '')
        pattern = re.escape(search_string)

        # Step 1: Build base query for direct matches on HsCode
        base_query = Q(
            Q(hs_code__iregex=pattern) |
            Q(label__iregex=pattern) |
            Q(review__iregex=pattern) |
            Q(label_en__iregex=pattern)
        )

        fee_results = HsCode.objects.filter(base_query)

        # Step 2: Query Commercial_Description once with regex match
        commercial_descs = Commercial_Description.objects.filter(second_description__iregex=pattern)

        # Step 3: Get HsCodes indirectly via Commercial_Description
        fee_from_commercial_desc = HsCode.objects.filter(
            id__in=commercial_descs.values_list('id_desc_id', flat=True)
        )

        # Step 4: Combine both sets of results and deduplicate
        all_fee_results = (fee_results | fee_from_commercial_desc).distinct()

        # Step 5: Prefetch filtered commercial descriptions to avoid N+1
        prefetch = Prefetch(
            'commercial_description_set',
            queryset=Commercial_Description.objects.filter(second_description__iregex=pattern),
            to_attr='filtered_descriptions'
        )

        all_fee_results = all_fee_results.prefetch_related(prefetch)

        # Step 6: Serialize with the same output structure
        serialized_data = []
        for fee in all_fee_results:
            serialized_fee = CustomFeeSerializer(fee, context={'request': request}).data

            # Get prefetched filtered descriptions
            commercial_descriptions = getattr(fee, 'filtered_descriptions', [])
            if commercial_descriptions:
                serialized_fee["commercial_descriptions"] = CommercialDescriptionSerializer(
                    commercial_descriptions, many=True
                ).data
            else:
                serialized_fee["commercial_descriptions"] = []

            serialized_data.append({
                "model_name": "HsCode",
                "data": [serialized_fee]  # Wrap in list like original
            })

        return Response({
            "HsCode": serialized_data
        })      
        
class SecondDescription(APIView):
    def get(self, request, id_desc):
        
        commercial_descriptions = Commercial_Description.objects.filter(id_desc=id_desc)
        image_descriptions = Image_Description.objects.filter(id_desc=id_desc)
        commercial_serializer = CommercialDescriptionSerializer(commercial_descriptions, many=True)
        image_serializer = ImageDescriptionSerializer(image_descriptions, many=True)

        response_data = {
            "commercial_descriptions": commercial_serializer.data,
            "image_descriptions": image_serializer.data,
        }

        for item in response_data['image_descriptions']:
           item['image'] = request.build_absolute_uri( str(item['image']))

        return Response(response_data)



