# import django_filters
# from django.db.models import Q
# from .models import Section, Chapter, Sub_Chapter, Fee

# class CustomFilter(django_filters.FilterSet):
#     custom_filter = django_filters.CharFilter(method='filter_custom')

#     class Meta:
#         model = Section  # You can use any model here; it's just a placeholder.
#         fields = []

#     def filter_custom(self, queryset, name, value):
#         # Check if the input value consists of digits only
#         if value.isdigit():
#             # Filter by IDs for all relevant models
#             return queryset.filter(
#                 Q(id__icontains=value) |
#                 Q(chapter__id__icontains=value) |
#                 Q(sub_chapter__id__icontains=value) |
#                 Q(fee__id__icontains=value)
#             )
#         else:
#             # Filter by label or name for all relevant models
#             return queryset.filter(
#                 Q(label__icontains=value) |
#                 Q(name__icontains=value) |
#                 Q(chapter__label__icontains=value) |
#                 Q(chapter__name__icontains=value) |
#                 Q(sub_chapter__label__icontains=value) |
#                 Q(sub_chapter__name__icontains=value) |
#                 Q(fee__label__icontains=value) |
#                 Q(fee__name__icontains=value)
#             )
