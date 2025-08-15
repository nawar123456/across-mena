from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import  OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import ExtraSerializer, FeesSerializer, OriginSerializer, PortSerializer, airPortSerializer
from .models import Extra, Fees, Origin, Port, Airport
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Taxes , Atom
from .serializers import AtomSerializer , CountrySerializer
from rest_framework import status
from rest_framework.decorators import api_view
from decimal import Decimal
from django.core.mail import send_mail
from django.http import HttpResponse
import json
from rest_framework import generics
from django.db.models import Q
import re
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet


class FeesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000  

class FeesViewSet(ModelViewSet):
    queryset = Fees.objects.all() 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = FeesSerializer
    search_fields = ['label','label_en']
    pagination_class = FeesPagination


class OriginViewSet(ModelViewSet):
    queryset = Origin.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lang']
    serializer_class = OriginSerializer
    search_fields = ['label']
    ordering_fields = ['label']
    ordering = ['label']

    
class ExtraViewSet(ModelViewSet):
    queryset = Extra.objects.all()
    serializer_class=ExtraSerializer

class GetPriceByInput(APIView):
    def get(self, request, input_number):
        try:
            weight = Decimal(input_number)
        except ValueError:
            return Response({'error': 'Invalid input number'}, status=400)
        if 0 <= weight <= 1000:
            category = '1 kg to 1 ton'
        elif 1000 < weight <= 10000:
            category = '1 ton to 10 ton'
        elif 10000 < weight <= 20000:
            category = '10 ton to 20 ton'
        elif 20000 < weight <= 50000:
            category = '20 ton to 50 ton'
        elif 50000 < weight <= 100000:
            category = '50 ton to 100 ton'
        elif 100000 < weight <= 300000:
            category = '100 ton to 300 ton'
        elif 300000 < weight <= 1000000:
            category = '300 ton to 1000 ton'
        elif 1000000 < weight <= 5000000:
            category = '1000 ton to 5000 ton'
        elif 5000000 < weight <= 10000000:
            category = '5000 ton to 10000 ton'
        elif 10000000 < weight <= 15000000:
            category = '10000 ton to 15000 ton'
        elif 15000000 < weight :
            category = 'than of 15000 ton'
        
        else:
            return Response({'error': 'Category not found'}, status=404)
        
        try:
            atom = Atom.objects.get(categories=category)
        except Atom.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        
        serializer = AtomSerializer(atom)
        return Response(serializer.data)

class TotalPriceSumView(APIView):
     def get(self, request):
        taxes_instances = Taxes.objects.all()
        total_price_sum = taxes_instances.aggregate(total_price=Sum('price'))['total_price']
        
        return Response({"total_price_sum": total_price_sum})


def send_email(request):
    if request.method == 'GET':
        data = request.GET
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Define the recipient email address(es) as a list
        recipient_list = ['hayahamada10311@gmail.com']  

        # Send an email using Django's send_mail function
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'acroifcn@across-mena.com',
            recipient_list, 
            fail_silently=False,
        )

        send_mail(
            'نشكركم على التواصل معنا سيتم التواصل معكم من قبل الفريق المختص',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'acroifcn@across-mena.com',
            [email],  # Use the sender's email as the recipient
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully'})
    
    return JsonResponse({'message': 'Invalid request method'}, status=405)



@csrf_exempt
def calculate_view(request):
    customs_fee = 0.0
    spending_fee = 0.0
    #imran_locality = 0.0
    conservative_locality = 0.0
    fee_supporting_local_production = 0.0
    cities_protection_fee = 0.0
    natural_disaster_fee = 0.0
    income_tax_fee = 0.0
    import_license_fee = 0.0
    final_fee = 0.0
    added_taxes = 0.0
    customs_certificate = 0.0
    bill_tax = 0.0
    insurance_fee = 0.0
    stamp_fee = 0.0
    provincial_local_tax = 0.0
    advance_income_tax = 0.0
    reconstruction_fee = 0.0
    Granting_import_license = 0.0
    final_taxes = 0.0
    final_total = 0.0

    if request.method == 'GET':
        try:
            #قيمة البضاعة مع التأمين
            insurance = Decimal(request.GET.get('insurance', 0))
            #المنشأ
            origin = request.GET.get("origin", "")
            #الرسم الجمركي
            fee = float(request.GET.get("fee", 0))
            #رسم الإنفاق
            spending_fee = Decimal(request.GET.get("spending_fee", 0))
            #محلية عمران
            #local_fee = Decimal(request.GET.get("local_fee", 0))
            # عامود رسم دعم و تنمية الانتاج المحلي 
            support_fee = Decimal(request.GET.get("support_fee", 0))
            # عامود تأهيل وحماية المدن والمنشاة
            protection_fee = Decimal(request.GET.get("protection_fee", 0))
            #عامود رسم صندوق الجفاف و الكوارث الطبيعة 
            natural_fee = Decimal(request.GET.get("natural_fee", 0))
            # عامود رسم السلفة على ضريبة الدخل 
            tax_fee = Decimal(request.GET.get("tax_fee", 0))
            # عامود رسم الترخيص بالاستراد
            import_fee = Decimal(request.GET.get("import_fee", 0))
            #مادة اولية
            raw_material = int(request.GET.get("raw_material", 0))
            #المنشأ صناعية 
            industrial = int(request.GET.get("industrial", 0))
            # الضرائب الكاملة 
            total_tax = Decimal(request.GET.get("total_tax", 0))
            # الضرائب الجزئية
            partial_tax = Decimal(request.GET.get("partial_tax", 0))
            # طابع خاص بالاتفاقية العربية
            arabic_stamp = Decimal(request.GET.get("arabic_stamp", 0))
            # الوزن
            weight = Decimal(request.GET.get('weight', 0))
            # القنصلية
            cnsulate = int(request.GET.get("cnsulate", 0))
            # السعر 
            price = Decimal(request.GET.get('price', 0))
            # الدولار
            dolar = Decimal(request.GET.get('dolar', 0))
            # البلدان العربية
            countries_arabic =['الإمارات العربية المتحدة ' , 'البحرين' , 'الكويت' , 'المملكة العربية السعودية' , 'اليمن' , 'دولة قطر' , 'الأردن' , 'سلطنة عمان' , 'الجمهورية العربية السورية' , 'لبنان' , 'فلسطين' , 'العراق' , 'مصر' , 'المغرب' , 'ليبيا' , 'تونس' , 'الجزائر' , 'السودان' , 'جنوب السودان' , 'موريتانيا' , 'الصومال' , 'جيبوتي' , 'جزر القمر' , 'جنوب أفريقيا' , 'Yemen' , 'United Arab Emirates' , 'Tunisia' , 'Syrian Arab Republic' , 'Sudan' , 'South Sudan' , 'South Africa' , 'Somalia' , 'Saudi Arabia' , 'Qatar' , 'Palestine' , 'Oman' , 'Morocco' , 'Libya' , 'Lebanon' , 'Kuwait' , 'Jordan' , 'Iraq' , 'Egypt' , 'Comoros' , 'Bahrain' , 'Algeria' , 'Djibouti' , 'Mauritania']
            # ايران
            countries_iran =['Islamic Republic of Iran' , 'جمهورية ايران الاسلامية']
            if 0 <= weight <= 1000:
                category = '1 kg to 1 ton'
            elif 1000 < weight <= 10000:
                category = '1 ton to 10 ton'
            elif 10000 < weight <= 20000:
                category = '10 ton to 20 ton'
            elif 20000 < weight <= 50000:
                category = '20 ton to 50 ton'
            elif 50000 < weight <= 100000:
                category = '50 ton to 100 ton'
            elif 100000 < weight <= 300000:
                category = '100 ton to 300 ton'
            elif 300000 < weight <= 1000000:
                category = '300 ton to 1000 ton'
            elif 1000000 < weight <= 5000000:
                category = '1000 ton to 5000 ton'
            elif 5000000 < weight <= 10000000:
                category = '5000 ton to 10000 ton'
            elif 10000000 < weight <= 15000000:
                category = '10000 ton to 15000 ton'
            elif 15000000 < weight :
                category = 'than of 15000 ton'
            else:
                return JsonResponse({'error': 'Category not found'}, status=404)

            try:
                atom = Atom.objects.get(categories=category)
                category_price = atom.price

                # اذا كان المنشأ صناعي والمادة اولية والرسم الجمركي هو 0.01 

                if( raw_material == 1 and industrial == 1 and fee == 0.01):
                   #  رسم الجمارك
                    customs_fee = Decimal('0.0')
                    #  رسم الانفاق 
                    spending_fee = Decimal('0.0')
                    #  محلية عمران
                    #imran_locality = Decimal('0.0')
                    # محلية محافظة 
                    conservative_locality = Decimal('0.0')
                    #  رسم دعم تنمية الانتاج المحلي 
                    fee_supporting_local_production = Decimal('0.0')
                    #  رسم تأهيل وحماية المدن والمنشاة
                    cities_protection_fee = Decimal('0.0')
                    #  رسم صندوق الجفاف و الكوارث الطبيعية 
                    natural_disaster_fee = Decimal('0.0')
                    #  رسم السلفة على ضريبة الدخل
                    income_tax_fee = Decimal('0.0')
                    #  رسم الترخيص بالاستراد
                    import_license_fee = Decimal('0.0')
                    #رسم الذرة 
                    category_price = category_price
                    # رسم القنصلية + غرامة قنصلية
                    if cnsulate == 1:
                        consulate_fee = Decimal('0.0')
                        consulate_tax = Decimal('0.0')
                    elif cnsulate == 0:
                        consulate_fee =  (( price * Decimal('0.015')) + 50)
                        consulate_tax = ((consulate_fee / 2) * dolar)
                    # الرسم النهائي
                    final_fee = 0 +  category_price + consulate_tax
                    # ضرائب مضافة
                    added_taxes = total_tax
                    # شهادة جمركية
                    #customs_certificate = Decimal('1000.0')
                    #غرامة فاتورة 
                    #bill_tax = Decimal('0.0')
                    if origin in countries_arabic:
                     #رسم تأمين إلزامي
                        insurance_fee = ((insurance * Decimal('0.01'))/12)
                        # رسم طابع
                        stamp_fee =  insurance * Decimal('0.0015') 
                        # بدل خدمة منح إجازة استراد
                        Granting_import_license = insurance * Decimal('0.0005') 
                        # ضريبة محلية محافظة
                        provincial_local_tax = ((insurance * Decimal('0.001') ) + ((customs_fee * Decimal('0.1')))+ ((spending_fee + added_taxes + arabic_stamp + Granting_import_license + stamp_fee + insurance_fee) * Decimal('0.05')))
                        # السلفة على ضريبة الدخل 
                        advance_income_tax = (( added_taxes + arabic_stamp+ provincial_local_tax + stamp_fee + insurance_fee  + Granting_import_license + consulate_tax) * tax_fee)
                        # رسم المساهمة الوطنية لإعادة الإعمار
                        reconstruction_fee = (( added_taxes  + arabic_stamp + insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + final_fee + Granting_import_license) * Decimal('0.1') )
                        # مجموع الضرائب النهائي
                        final_taxes = (added_taxes + arabic_stamp+ insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee + Granting_import_license )
                        # مجموع الرسوم والضرائب
                        final_total = final_taxes + final_fee
                    else:
                         #رسم تأمين إلزامي
                        insurance_fee = ((insurance * Decimal('0.01'))/12)
                        # رسم طابع
                        stamp_fee =  insurance * Decimal('0.0015') 
                        # ضريبة محلية محافظة
                        provincial_local_tax = ((insurance * Decimal('0.001') ) + ((customs_fee * Decimal('0.1'))) + ((spending_fee + added_taxes + stamp_fee + insurance_fee ) * Decimal('0.05')))
                        # السلفة على ضريبة الدخل 
                        advance_income_tax = (( added_taxes +   provincial_local_tax + stamp_fee + insurance_fee + consulate_tax  ) * tax_fee)
                        # رسم المساهمة الوطنية لإعادة الإعمار
                        reconstruction_fee = (( added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + final_fee ) * Decimal('0.1') )
                        # بدل خدمة منح إجازة استراد
                        Granting_import_license = Decimal('0.0')
                        # مجموع الضرائب النهائي
                        final_taxes = (added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee )
                    # مجموع الرسوم والضرائب
                        final_total = final_taxes + final_fee
                        
                    return JsonResponse({'customs_fee': customs_fee, 'spending_fee': spending_fee, 'conservative_locality': conservative_locality, 'fee_supporting_local_production': fee_supporting_local_production, 'cities_protection_fee': cities_protection_fee, 'natural_disaster_fee': natural_disaster_fee, 'income_tax_fee': income_tax_fee, 'import_license_fee': import_license_fee , 'consulate_tax':consulate_tax, 'category_price': category_price,'final_fee': final_fee, 'added_taxes': added_taxes, 'insurance_fee': insurance_fee, 'stamp_fee': stamp_fee, 'provincial_local_tax': provincial_local_tax, 'advance_income_tax': advance_income_tax, 'reconstruction_fee': reconstruction_fee, 'final_taxes': final_taxes, 'final_total': final_total, 'Granting_import_license': Granting_import_license })
        
             # الاتفاقية العربية

                elif origin in countries_arabic:
                    #  رسم الجمارك
                    customs_fee = Decimal('0.0')
                    #  محلية عمران
                    #imran_locality = insurance * local_fee
                    # محلية محافظة 
                    conservative_locality = insurance * Decimal('0.001')
                    #  رسم دعم تنمية الانتاج المحلي 
                    fee_supporting_local_production = insurance * support_fee
                    #  رسم تأهيل وحماية المدن والمنشاة
                    cities_protection_fee = insurance * protection_fee
                    #  رسم صندوق الجفاف و الكوارث الطبيعية 
                    natural_disaster_fee = insurance * natural_fee
                    #  رسم الترخيص بالاستراد
                    import_license_fee = insurance * import_fee
                    #  رسم السلفة على ضريبة الدخل
                    income_tax_fee = ((insurance + customs_fee + conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + import_license_fee ) * tax_fee )
                    #  رسم الانفاق 
                    spending_fee = (insurance + import_license_fee) * spending_fee
                    #رسم الذرة 
                    category_price = category_price
                    # رسم القنصلية + غرامة قنصلية
                    if cnsulate == 1:
                        consulate_fee = Decimal('0.0')
                        consulate_tax = Decimal('0.0')
                    elif cnsulate == 0:
                        consulate_fee =  (( price * Decimal('0.015')) + 50)
                        consulate_tax = ((consulate_fee / 2) * dolar)
                    # الرسم النهائي
                    final_fee = category_price + customs_fee + spending_fee + conservative_locality +fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + income_tax_fee + import_license_fee 
                    # ضرائب مضافة 
                    added_taxes = total_tax + arabic_stamp
                    # شهادة جمركية
                    #customs_certificate = Decimal('1000.0')
                    #غرامة فاتورة 
                    #bill_tax = Decimal('0.0')
                    #رسم تأمين إلزامي
                    insurance_fee = ((insurance * Decimal('0.01'))/12)
                    # رسم طابع
                    stamp_fee =  insurance * Decimal('0.0015') 
                    # بدل خدمة منح إجازة استراد
                    Granting_import_license = 25000 
                    # ضريبة محلية محافظة
                    provincial_local_tax = ((insurance * Decimal('0.001') ) + ((spending_fee + added_taxes + Granting_import_license + stamp_fee + insurance_fee) * Decimal('0.05')))
                    # السلفة على ضريبة الدخل 
                    advance_income_tax = (( added_taxes +  provincial_local_tax + stamp_fee + insurance_fee  + Granting_import_license + consulate_tax ) * tax_fee)
                    # رسم المساهمة الوطنية لإعادة الإعمار
                    reconstruction_fee = (( added_taxes  + insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + final_fee + Granting_import_license) * Decimal('0.1') )
                    # مجموع الضرائب النهائي
                    final_taxes = (added_taxes + insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee + Granting_import_license )
                    # مجموع الرسوم والضرائب
                    final_total = final_taxes + final_fee
                        
                    return JsonResponse({'customs_fee': customs_fee, 'spending_fee': spending_fee,  'category_price': category_price, 'conservative_locality': conservative_locality, 'fee_supporting_local_production': fee_supporting_local_production, 'cities_protection_fee': cities_protection_fee, 'natural_disaster_fee': natural_disaster_fee, 'consulate_tax': consulate_tax, 'income_tax_fee': income_tax_fee, 'import_license_fee': import_license_fee, 'final_fee': final_fee, 'added_taxes': added_taxes, 'insurance_fee': insurance_fee, 'stamp_fee': stamp_fee, 'provincial_local_tax': provincial_local_tax, 'advance_income_tax': advance_income_tax, 'reconstruction_fee': reconstruction_fee, 'final_taxes': final_taxes, 'final_total': final_total, 'Granting_import_license': Granting_import_license })
               
               # الاتفاقية الايرانية
               
                elif origin in countries_iran:
                    if fee > 0.05:
                        fee = 0.04
                    elif fee <= 0.05:
                        fee =0.01
                    #  رسم الجمارك
                    customs_fee = insurance * Decimal(fee)
                    #  محلية عمران
                    #imran_locality = insurance * local_fee
                    # محلية محافظة 
                    conservative_locality = insurance * Decimal('0.001')
                    #  رسم دعم تنمية الانتاج المحلي 
                    fee_supporting_local_production = insurance * support_fee
                    #  رسم تأهيل وحماية المدن والمنشاة
                    cities_protection_fee = insurance * protection_fee
                    #  رسم صندوق الجفاف و الكوارث الطبيعية 
                    natural_disaster_fee = insurance * natural_fee
                    #  رسم السلفة على ضريبة الدخل
                    income_tax_fee = ((insurance + conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee ) * tax_fee )
                    #  رسم الانفاق 
                    spending_fee = (insurance + customs_fee ) * spending_fee
                    #رسم الذرة 
                    category_price = category_price
                    # رسم القنصلية + غرامة قنصلية
                    if cnsulate == 1:
                        consulate_fee = Decimal('0.0')
                        consulate_tax = Decimal('0.0')
                    elif cnsulate == 0:
                        consulate_fee =  (( price * Decimal('0.015')) + 50)
                        consulate_tax = ((consulate_fee / 2) * dolar)
                    # الرسم النهائي
                    final_fee = category_price + customs_fee + spending_fee +  conservative_locality +fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + income_tax_fee 
                    # ضرائب مضافة 
                    added_taxes = total_tax + arabic_stamp
                    # شهادة جمركية
                    #customs_certificate = Decimal('1000.0')
                    #غرامة فاتورة 
                    #bill_tax = Decimal('0.0')
                     #رسم تأمين إلزامي
                    insurance_fee = ((insurance * Decimal('0.01'))/12)
                    # رسم طابع
                    stamp_fee =  insurance * Decimal('0.0015') 
                    # ضريبة محلية محافظة
                    provincial_local_tax = ((insurance * Decimal('0.001') ) + ((customs_fee * Decimal('0.1'))) + ((spending_fee + added_taxes + stamp_fee + insurance_fee ) * Decimal('0.05')))
                    # السلفة على ضريبة الدخل 
                    advance_income_tax = (( added_taxes +   provincial_local_tax + stamp_fee + insurance_fee + consulate_tax  ) * tax_fee)
                    # رسم المساهمة الوطنية لإعادة الإعمار
                    reconstruction_fee = (( added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + final_fee ) * Decimal('0.1') )
                    # مجموع الضرائب النهائي
                    final_taxes = (added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee )
                    # مجموع الرسوم والضرائب
                    final_total = final_taxes + final_fee
                        
                    return JsonResponse({'customs_fee': customs_fee, 'spending_fee': spending_fee, 'category_price': category_price, 'conservative_locality': conservative_locality, 'fee_supporting_local_production': fee_supporting_local_production, 'cities_protection_fee': cities_protection_fee, 'natural_disaster_fee': natural_disaster_fee, 'income_tax_fee': income_tax_fee, 'consulate_tax':consulate_tax, 'final_fee': final_fee, 'added_taxes': added_taxes,  'insurance_fee': insurance_fee, 'stamp_fee': stamp_fee, 'provincial_local_tax': provincial_local_tax, 'advance_income_tax': advance_income_tax, 'reconstruction_fee': reconstruction_fee, 'final_taxes': final_taxes, 'final_total': final_total, })
               # الاتفاقية العامة 
                else:
                     #  رسم الجمارك
                    customs_fee = insurance * Decimal(fee)
                    #  محلية عمران
                    #imran_locality = insurance * local_fee
                    # محلية محافظة 
                    conservative_locality = insurance * Decimal('0.001')
                    #  رسم دعم تنمية الانتاج المحلي 
                    fee_supporting_local_production = insurance * support_fee
                    #  رسم تأهيل وحماية المدن والمنشاة
                    cities_protection_fee = insurance * protection_fee
                    #  رسم صندوق الجفاف و الكوارث الطبيعية 
                    natural_disaster_fee = insurance * natural_fee
                    #  رسم السلفة على ضريبة الدخل
                    income_tax_fee = ((insurance + customs_fee +  conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee ) * tax_fee )
                    #  رسم الانفاق 
                    spending_fee = (insurance + customs_fee) * spending_fee
                    #رسم الذرة 
                    category_price = category_price
                    # رسم القنصلية + غرامة قنصلية
                    if cnsulate == 1:
                        consulate_fee = Decimal('0.0')
                        consulate_tax = Decimal('0.0')
                    elif cnsulate == 0:
                        consulate_fee =  (( price * Decimal('0.015')) + 50)
                        consulate_tax = ((consulate_fee / 2) * dolar)
                    # الرسم النهائي
                    final_fee = category_price + customs_fee + spending_fee  + conservative_locality +fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + income_tax_fee 
                    # ضرائب مضافة 
                    added_taxes = total_tax 
                    # شهادة جمركية
                    #customs_certificate = Decimal('1000.0')
                    #غرامة فاتورة 
                    #bill_tax = Decimal('0.0')
                    #رسم تأمين إلزامي
                    insurance_fee = ((insurance * Decimal('0.01'))/12)
                    # رسم طابع
                    stamp_fee =  insurance * Decimal('0.0015') 
                    # ضريبة محلية محافظة
                    provincial_local_tax = ((insurance * Decimal('0.001') ) + ((customs_fee * Decimal('0.1'))) + ((spending_fee + added_taxes + stamp_fee + insurance_fee ) * Decimal('0.05')))
                    # السلفة على ضريبة الدخل 
                    advance_income_tax = (( added_taxes +   provincial_local_tax + stamp_fee + insurance_fee + consulate_tax  ) * tax_fee)
                    # رسم المساهمة الوطنية لإعادة الإعمار
                    reconstruction_fee = (( added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + final_fee ) * Decimal('0.1') )
                    # مجموع الضرائب النهائي
                    final_taxes = (added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee )
                    # مجموع الرسوم والضرائب
                    final_total = final_taxes + final_fee
                        
                    return JsonResponse({'customs_fee': customs_fee, 'spending_fee': spending_fee, 'category_price': category_price, 'conservative_locality': conservative_locality, 'fee_supporting_local_production': fee_supporting_local_production, 'cities_protection_fee': cities_protection_fee, 'natural_disaster_fee': natural_disaster_fee, 'income_tax_fee': income_tax_fee, 'consulate_tax':consulate_tax, 'final_fee': final_fee, 'added_taxes': added_taxes, 'insurance_fee': insurance_fee, 'stamp_fee': stamp_fee, 'provincial_local_tax': provincial_local_tax, 'advance_income_tax': advance_income_tax, 'reconstruction_fee': reconstruction_fee, 'final_taxes': final_taxes, 'final_total': final_total, })
            except Atom.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        except ValueError:
            return JsonResponse({'error': 'Invalid input weight'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'})


class OriginListAPIView(APIView):
    def get(self, request, language='english', origin=None, *args, **kwargs):
        # Your existing language validation code
        language = language.lower()
        valid_languages = ['english', 'arabic']

        if language not in valid_languages:
            return Response({"detail": "Invalid language parameter"}, status=400)

        # Filter origins based on language
        if language == 'english':
            origins = Origin.objects.filter(label__iregex=r'^[a-zA-Z]')
        else:
            origins = Origin.objects.filter(label__iregex=r'^[^\x00-\x7F]+')

        # Filter origins based on specified origin (if provided)
        if origin:
            origins = origins.filter(label=origin)

        # Create an empty list to store the serialized data for each origin
        result = []

        # Loop through each origin and retrieve the associated ports
        for origin in origins:
            ports = Port.objects.filter(countries_code=origin.countries_code)

            # Filter ports based on the language of the origin
            if language == 'english':
                ports = ports.filter(name__iregex=r'^[a-zA-Z]')
            else:
                ports = ports.filter(name__iregex=r'^[^\x00-\x7F]+')

            port_serializer = PortSerializer(ports, many=True)

            # Serialize the origin along with the associated ports
            origin_data = {
                'origin': {
                    'label': origin.label,
                    'ImageURL': origin.ImageURL,
                    'countries_code': origin.countries_code,
                },
                'ports': port_serializer.data
            }

            result.append(origin_data)

        return Response(result)
        
        
#search if the result is an origin, it includes all the ports belonging to it, and if the result is a port, it includes the origin information

class SearchView(APIView):
    def get(self, request):
        search_string = request.query_params.get('search', '')
        
        # Detect language based on the search string
        language = 'english' if not any(ord(char) > 127 for char in search_string) else 'arabic'
        
        pattern = re.escape(search_string)  # Escape special regex characters

        # 🔹 **Filter origins based on detected language**
        if language == 'english':
            origins = Origin.objects.filter(Q(label__iregex=pattern))
        else:
            origins = Origin.objects.filter(Q(label_ar__iregex=pattern))

        # 🔹 **Create a list to store the serialized data**
        result = []

        # 🔹 **Loop through each origin and retrieve associated ports**
        for origin in origins:
            origin_dict = {
                "ImageURL": origin.ImageURL,
                "countries_code": origin.countries_code,
                "label": origin.label if language == 'english' else origin.label_ar  # Return label in the detected language
            }

            # Retrieve associated ports and apply the correct language
            ports = Port.objects.filter(countries_code=origin.countries_code)
            port_list = [
                {
                    "name": port.name if language == 'english' else port.name_arabic,
                    "port_code": port.port_code,
                }
                for port in ports
            ]

            origin_dict["ports"] = port_list
            result.append({"origin": origin_dict})

        # 🔹 **Include standalone ports in the result**
        standalone_ports = Port.objects.filter(
            Q(name__iregex=pattern) | Q(name_arabic__iregex=pattern)
        )
        for port in standalone_ports:
            port_dict = {
                "name": port.name if language == 'english' else port.name_arabic,
                "port_code": port.port_code,
            }
            origin = Origin.objects.filter(countries_code=port.countries_code).first()
            if origin:
                # Include origin details with the correct language
                origin_dict = {
                    "ImageURL": origin.ImageURL,
                    "countries_code": origin.countries_code,
                    "label": origin.label if language == 'english' else origin.label_ar
                }
                port_dict["origin"] = origin_dict

            result.append(port_dict)

        return Response(result)


# search every airport and the origin to it
class AirportView(APIView):
    def get(self, request):
        search_string = request.query_params.get('search', '')
        # Detect language based on the search string
        language = 'arabic' if any(ord(char) > 127 for char in search_string) else 'english'
        valid_languages = ['english', 'arabic']
        if language not in valid_languages:
            return Response({"detail": "Invalid language parameter"}, status=400)
        pattern = re.escape(search_string)
        # Filter origins based on language
        if language == 'english':
            origins = Origin.objects.filter(label__iregex=r'^[a-zA-Z]')
        else:
            origins = Origin.objects.filter(label_ar__iregex=r'^[^\x00-\x7F]+')
        # Filter origins based on the specified search string
        if search_string:
            origins = origins.filter(Q(label__iregex=pattern) | Q(label_ar__iregex=pattern))
        # Create a list to store the serialized data for each origin and airport
        result = []
        # Loop through each origin and retrieve the associated airports
        for origin in origins:
            origin_dict = {
                "ImageURL": origin.ImageURL,
                "countries_code": origin.countries_code,
            }
            # Determine which label to include based on language
            if language == 'english':
                origin_dict["label"] = origin.label
            else:
                origin_dict["label_ar"] = origin.label_ar
            # Retrieve associated airports for the current origin
            airports = Airport.objects.filter(countries_code=origin.countries_code)
            airport_list = []
            for airport in airports:
                airport_dict = {
                    "name": airport.name if language == 'english' else airport.name_arabic,
                    "airport_code": airport.airport_code,
                }
                airport_list.append(airport_dict)
            origin_dict["airports"] = airport_list
            result.append({"origin": origin_dict})
        # Include standalone airports in the result
        standalone_airports = Airport.objects.filter(Q(name__iregex=pattern) | Q(name_arabic__iregex=pattern))
        for airport in standalone_airports:
            airport_dict = {
                "name": airport.name if language == 'english' else airport.name_arabic,
                "airport_code": airport.airport_code,
            }
            origin = Origin.objects.filter(countries_code=airport.countries_code).first()
            if origin:
                # Include label within the origin dictionary for standalone airports
                origin_dict = {
                    "ImageURL": origin.ImageURL,
                    "countries_code": origin.countries_code,
                }
                if language == 'english':
                    origin_dict["label"] = origin.label
                else:
                    origin_dict["label_ar"] = origin.label_ar
                airport_dict["origin"] = origin_dict
            result.append(airport_dict)
        return Response(result)









class CalculateViewSet(ViewSet):
    @staticmethod
    @api_view(['POST'])
    def calculate_view(request):
        customs_fee = 0.0
        spending_fee = 0.0
        conservative_locality = 0.0
        fee_supporting_local_production = 0.0
        cities_protection_fee = 0.0
        natural_disaster_fee = 0.0
        income_tax_fee = 0.0
        import_license_fee = 0.0
        final_fee = 0.0
        added_taxes = 0.0
        customs_certificate = 0.0
        bill_tax = 0.0
        insurance_fee = 0.0
        stamp_fee = 0.0
        provincial_local_tax = 0.0
        advance_income_tax = 0.0
        reconstruction_fee = 0.0
        Granting_import_license = 0.0
        final_taxes = 0.0
        final_total = 0.0
        import_fee = 0.0
        consulate_fee = 0.0
        consulate_tax= 0.0
        total_price = Decimal('0.0') 
        total_price_sy = 0.0 
        try:
            data = json.loads(request.body)
            results = []
            for params in data:
                try:
                    insurance = Decimal(params.get('insurance', 0))
                    #قيمة البضاعة مع التأمين
                    insurance = Decimal(params.get('insurance', 0))
                    #المنشأ
                    origin = params.get("origin", "")
                    #المصدر
                    source = params.get("source", "")
                    #الرسم الجمركي
                    fee = Decimal(params.get("fee", 0))
                    #رسم الإنفاق
                    spending_fee = Decimal(params.get("spending_fee", 0))
                    #محلية عمران
                    #local_fee = Decimal(params.get("local_fee", 0))
                    # عامود رسم دعم و تنمية الانتاج المحلي 
                    support_fee = Decimal(params.get("support_fee", 0))
                    # عامود تأهيل وحماية المدن والمنشاة
                    protection_fee = Decimal(params.get("protection_fee", 0))
                    #عامود رسم صندوق الجفاف و الكوارث الطبيعة 
                    natural_fee = Decimal(params.get("natural_fee", 0))
                    # عامود رسم السلفة على ضريبة الدخل 
                    tax_fee = Decimal(params.get("tax_fee", 0))
                    # عامود رسم الترخيص بالاستراد
                    import_fee = Decimal(params.get("import_fee", 0))
                    #مادة اولية
                    raw_material = int(params.get("raw_material", 0))
                    #المنشأ صناعية 
                    industrial = int(params.get("industrial", 0))
                    # الضرائب الكاملة 
                    total_tax = Decimal(params.get("total_tax", 0))
                    # الضرائب الجزئية
                    partial_tax = Decimal(params.get("partial_tax", 0))
                    # طابع خاص بالاتفاقية العربية
                    arabic_stamp = Decimal(params.get("arabic_stamp", 0))
                    # الوزن
                    weight = Decimal(params.get('weight', 0))
                    # القنصلية
                    cnsulate = int(params.get("cnsulate", 0))
                    # السعر 
                    price = Decimal(params.get('price', 0))
                    # الدولار
                    dolar = Decimal(params.get('dolar', 0))
                    # البلدان العربية
                    countries_arabic =['الإمارات العربية المتحدة ' , 'البحرين' , 'الكويت' , 'المملكة العربية السعودية' , 'اليمن' , 'دولة قطر' , 'الأردن' , 'سلطنة عمان' , 'الجمهورية العربية السورية' , 'لبنان' , 'فلسطين' , 'العراق' , 'مصر' , 'المغرب' , 'ليبيا' , 'تونس' , 'الجزائر' , 'السودان' , 'جنوب السودان' , 'موريتانيا' , 'الصومال' , 'جيبوتي' , 'جزر القمر' , 'جنوب أفريقيا' , 'Yemen' , 'United Arab Emirates' , 'Tunisia' , 'Syrian Arab Republic' , 'Sudan' , 'South Sudan' , 'South Africa' , 'Somalia' , 'Saudi Arabia' , 'Qatar' , 'Palestine' , 'Oman' , 'Morocco' , 'Libya' , 'Lebanon' , 'Kuwait' , 'Jordan' , 'Iraq' , 'Egypt' , 'Comoros' , 'Bahrain' , 'Algeria' , 'Djibouti' , 'Mauritania']
                    # ايران
                    countries_iran =['Islamic Republic of Iran' , 'جمهورية ايران الاسلامية']
                    # Weight categorization logic
                    if 0 <= weight <= 1000:
                        category = '1 kg to 1 ton'
                    elif 1000 < weight <= 10000:
                        category = '1 ton to 10 ton'
                    elif 10000 < weight <= 20000:
                        category = '10 ton to 20 ton'
                    elif 20000 < weight <= 50000:
                        category = '20 ton to 50 ton'
                    elif 50000 < weight <= 100000:
                        category = '50 ton to 100 ton'
                    elif 100000 < weight <= 300000:
                        category = '100 ton to 300 ton'
                    elif 300000 < weight <= 1000000:
                        category = '300 ton to 1000 ton'
                    elif 1000000 < weight <= 5000000:
                        category = '1000 ton to 5000 ton'
                    elif 5000000 < weight <= 10000000:
                        category = '5000 ton to 10000 ton'
                    elif 10000000 < weight <= 15000000:
                        category = '10000 ton to 15000 ton'
                    elif 15000000 < weight :
                        category = 'than of 15000 ton'
                    else:
                        return JsonResponse({'error': 'Category not found'}, status=404)

                    # Fetch Atom object based on the category
                    try:
                        atom = Atom.objects.get(categories=category)
                        category_price = atom.price
                    except Atom.DoesNotExist:
                        return JsonResponse({'error': 'Atom object not found for category'}, status=404)
                    # total price in dolar 
                    total_price += price
                    # total price in syrian 
                    total_price_sy = total_price * dolar
                    # المادة اولية المنشأ صناعية الرسم الجمركي 0.01
                    if (fee == 0.0100 and raw_material == 1 and industrial == 1):
                        #الرسم الجمركي 
                        customs_fee = Decimal('0.0')
                        # محلية محافظة 
                        conservative_locality = Decimal('0.0')
                        #  رسم دعم تنمية الانتاج المحلي 
                        fee_supporting_local_production = Decimal('0.0')
                        #  رسم تأهيل وحماية المدن والمنشاة
                        cities_protection_fee = Decimal('0.0')
                        #  رسم صندوق الجفاف و الكوارث الطبيعية 
                        natural_disaster_fee = Decimal('0.0')
                        #  رسم الترخيص بالاستراد
                        import_license_fee = Decimal('0.0')
                         #  رسم الانفاق 
                        spending_fee = Decimal('0.0')
                        #  رسم السلفة على ضريبة الدخل
                        income_tax_fee = Decimal('0.0')
                        category_price = category_price
                        # رسم القنصلية + غرامة قنصلية
                        if cnsulate == 1:
                            consulate_fee = Decimal('0.0')
                            consulate_tax = Decimal('0.0')
                        elif cnsulate == 0:
                            consulate_fee =  (( price * Decimal('0.015')) + 50)
                            consulate_tax = ((consulate_fee / 2) * dolar)
                        # الرسم النهائي
                        final_fee =  Decimal('0.0')
                        if all(country in countries_arabic for country in [origin, source]):
                        # ضرائب مضافة 
                             added_taxes = total_tax + arabic_stamp
                        # بدل خدمة منح إجازة استراد
                             Granting_import_license = 25000
                        else:
                            # ضرائب مضافة 
                             added_taxes = total_tax 
                        # بدل خدمة منح إجازة استراد
                             Granting_import_license = Decimal('0.0')
                         #رسم تأمين إلزامي
                        insurance_fee = ((total_price_sy * Decimal('0.01'))/12)
                        # رسم طابع
                        stamp_fee =  total_price_sy * Decimal('0.0015') 
                        # ضريبة محلية محافظة
                        provincial_local_tax = ((total_price_sy * Decimal('0.001') ) + ((customs_fee * Decimal('0.1'))) + ((spending_fee + added_taxes + stamp_fee + insurance_fee ) * Decimal('0.05')))
                        # السلفة على ضريبة الدخل 
                        advance_income_tax = (( added_taxes +   provincial_local_tax + stamp_fee + insurance_fee + consulate_tax  ) * tax_fee)
                        # رسم المساهمة الوطنية لإعادة الإعمار
                        reconstruction_fee = (( added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + consulate_tax + final_fee ) * Decimal('0.1') )
                        # مجموع الضرائب النهائي
                        final_taxes = (added_taxes + insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee + Granting_import_license + consulate_tax )
                        # مجموع الرسوم والضرائب
                        final_total = final_taxes + final_fee

                    else:
                        # حساب الرسم الجمركي حسب الاتفاقية العربية
                        if all(country in countries_arabic for country in [origin, source]) and origin != source:
                            customs_fee = insurance * fee
                        elif all(country in countries_arabic for country in [origin, source]) and origin == source:
                            customs_fee = Decimal('0.0')
                        # حساب الرسم الجمركي حسب الاتفاقية الايرانية
                        elif all(country in countries_iran for country in [origin, source]) and origin == source:
                            if fee <= Decimal('0.05'):
                                customs_fee = Decimal('0.01') * insurance
                            else:
                                customs_fee = Decimal('0.04') * insurance
                        #حساب الرسم الجمركي حسب الاتفاقية العامة
                        else:
                            customs_fee = insurance * fee
                        #  محلية عمران
                        #imran_locality = insurance * local_fee
                        # محلية محافظة 
                        conservative_locality = insurance * Decimal('0.001')
                        #  رسم دعم تنمية الانتاج المحلي 
                        fee_supporting_local_production = insurance * support_fee
                        #  رسم تأهيل وحماية المدن والمنشاة
                        cities_protection_fee = insurance * protection_fee
                        #  رسم صندوق الجفاف و الكوارث الطبيعية 
                        natural_disaster_fee = insurance * natural_fee

                        if all(country in countries_arabic for country in [origin, source]):
                        #  رسم الترخيص بالاستراد
                            import_license_fee = insurance * import_fee
                        #  رسم الانفاق 
                            spending_fee = (insurance + import_license_fee) * spending_fee
                        #  رسم السلفة على ضريبة الدخل
                            income_tax_fee = ((insurance + customs_fee + conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + import_license_fee ) * tax_fee )
                        # ضرائب مضافة 
                            added_taxes = total_tax + arabic_stamp
                        # بدل خدمة منح إجازة استراد
                            Granting_import_license = 25000
                        elif  all(country in countries_iran for country in [origin, source]):
                            import_license_fee = 0
                        #  رسم الانفاق 
                            spending_fee = (insurance + customs_fee) * spending_fee
                        #  رسم السلفة على ضريبة الدخل
                            income_tax_fee = ((insurance  + conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + import_license_fee ) * tax_fee )
                        # ضرائب مضافة 
                            added_taxes = total_tax + arabic_stamp
                        # بدل خدمة منح إجازة استراد
                            Granting_import_license = 0
                        else:
                            import_license_fee = 0
                        #  رسم الانفاق 
                            spending_fee = (insurance + customs_fee) * spending_fee
                        #  رسم السلفة على ضريبة الدخل
                            income_tax_fee = ((insurance + customs_fee + conservative_locality + fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + import_license_fee ) * tax_fee )
                        # ضرائب مضافة 
                            added_taxes = total_tax 
                        # بدل خدمة منح إجازة استراد
                            Granting_import_license = 0
                        #رسم الذرة 
                        category_price = category_price
                        # رسم القنصلية + غرامة قنصلية
                        if cnsulate == 1:
                            consulate_fee = Decimal('0.0')
                            consulate_tax = Decimal('0.0')
                        elif cnsulate == 0:
                            consulate_fee =  (( price * Decimal('0.015')) + 50)
                            consulate_tax = ((consulate_fee / 2) * dolar)
                        # الرسم النهائي
                        final_fee = category_price + customs_fee + spending_fee + conservative_locality +fee_supporting_local_production + cities_protection_fee + natural_disaster_fee + income_tax_fee + import_license_fee 
                        # شهادة جمركية
                        #customs_certificate = Decimal('1000.0')
                        #غرامة فاتورة 
                        #bill_tax = Decimal('0.0')
                        #رسم تأمين إلزامي
                        insurance_fee = ((total_price_sy * Decimal('0.01'))/12)
                        # رسم طابع
                        stamp_fee =  total_price_sy * Decimal('0.0015') 
                        # ضريبة محلية محافظة
                        provincial_local_tax = ((total_price_sy * Decimal('0.001') ) + ((customs_fee * Decimal('0.1'))) + ((spending_fee + added_taxes + stamp_fee + insurance_fee ) * Decimal('0.05')))
                        # السلفة على ضريبة الدخل 
                        advance_income_tax = (( added_taxes +   provincial_local_tax + stamp_fee + insurance_fee + consulate_tax  ) * tax_fee)
                        # رسم المساهمة الوطنية لإعادة الإعمار
                        reconstruction_fee = (( added_taxes +  insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + consulate_tax + final_fee ) * Decimal('0.1') )
                        # مجموع الضرائب النهائي
                        final_taxes = (added_taxes + insurance_fee + stamp_fee + provincial_local_tax + advance_income_tax + reconstruction_fee + Granting_import_license + consulate_tax )
                        # مجموع الرسوم والضرائب
                        final_total = final_taxes + final_fee
                    result = {
                        'customs_fee': customs_fee,
                        'conservative_locality': conservative_locality,
                        'fee_supporting_local_production': fee_supporting_local_production,
                        'cities_protection_fee': cities_protection_fee,
                        'natural_disaster_fee': natural_disaster_fee,
                        'import_license_fee': import_license_fee,
                        'income_tax_fee': income_tax_fee,
                        'spending_fee': spending_fee,
                        'category_price': category_price,
                        'consulate_fee': consulate_fee,
                        'consulate_tax': consulate_tax,
                        'final_fee': final_fee,
                        'added_taxes':added_taxes,
                        'insurance_fee':insurance_fee,
                        'stamp_fee':stamp_fee,
                        'Granting_import_license':Granting_import_license,
                        'provincial_local_tax': provincial_local_tax,
                        'advance_income_tax': advance_income_tax,
                        'reconstruction_fee': reconstruction_fee,
                        'final_taxes': final_taxes,
                        'final_total':final_total,
                    }
                    results.append(result)
                except (ValueError, TypeError) as e:
                    return JsonResponse({'error': str(e)}, status=400)
            total_customs_fee = sum(Decimal(result.get('customs_fee', 0)) for result in results)
            total_conservative_locality = sum(Decimal(result.get('conservative_locality', 0)) for result in results)
            total_fee_supporting_local_production = sum(Decimal(result.get('fee_supporting_local_production', 0)) for result in results)
            total_cities_protection_fee = sum(Decimal(result.get('cities_protection_fee', 0)) for result in results)
            total_natural_disaster_fee = sum(Decimal(result.get('natural_disaster_fee', 0)) for result in results)
            total_import_license_fee = sum(Decimal(result.get('import_license_fee', 0)) for result in results)
            total_income_tax_fee = sum(Decimal(result.get('income_tax_fee', 0)) for result in results)
            total_spending_fee = sum(Decimal(result.get('spending_fee', 0)) for result in results)
            total_category_price = sum(Decimal(result.get('category_price', 0)) for result in results)
            total_consulate_fee = sum(Decimal(result.get('consulate_fee', 0)) for result in results)
            total_consulate_tax = sum(Decimal(result.get('consulate_tax', 0)) for result in results)
            total_final_fee = sum(Decimal(result.get('final_fee', 0)) for result in results)
            total_added_taxes = added_taxes
            total_insurance_fee = sum(Decimal(result.get('insurance_fee', 0)) for result in results)
            total_stamp_fee = sum(Decimal(result.get('stamp_fee', 0)) for result in results)
            total_Granting_import_license = sum(Decimal(result.get('Granting_import_license', 0)) for result in results)
            total_provincial_local_tax = sum(Decimal(result.get('provincial_local_tax', 0)) for result in results)
            total_advance_income_tax = sum(Decimal(result.get('advance_income_tax', 0)) for result in results)
            total_reconstruction_fee = sum(Decimal(result.get('reconstruction_fee', 0)) for result in results)
            total_final_taxes = sum(Decimal(result.get('final_taxes', 0)) for result in results)
            total_final_total = sum(Decimal(result.get('final_total', 0)) for result in results)
            final_result = {
                'results': results,
                'total_customs_fee': total_customs_fee,
                'total_conservative_locality': total_conservative_locality,
                'total_fee_supporting_local_production': total_fee_supporting_local_production,
                'total_cities_protection_fee': total_cities_protection_fee,
                'total_natural_disaster_fee': total_natural_disaster_fee,
                'total_import_license_fee': total_import_license_fee,
                'total_income_tax_fee': total_income_tax_fee,
                'total_spending_fee': total_spending_fee,
                'total_category_price': total_category_price,
                'total_consulate_fee': total_consulate_fee,
                'total_consulate_tax': total_consulate_tax,
                'total_final_fee': total_final_fee,
                'total_added_taxes': total_added_taxes,
                'total_insurance_fee': total_insurance_fee,
                'total_stamp_fee': total_stamp_fee,
                'total_Granting_import_license': total_Granting_import_license,
                'total_provincial_local_tax': total_provincial_local_tax,
                'total_advance_income_tax': total_advance_income_tax,
                'total_reconstruction_fee': total_reconstruction_fee,
                'total_final_taxes': total_final_taxes,
                'total_final_total': total_final_total,
            }
            return JsonResponse(final_result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)