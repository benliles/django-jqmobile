from django.contrib import admin

from jqmobile.models import Page, HeaderTemplate, FooterTemplate



class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title','slug','body',)}),
        ('Header', {
            'classes': ('collapse',),
            'fields': ('header_template','header_content')}),
        ('Footer', {
            'classes': ('collapse',),
            'fields': ('footer_template','footer_content')}),
        ('Advanced',{
            'classes': ('collapse',),
            'fields': ('embed','attributes','content_attributes',
                       'header_content_attributes',
                       'footer_content_attributes','sites')}))
    list_display = ('slug','title','embed')
    ordering = ('title',)
    list_filter = ('embed',)

admin.site.register(Page, PageAdmin)
admin.site.register(HeaderTemplate)
admin.site.register(FooterTemplate)