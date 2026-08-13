# telecomcomplaints/admin.py
from django.contrib import admin
from django.urls import path
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import Complaint


from django.contrib.auth.models import User

class NCCAdminSite(admin.AdminSite):
    site_header = "MTN Complaint System Admin"
    site_title = "MTN Admin Portal"
    index_title = "Welcome to MTN Complaint Management Admin"
    index_template = "admin/custom_index.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "complaints-by-location/",
                self.admin_view(self.complaints_by_location),
                name="complaints_by_location"
            ),
        ]
        return custom_urls + urls

    def complaints_by_location(self, request):
        # ✅ Only include these categories
        allowed_types = ["Call Drop", "SMS Failure", "Slow Internet", "No Network"]

        # Query filtered complaints only in allowed types
        data = (
            Complaint.objects.filter(service_type__in=allowed_types)
            .values("location_area", "service_type")
            .annotate(total=Count("id"))
            .order_by("location_area", "service_type")
        )

        # Collect unique locations
        locations = sorted(set(d["location_area"] or "Unknown" for d in data))

        # Use only allowed service types
        service_types = allowed_types  

        # Initialize dataset map
        dataset_map = {stype: [0] * len(locations) for stype in service_types}

        # Fill dataset
        for d in data:
            loc = d["location_area"] or "Unknown"
            stype = d["service_type"]
            dataset_map[stype][locations.index(loc)] = d["total"]

        context = dict(
            self.each_context(request),
            title="Complaints by Location and Type",
            locations=locations,
            service_types=service_types,
            dataset_map=dataset_map,
        )
        return TemplateResponse(request, "admin/complaints_by_location.html", context)

    def each_context(self, request):
        context = super().each_context(request)
        context['css_files'] = ['/static/css/admin.css']
        context['custom_links'] = [
            {'url': '/admin/complaints-by-location/', 'label': '📊 Complaints by Location'},
        ]
        return context


    




    



# Custom Admin Site instance
admin_site = NCCAdminSite(name='ncc_admin')


class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'service_type', 'status',
        'phone_number', 'submitted_at',
        'colored_status', 'location_link'
    )
    list_filter = ('status', 'service_type', 'location_area', 'submitted_at')
    search_fields = ('user__username', 'email', 'phone_number', 'description')
    ordering = ('-submitted_at',)
    list_per_page = 20
    list_editable = ('status',)

    def location_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">View on Map</a>', url)
        return "-"
    location_link.short_description = "Location"

    def colored_status(self, obj):
        colors = {
            'Pending': 'red',
            'In Progress': 'orange',
            'Resolved': 'green',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color:white; background:{}; padding:4px 8px; border-radius:4px;">{}</span>',
            color, obj.status
        )
    colored_status.short_description = "Status"


# Register model with your custom NCC admin site
admin_site.register(Complaint, ComplaintAdmin)



# Register built-in models to your custom admin site
admin_site.register(User)



