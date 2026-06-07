from django.contrib import admin
from .models import Profile, Skill, Project, Service, Experience, Certificate, ContactMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone', 'location')
    fieldsets = (
        ('General Info', {
            'fields': ('name', 'title', 'logo_text', 'profile_image', 'resume')
        }),
        ('Biographies', {
            'fields': ('bio', 'about_me')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter')
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'percentage')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('percentage',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('featured',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current', 'company')
    list_editable = ('order', 'is_current')
    search_fields = ('role', 'company', 'description')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'order')
    list_filter = ('issuing_organization',)
    list_editable = ('order',)
    search_fields = ('name', 'issuing_organization')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)

