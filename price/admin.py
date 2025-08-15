import csv
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from nested_admin import NestedTabularInline, NestedModelAdmin
from .models import PortPrice, Vessel, Price
from Fee_calculator.models import Port  # ✅ Import Port model
from django.utils.safestring import mark_safe
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django import forms
from django.db.models import Q


class PriceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data:
                continue  # Completely untouched form, skip it

            is_deleted = form.cleaned_data.get('DELETE', False)
            container = form.cleaned_data.get('container')

            # Check if the form has any data at all besides delete
            has_any_data = any(
                value not in [None, '', 0]
                for key, value in form.cleaned_data.items()
                if key != 'DELETE'
            )

           
class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['container'].required = False  # Let formset handle the logic
        self.fields['ocean_freight_last_updated'].disabled = True  # 👈 read-only in the form UI

class PriceInline(NestedTabularInline):
    model = Price
    extra = 0
    formset = PriceInlineFormSet  # 👈 This enforces the validation
    readonly_fields = ['ocean_freight_last_updated']  # 👈 Read-only field in admin



# ✅ Inline for Vessel model
class VesselInline(NestedTabularInline):
    model = Vessel
    extra = 0
    inlines = [PriceInline]  # Attach PriceInline inside VesselInline

# ✅ Function to Parse Date Formats Safely
def parse_date(date_str):
    """Convert date formats to YYYY-MM-DD"""
    if not date_str or date_str.strip() == '':
        return None  # ✅ Handle missing dates safely

    date_formats = [
        "%A, %d-%b-%Y",   # ✅ Example: "Friday, 18-APR-2025"
        "%d-%b-%Y",       # ✅ Example: "18-APR-2025"
        "%Y-%m-%d",       # ✅ Example: "2025-04-18"
        "%d-%b %Y, %I:%M %p",  # ✅ Example: "16-MAR 2025, 05:00 PM"
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()  # ✅ Convert to YYYY-MM-DD
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")  # ❌ Raise error if no format matches

# ✅ Function to Remove Country Code from City Names
def clean_city_name(city_with_country):
    """Extract city name before the comma (',')."""
    return city_with_country.split(',')[0].strip() if city_with_country else ''

# ✅ PortPrice Admin with CSV Import

# ✅ Register the Model in Admin


# ------------------------
# Inline Admins
# ------------------------

class PriceInline(NestedTabularInline):
    model = Price
    extra = 0
    form = PriceForm
    formset = PriceInlineFormSet

class VesselInline(NestedTabularInline):
    model = Vessel
    extra = 0
    inlines = [PriceInline]

# ------------------------
# Helper Functions
# ------------------------

def clean_city_name(city_with_country):
    """Extract city name before the comma (e.g. 'Jebel Ali, AE' → 'Jebel Ali')"""
    return city_with_country.split(',')[0].strip() if city_with_country else ''

def parse_date(date_str):
    """Convert date formats to datetime.date"""
    if not date_str or date_str.strip() == '':
        return None
    date_formats = [
        "%A, %d-%b-%Y",            # Friday, 18-APR-2025
        "%d-%b-%Y",                # 18-APR-2025
        "%Y-%m-%d",                # 2025-04-18
        "%d-%b %Y, %I:%M %p",      # 16-MAR 2025, 05:00 PM
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")

# ------------------------
# Admin Class
# ------------------------

class PortPriceAdmin(NestedModelAdmin):
    inlines = [VesselInline]
    list_display = ['station_origin', 'station_delivery']
    list_filter = ['visible']
    search_fields = ['station_origin__name', 'station_delivery__name']
    autocomplete_fields = ['station_origin', 'station_delivery']
    list_filter = ['visible']


    def upload_csv_button(self, obj=None):
        return format_html(
            '<a class="button" href="{}">Upload CSV</a>',
            "/admin/price/portprice/import-csv/"
        )

    upload_csv_button.allow_tags = True
    upload_csv_button.short_description = "Upload CSV"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(visible=True)  # 
    # ✅ Inject upload button into top bar
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['upload_csv_button'] = mark_safe(
            '<a class="addlink" href="import-csv/" style="margin-left: 10px;height:17px; padding-top:6px  ">📂 Upload CSV</a>'
        )
        return super().changelist_view(request, extra_context=extra_context)

    # ✅ Custom CSV upload view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode("utf-8", errors="replace").splitlines()
            reader = list(csv.DictReader(decoded_file))  # 👈 Convert to list for multiple passes
            origin_dest_pairs = set()
            for row in reader:
                origin_name = clean_city_name(row['Origin'])
                destination_name = clean_city_name(row['Destination'])
                origin_dest_pairs.add((origin_name, destination_name))
                q = Q()
                for origin, dest in origin_dest_pairs:
                    q |= Q(station_origin__name=origin, station_delivery__name=dest)
                    PortPrice.objects.filter(q).update(visible=False)
                  
           
            for row in reader:
                try:
                    # ✅ Clean City Names (Remove Country Code)
                    origin_name = clean_city_name(row['Origin'])
                    destination_name = clean_city_name(row['Destination'])

                    # ✅ Get or Create the Ports
                    origin_port, _ = Port.objects.get_or_create(name=origin_name)
                    destination_port, _ = Port.objects.get_or_create(name=destination_name)

                    # ✅ Get or Create the PortPrice instance
                    port_price, _ = PortPrice.objects.get_or_create(
                        station_origin=origin_port,
                        station_delivery=destination_port
                    )
                    port_price.visible = True
                    port_price.save()

                    # ✅ Get or Create the Vessel instance with Validated Date Formats
                    vessel = Vessel.objects.create(
                      port_price=port_price,
                      date=parse_date(row.get('Departure Date', '')),
                      cuttoff_dare=parse_date(row.get('Port cut-off', '')),
                      end_date=parse_date(row.get('Arrival Date', '')),
                      number_of_station=int(row.get('Transhipment', 0)),
                      number_of_day=int(row.get('Transit Time', 0))
)
                    
                    # Create 20FT container if present
                    if row.get('container20ft'):
                         added_20ft = float(row.get('added20ft', 0) or 0)
                         oceanfreight_20ft = float(row.get('oceanfreight20ft', 0) or 0) 
                         Price.objects.create(
                         vessel=vessel,
                         container='20ft',
                         pickup=float(row.get('pickup20ft', 0) or 0),
                         ocean_freight=oceanfreight_20ft,
                         port_of_origin=float(row.get('portoforigin20ft', 0) or 0),
                         port_of_discharge=float(row.get('portofdischarge20ft', 0) or 0),
                         added_value=added_20ft
    ) 

# Create 40HC container if present 
                    if row.get('container40ft'):
                        added_40ft = float(row.get('added40ft', 0) or 0)
                        oceanfreight_40ft = float(row.get('oceanfreight40ft', 0) or 0) 
                        Price.objects.create(
                         vessel=vessel,
                         container='40ft',
                         pickup=float(row.get('pickup40ft', 0) or 0),
                         ocean_freight=oceanfreight_40ft,
                         port_of_origin=float(row.get('portoforigin40ft', 0) or 0),
                         port_of_discharge=float(row.get('portofdischarge40ft', 0) or 0),
                         added_value=added_40ft
)                  
                    if row.get('container40HC'):
                        added_40HC = float(row.get('added40HC', 0) or 0)
                        oceanfreight_40HC = float(row.get('oceanfreight40HC', 0) or 0) 
                        Price.objects.create(
                         vessel=vessel,
                         container='40HC',
                         pickup=float(row.get('container40HC', 0) or 0),
                         ocean_freight=oceanfreight_40HC,
                         port_of_origin=float(row.get('portoforigin40HC', 0) or 0),
                         port_of_discharge=float(row.get('portofdischarge40HC', 0) or 0),
                         added_value=added_40HC 
    )
 
                    # ✅ Create the Price instance
                    # Price.objects.create(
                    #     vessel=vessel,
                    #     container=row.get('Container', ''),
                    #     pickup=float(row.get('Pickup', 0) or 0),
                    #     port_of_origin=float(row.get('Port of Origin', 0) or 0),
                    #     ocean_freight=float(row.get('Ocean Freight', 0) or 0),
                    #     port_of_discharge=float(row.get('Port of Discharge', 0) or 0)
                    # )

                except ValueError as e:
                    self.message_user(request, f"Skipping row due to error: {e}", level="error")
                    continue  # ✅ Skip problematic rows without crashing

            self.message_user(request, "CSV file successfully imported.")
            return HttpResponseRedirect("../")

        return render(request, "admin/csv_upload.html")

# Register admin
admin.site.register(PortPrice, PortPriceAdmin)
