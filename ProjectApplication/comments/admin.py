from django.contrib import admin

import comments.models


class ProposalCommentAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on',)
    ordering = ['proposal', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class CallCommentAdmin(admin.ModelAdmin):
    list_display = ('call', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on',)
    ordering = ['call', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    ordering = ['category']


class ProposalCommentCategoryAdmin(admin.ModelAdmin):
    list_display = ('comment_category', )
    ordering = ['comment_category', ]


admin.site.register(comments.models.ProposalComment, ProposalCommentAdmin)
admin.site.register(comments.models.CallComment, CallCommentAdmin)
admin.site.register(comments.models.Category, CategoryAdmin)
admin.site.register(comments.models.ProposalCommentCategory, ProposalCommentCategoryAdmin)
