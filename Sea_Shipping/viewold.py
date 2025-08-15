from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import FeedBack,Contant_us,helper,Booking, Good_Air,Container, Sea_Shipping, Land_Shipping, Air_Freight, Customs_Clearance, Truck
from .serializers import FeedBackSerializer,Contant_usSerializer,HelperSerializer,BookingSerializer, GoodAirSerializer, TruckSerializer, ContainerSerializer, SeaShippingSerializer, LandShippingSerializer, AirFreightSerializer, CustomsClearanceSerializer
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import generics, serializers, status
from django.core.mail import EmailMessage


""" class sendmail(generics.ListCreateAPIView):
    queryset = Sea_Shipping.objects.all()
    serializer_class = SeaShippingSerializer

    def create(self, request, *args, **kwargs):
        # Extract container data from the request data
        containers_data = request.data.pop('containers', [])

        # Validate Sea_Shipping data
        sea_shipping_serializer = self.get_serializer(data=request.data)
        sea_shipping_serializer.is_valid(raise_exception=True)

        # Create Sea_Shipping instance
        sea_shipping_instance = sea_shipping_serializer.save()

        # Create Container instances and associate them with the Sea_Shipping instance
        for container_data in containers_data:
            container_data['sea_shipping'] = sea_shipping_instance.id
            container_serializer = ContainerSerializer(data=container_data)
            container_serializer.is_valid(raise_exception=True)
            container_serializer.save()

        # Send email with details of Sea_Shipping and associated Containers
        self.send_email(sea_shipping_instance, containers_data)

        headers = self.get_success_headers(sea_shipping_serializer.data)
        return Response(sea_shipping_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email(self, sea_shipping_instance, containers_data):
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'

        # Include Sea_Shipping details in the email message
        message = (
    f"We thank you for contacting AcrossMena. We will contact you as soon as possible\n\n"
    f"تفاصيل الشحنة:\n\n"
    f"وزن البضاعة: {sea_shipping_instance.goods_weight}{sea_shipping_instance.goods_unit}\n"
    f"نوع البضاعة: {sea_shipping_instance.goods_type}\n"
    f"نوع الحركة: {sea_shipping_instance.movement_type}\n"
    f"تاريخ الشحنة: {sea_shipping_instance.shipment_date}\n"
    f"عدد الحاويات: {len(containers_data)}\n"
    f"اسم المرسل: {sea_shipping_instance.sender_name}\n"
    f"اسم الشركة: {sea_shipping_instance.company_name}\n"
    f"رقم الهاتف: {sea_shipping_instance.phone_number}\n"
    f"الايميل: {sea_shipping_instance.email}\n"
    f"وصف البضاعة: {sea_shipping_instance.goods_description}\n"
    f"ميناء التحميل: {sea_shipping_instance.loading_address}\n"
    f"ميناء التفريغ: {sea_shipping_instance.discharge_address}"
)

        # Include Container details in the email message
        if containers_data:
            message += "\n\nتفاصيل الحاويات:\n"
            for container_data in containers_data:
                message += f"\nحاوية {container_data['container_number']} - نوع الحاوية: {container_data['container_type']}\n"
                message += f"الطول: {container_data['length']}, العرض: {container_data['width']}, الارتفاع: {container_data['height']}\n"

        recipient_list = ['customer-service@acrossmena.com', sea_shipping_instance.email]

        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False)
class LandShippingListCreateView(generics.ListCreateAPIView):
    queryset = Land_Shipping.objects.all()
    serializer_class = LandShippingSerializer

    def perform_create(self, serializer):
        # Call the serializer's save method to create the instance
        instance = serializer.save()

        # Convert the serialized data to JSON
        serialized_data = LandShippingSerializer(instance).data

        # Send an email with the information to the fixed email address
        fixed_recipient = 'customer-service@acrossmena.com'
         
        # Send an email with the information
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'
        message = f"We thank you for contacting AcrossMena. We will contact you as soon as possible\n\nتفاصيل الشحنة:\n\nوزن البضاعة: {serialized_data['goods_weight']}\nنوع البضاعة: {serialized_data['goods_type']}\nنوع الطرد: {serialized_data['package_type']}\nعدد الطرود: {serialized_data['number_package']}\nعنوان التحميل: {serialized_data['loading_address']}\nعنوان التفريغ: {serialized_data['discharge_address']}\nنوع الشاحنة: {serialized_data['truck_type']}\nتاريخ الشحنة: {serialized_data['shipment_date']}\nاسم المرسل: {serialized_data['sender_name']}\nاسم الشركة: {serialized_data['company_name']}\nرقم الهاتف: {serialized_data['phone_number']}\nالايميل: {serialized_data['email']}"
        recipient_list = [fixed_recipient, serialized_data['email']]

        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




class AirFreightListCreateView(generics.ListCreateAPIView):
    queryset = Air_Freight.objects.all()
    serializer_class = AirFreightSerializer

    def perform_create(self, serializer):
        # Call the serializer's save method to create the instance
        instance = serializer.save()

        # Convert the serialized data to JSON
        serialized_data = AirFreightSerializer(instance).data
        fixed_recipient = 'customer-service@acrossmena.com'
        # Send an email with the information
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'
        message = f"We thank you for contacting AcrossMena. We will contact you as soon as possible\n\nتفاصيل الشحنة:\n\nوزن البضاعة: {serialized_data['goods_weight']}\nنوع البضاعة: {serialized_data['goods_type']}\nنوع الطرد: {serialized_data['package_type']}\nعدد الطرد: {serialized_data['number_package']}\nنوع الحركة: {serialized_data['movement_type']}\nتاريخ الشحنة: {serialized_data['shipment_date']}\nعنوان التحميل: {serialized_data['loading_address']}\nعنوان التفريغ: {serialized_data['discharge_address']}\nعرض الطرد: {serialized_data['Package_width']}\nارتفاع الطرد: {serialized_data['Package_height']}\nطول الطرد: {serialized_data['Package_length']}\nاسم المرسل: {serialized_data['sender_name']}\nاسم الشركة: {serialized_data['company_name']}\nرقم الهاتف: {serialized_data['phone_number']}\nالايميل: {serialized_data['email']}"
        recipient_list = [fixed_recipient, serialized_data['email']]
te
        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CustomsClearanceListCreateView(generics.ListCreateAPIView):
    queryset = Customs_Clearance.objects.all()
    serializer_class = CustomsClearanceSerializer

    def perform_create(self, serializer):
        # Call the serializer's save method to create the instance
        instance = serializer.save()

        # Convert the serialized data to JSON
        serialized_data = CustomsClearanceSerializer(instance).data
        fixed_recipient = 'customer-service@acrossmena.com'
        # Send an email with the information
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'
        message = f"We thank you for contacting AcrossMena. We will contact you as soon as possible\n\nتفاصيل الشحنة:\n\nوزن البضاعة: {serialized_data['goods_weight']}\nنوع البضاعة: {serialized_data['goods_type']}\nنوع الطرد: {serialized_data['package_type']}\nعدد الطرود: {serialized_data['number_package']}\nنوع الشحن: {serialized_data['shipment_type']}\nنوع وسيلة النقل: {serialized_data['transportation_type']}\nالمصدر: {serialized_data['origin']}\nالوجهة: {serialized_data['destination']}\nموقع التخليص: {serialized_data['clearance_location']}\nاسم المرسل: {serialized_data['sender_name']}\nاسم الشركة: {serialized_data['company_name']}\nرقم الهاتف: {serialized_data['phone_number']}\nالايميل: {serialized_data['email']}"
        recipient_list = [fixed_recipient, serialized_data['email']]

        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED) """

# new


class SeaShippingListCreateView(generics.ListCreateAPIView):
    queryset = Sea_Shipping.objects.all()
    serializer_class = SeaShippingSerializer

    def create(self, request, *args, **kwargs):
        mutable_request_data = request.data.copy()
        containers_data = mutable_request_data.pop('containers', [])
        sea_shipping_serializer = self.get_serializer(data=mutable_request_data)
        sea_shipping_serializer.is_valid(raise_exception=True)
        sea_shipping_instance = sea_shipping_serializer.save()

        # Sending email to sea_shipping_instance.email
        self.send_email(sea_shipping_instance.email, sea_shipping_instance, containers_data, 'email_template.html')

        # Sending email to other recipients
        other_recipients = ['customer-service@acrossmena.com']
        for recipient_email in other_recipients:
            self.send_email(recipient_email, sea_shipping_instance, containers_data, 'email_template2.html')

        headers = self.get_success_headers(sea_shipping_serializer.data)
        return Response(sea_shipping_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email(self, recipient_email, sea_shipping_instance, containers_data, template_name):
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'
        context = {
            'goods_weight': sea_shipping_instance.goods_weight,
            'goods_unit': sea_shipping_instance.goods_unit,
            'goods_type': sea_shipping_instance.goods_type,
            'movement_type': sea_shipping_instance.movement_type,
            'shipment_date': sea_shipping_instance.shipment_date,
            'sender_name': sea_shipping_instance.sender_name,
            'company_name': sea_shipping_instance.company_name,
            'phone_number': sea_shipping_instance.phone_number,
            'email': sea_shipping_instance.email,
            'goods_description': sea_shipping_instance.goods_description,
            'loading_address': sea_shipping_instance.loading_address,
            'discharge_address': sea_shipping_instance.discharge_address,
            'containers_data': containers_data,
        }
        if containers_data:
            container_details_html = ""
            for container_data in containers_data:
                container_details_html += str(container_data['container_number'])
                container_details_html += str(container_data['container_type'])
                container_details_html += str(container_data['length'])
                container_details_html += str(container_data['width'])
                container_details_html += str(container_data['height'])
            context['container_details'] = container_details_html
        message = render_to_string(template_name, context)
        recipient_list = [recipient_email]
        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False, html_message=message)
        return JsonResponse({'message': 'Email sent successfully.'})



    # land 

class LandShippingListCreateView(generics.ListCreateAPIView):
    queryset = Land_Shipping.objects.all()
    serializer_class = LandShippingSerializer

    def create(self, request, *args, **kwargs):
        mutable_request_data = request.data.copy()
        trucks_data = mutable_request_data.pop('trucks', [])
        land_shipping_serializer = self.get_serializer(data=mutable_request_data)
        land_shipping_serializer.is_valid(raise_exception=True)
        land_shipping_instance = land_shipping_serializer.save()

        # Sending email to land_shipping_instance.email
        self.send_email(land_shipping_instance.email, land_shipping_instance, trucks_data, 'email_template_land.html')

        # Sending email to other recipients
        other_recipients = ['customer-service@acrossmena.com']
        for recipient_email in other_recipients:
            self.send_email(recipient_email, land_shipping_instance, trucks_data, 'email_template_land2.html')

        headers = self.get_success_headers(land_shipping_serializer.data)
        return Response(land_shipping_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email(self, recipient_email, land_shipping_instance, trucks_data, template_name):
        subject = 'We thank you for contacting AcrossMena. We will contact you as soon as possible'
        context = {
            'goods_weight': land_shipping_instance.goods_weight,
            'goods_unit': land_shipping_instance.goods_unit,
            'goods_type': land_shipping_instance.goods_type,
            'shipment_date': land_shipping_instance.shipment_date,
            'sender_name': land_shipping_instance.sender_name,
            'company_name': land_shipping_instance.company_name,
            'phone_number': land_shipping_instance.phone_number,
            'email': land_shipping_instance.email,
            'goods_description': land_shipping_instance.goods_description,
            'loading_address': land_shipping_instance.loading_address,
            'discharge_address': land_shipping_instance.discharge_address,
            'trucks_data': trucks_data,
        }
        if trucks_data:
            truck_details_html = ""
            for truck_data in trucks_data:
                truck_details_html += str(truck_data['truck_number'])
                truck_details_html += str(truck_data['truck_type'])
            context['truck_details'] = truck_details_html
        message = render_to_string(template_name, context)
        recipient_list = [recipient_email]
        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False, html_message=message)
        return JsonResponse({'message': 'Email sent successfully.'})


# Air

class AirFreightListCreateView(generics.ListCreateAPIView):
    queryset = Air_Freight.objects.all()
    serializer_class = AirFreightSerializer

    def create(self, request, *args, **kwargs):
        mutable_request_data = request.data.copy()
        goods_data = mutable_request_data.pop('good_air', [])

        air_freight_serializer = self.get_serializer(data=mutable_request_data)
        air_freight_serializer.is_valid(raise_exception=True)

        air_freight_instance = air_freight_serializer.save()

        for good_data in goods_data:
            good_data['air_freight'] = air_freight_instance.id
            good_air_serializer = GoodAirSerializer(data=good_data)
            good_air_serializer.is_valid(raise_exception=True)
            good_air_serializer.save()

        # Sending email to air_freight_instance.email
        self.send_email(air_freight_instance, goods_data, 'email_template_air.html')

        # Sending email to other recipients
        self.send_other_emails(air_freight_instance, goods_data)

        headers = self.get_success_headers(air_freight_serializer.data)
        return Response(air_freight_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email(self, air_freight_instance, goods_data, template_name):
        subject = 'Thank you for choosing our air freight service'

        context = {
            'movement_type': air_freight_instance.movement_type,
            'loading_address': air_freight_instance.loading_address,
            'discharge_address': air_freight_instance.discharge_address,
            'sender_name': air_freight_instance.sender_name,
            'company_name': air_freight_instance.company_name,
            'phone_number': air_freight_instance.phone_number,
            'email': air_freight_instance.email,
            'actual_weight': air_freight_instance.actual_weight,
            'volumetric_weight': air_freight_instance.volumetric_weight,
            'goods_data': goods_data,
        }

        if goods_data:
            goods_details_html = ""
            for good_data in goods_data:
                goods_details_html += f"{good_data['goods_type']} - {good_data['goods_weight']} - {good_data['number_package']}\n"

            context['goods_details'] = goods_details_html

        message = render_to_string(template_name, context)

        recipient_list = [air_freight_instance.email]

        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False, html_message=message)

    def send_other_emails(self, air_freight_instance, goods_data):
        subject = 'Thank you for choosing our air freight service'
        context = {
            'movement_type': air_freight_instance.movement_type,
            'loading_address': air_freight_instance.loading_address,
            'discharge_address': air_freight_instance.discharge_address,
            'sender_name': air_freight_instance.sender_name,
            'company_name': air_freight_instance.company_name,
            'phone_number': air_freight_instance.phone_number,
            'email': air_freight_instance.email,
            'actual_weight': air_freight_instance.actual_weight,
            'volumetric_weight': air_freight_instance.volumetric_weight,
            'goods_data': goods_data,
        }

        if goods_data:
            goods_details_html = ""
            for good_data in goods_data:
                goods_details_html += f"{good_data['goods_type']} - {good_data['goods_weight']} - {good_data['number_package']}\n"

            context['goods_details'] = goods_details_html

        message = render_to_string('email_template_air2.html', context)

        recipient_list = ['customer-service@acrossmena.com']

        send_mail(subject, message, 'acroifcn@across-mena.com', recipient_list, fail_silently=False, html_message=message)

        
import os
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        # Validate and save the booking
        booking_serializer = self.get_serializer(data=request.data)
        booking_serializer.is_valid(raise_exception=True)
        booking_instance = booking_serializer.save()

        # Send the confirmation email
        self.send_confirmation_email(booking_instance)

        headers = self.get_success_headers(booking_serializer.data)
        return Response(booking_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_confirmation_email(self, booking_instance):
        subject = 'Booking Request'
        from_email = 'acroifcn@across-mena.com'
        recipient_list = ['tech@acrossmena.com', booking_instance.email]

        # Prepare the context for the email template
        context = {
            'direction': booking_instance.direction,
            'shipping_service': booking_instance.shipping_service,
            'date': booking_instance.date,
            'end_date': booking_instance.end_date,
            'number_of_day': booking_instance.number_of_day,
            'commodity': booking_instance.commodity,
            'commodity_description': booking_instance.commodity_description,
            'containers_details': booking_instance.containers_details,
            'reference_number': booking_instance.reference_number,
            'email': booking_instance.email,
            'phone_number':booking_instance.phone_number,
            'full_name':booking_instance.full_name,
            'contact_method':booking_instance.contact_method,
            'weight':booking_instance.weight,
            'station_origin':booking_instance.station_origin,
            'station_delivery':booking_instance.station_delivery,
            'port_of_origin':booking_instance.port_of_origin,
            'port_of_destination':booking_instance.port_of_destination,
            'book_code':booking_instance.book_code,
            'total_price':booking_instance.total_price,
            
        }
        # Render the HTML content of the email
        html_message = render_to_string('booking_confirmation_email.html', context)
        text_message = strip_tags(html_message)  # Generate a plain-text version of the email

        # Create the email object
        email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")

        # Attach the company logo image inline using MIMEImage
        logo_path = os.path.join(settings.BASE_DIR, 'static/Sea_Shipping/images/company_logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<logo>')
                email.attach(mime_image)

        # Log the email status and send it
        try:
            email.send(fail_silently=False)
            print('Email sent successfully to:', recipient_list)
        except Exception as e:
            print(f'Error sending email: {e}')
            return JsonResponse({'message': f'Error sending email: {e}'}, status=500)

        return JsonResponse({'message': 'Email sent successfully.'})



class HelperListCreateView(generics.ListCreateAPIView):
    queryset = helper.objects.all()
    serializer_class = HelperSerializer

    def create(self, request, *args, **kwargs):
        helper_serializer = self.get_serializer(data=request.data)
        helper_serializer.is_valid(raise_exception=True)
        helper_instance = helper_serializer.save()

        self.send_confirmation_email(helper_instance)

        headers = self.get_success_headers(helper_serializer.data)
        return Response(helper_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_confirmation_email(self, helper_instance):
        subject = 'Support Request'
        
        # Prepare the context for the email template
        context = {
            'sender_name': helper_instance.sender_name,
            'phone_number': helper_instance.phone_number,
            'email': helper_instance.email,
            'Communication_method': helper_instance.Communication_method,
        }

        # Render the HTML content of the email
        html_message = render_to_string('helper_email.html', context)
        text_message = strip_tags(html_message)  # Generate a plain-text version of the email

        # Create the email object
        recipient_list = ['tech@acrossmena.com', helper_instance.email]
        email = EmailMultiAlternatives(subject, text_message, 'acroifcn@across-mena.com', recipient_list)
        email.attach_alternative(html_message, "text/html")

        # Attach the company logo image inline using MIMEImage
        logo_path = os.path.join(settings.BASE_DIR, 'static/Sea_Shipping/images/company_logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<logo>')  # Setting the Content-ID for inline image
                email.attach(mime_image)

        # Log the email status and send it
        try:
            email.send(fail_silently=False)
            print(f'Email sent successfully to: {recipient_list}')
        except Exception as e:
            print(f'Error sending email: {e}')
            return JsonResponse({'message': f'Error sending email: {e}'}, status=500)

        return JsonResponse({'message': 'Email sent successfully.'})

class Contant_usListCreateView(generics.ListCreateAPIView):
    queryset = Contant_us.objects.all()
    serializer_class = Contant_usSerializer

    def create(self, request, *args, **kwargs):
        Contant_us_serializer = self.get_serializer(data=request.data)
        Contant_us_serializer.is_valid(raise_exception=True)
        Contant_us_instance = Contant_us_serializer.save()

        self.send_confirmation_email(Contant_us_instance)

        headers = self.get_success_headers(Contant_us_serializer.data)
        return Response(Contant_us_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_confirmation_email(self, Contant_us_instance):
        subject = 'Contant_us Confirmation'

        context = {

            'sender_name': Contant_us_instance.sender_name,
            'phone_number': Contant_us_instance.phone_number,
            'email': Contant_us_instance.email,
            'massage': Contant_us_instance.massage,
        }

        html_message = render_to_string('Contant_us_email.html', context)
        recipient_list = ['customer-service@acrossmena.com', Contant_us_instance.email]
        email = EmailMessage(
         subject=subject,
         body=' ',  # plain text fallback
         from_email='customer-service@acrossmena.com',
         to=recipient_list,
         reply_to=['customer-service@acrossmena.com']  # force reply to your support address
    )
        email.content_subtype = "html"  # specify the email content type is HTML
        email.body = html_message  # set the HTML content
        email.send(fail_silently=False)
        # send_mail(subject, ' ', 'customer-service@acrossmena.com', recipient_list, fail_silently=False, html_message=html_message)

        return JsonResponse({'message': 'Confirmation email sent successfully.'})
        
        

class FeedBackListCreateView(generics.ListCreateAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer

    def create(self, request, *args, **kwargs):
        FeedBack_serializer = self.get_serializer(data=request.data)
        FeedBack_serializer.is_valid(raise_exception=True)
        FeedBack_instance = FeedBack_serializer.save()

        self.send_confirmation_email(FeedBack_instance)

        headers = self.get_success_headers(FeedBack_serializer.data)
        return Response(FeedBack_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_confirmation_email(self, FeedBack_instance):
        subject = 'FeedBack Confirmation'

        context = {
            'sender_name': FeedBack_instance.sender_name,
            'problem': FeedBack_instance.problem,
            'email': FeedBack_instance.email,
            'massage': FeedBack_instance.massage,
            'description':FeedBack_instance.description,
            'Tab_name':FeedBack_instance.Tab_name,
            'Field_type':FeedBack_instance.Field_type
        }

        html_message = render_to_string('FeedBack.html', context)
        recipient_list = ['customer-service@acrossmena.com', FeedBack_instance.email]

        send_mail(subject, ' ', 'acroifcn@across-mena.com', recipient_list, fail_silently=False, html_message=html_message)
