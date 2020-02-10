from django.contrib import admin

import comments.models


class ProposalCommentAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on',)
    ordering = ['proposal', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class CallCommentAdmin(admin.ModelAdmin):
    list_display = ('call', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on',)
    ordering = ['call', 'text', 'created_by', 'created_on', 'modified_by', 'modified_on', ]


class CommentTypeAdmin(admin.ModelAdmin):
    list_display = ('comment_type',)
    ordering = ['comment_type']


class ProposalCommentTypeAdmin(admin.ModelAdmin):
    list_display = ('comment_type', )
    ordering = ['comment_type', ]


admin.site.register(comments.models.ProposalComment, ProposalCommentAdmin)
admin.site.register(comments.models.CallComment, CallCommentAdmin)
admin.site.register(comments.models.CommentType, CommentTypeAdmin)
admin.site.register(comments.models.ProposalCommentType, ProposalCommentTypeAdmin)
