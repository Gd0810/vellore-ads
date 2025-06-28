from django.contrib import admin
from django import forms
from .models import Category, Location, Business, Enquiry, Leads, Review

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class BusinessAdminForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only leaf-node categories
        self.fields['business_type'].queryset = Category.objects.filter(children__isnull=True)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('reviewer', 'rating', 'comment', 'created_at')
    can_delete = False


class EnquiryInline(admin.TabularInline):
    model = Enquiry
    extra = 0
    readonly_fields = ('enquired_person', 'message', 'created_at', 'updated_at')
    can_delete = False


class BusinessAdmin(admin.ModelAdmin):
    form = BusinessAdminForm  # 👈 Add this line
    list_display = ('business_name', 'business_district', 'business_type', 'business_contact', 'active', 'premium', 'trusted', 'verified', 'views_count','top_rank')
    list_filter = ('active', 'premium', 'trusted', 'verified', 'business_type', 'business_district','top_rank')
    search_fields = ('business_name', 'business_contact', 'business_whatsapp', 'slug')  # <-- change here
    prepopulated_fields = {'slug': ('business_name',)}  # <-- change here
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    fieldsets = (
        ("Owner", {
            'fields': ('user',)
        }),
        ("Basic Details", {
            'fields': (
                'business_name', 'slug', 'business_type', 'business_district',
                'business_description', 'business_address', 'business_since'
            )
        }),
        ("Contact Info", {
            'fields': (
                'business_contact', 'business_whatsapp',
                'business_mail', 'business_website'
            )
        }),
        ("Location", {
            'fields': ('business_location',)
        }),
        ("Images", {
            'fields': (('business_image_1', 'business_logo', 'business_image_2', 'business_image_3',
                'business_image_4', 'business_image_5'),
            )
        }),
        ("Social Media", {
            'fields': (
                'business_instagram_link', 'business_facebook_link',
                'business_youtube_link', 'business_x_link'
            )
        }),
        ("Status & Rank", {
            'fields': (
                ('active', 'premium', 'trusted', 'verified','is_top_in_category'),
                ('top_rank', 'views_count'),
            )
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    inlines = [ReviewInline, EnquiryInline]



class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('enquired_person', 'enquired_business', 'created_at')
    search_fields = ('enquired_person__username', 'enquired_business__business_name')
    readonly_fields = ('created_at', 'updated_at')


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('visited_person', 'visited_business', 'created_at')
    search_fields = ('visited_person__username', 'visited_business__business_name')
    readonly_fields = ('created_at',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'business', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__username', 'business__business_name')
    readonly_fields = ('created_at',)
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Leads, LeadsAdmin)
admin.site.register(Review, ReviewAdmin)
