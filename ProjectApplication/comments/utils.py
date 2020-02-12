from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from comments.forms.attachment import AttachmentForm
from comments.forms.comment import CommentForm


def adds_comment_attachment_forms(context, submit_viewname, parent_id, comment_category_queryset, attachment_category_queryset):
    context[CommentForm.FORM_NAME] = CommentForm(form_action=reverse(submit_viewname,
                                                                     kwargs={'id': parent_id}),
                                                 category_queryset=comment_category_queryset,
                                                 prefix=CommentForm.FORM_NAME)

    context[AttachmentForm.FORM_NAME] = AttachmentForm(form_action=reverse(submit_viewname,
                                                                           kwargs={'id': parent_id}),
                                                       category_queryset=attachment_category_queryset,
                                                       prefix=AttachmentForm.FORM_NAME)


def process_comment_attachment(request, context, submit_viewname, submit_viewname_repost, form_with_errors_template, parent):
    if 'comment_form_submit' in request.POST:
        proposal_comment_form = CommentForm(request.POST, form_action=reverse(submit_viewname,
                                                                              kwargs={'id': parent.id}),
                                            prefix=CommentForm.FORM_NAME,
                                            category_queryset=parent.comment_object().category_queryset())
        proposal_attachment_form = AttachmentForm(form_action=reverse(submit_viewname,
                                                                      kwargs={'id': parent.id}),
                                                  category_queryset=parent.attachment_object().category_queryset(),
                                                  prefix=AttachmentForm.FORM_NAME)

        if proposal_comment_form.is_valid():
            proposal_comment_form.save(parent, request.user)

            messages.success(request, 'Comment saved')
            return redirect(reverse(submit_viewname, kwargs={'id': parent.id}))
        else:
            context[CommentForm.FORM_NAME] = proposal_comment_form

    elif 'attachment_form_submit' in request.POST:
        proposal_comment_form = CommentForm(form_action=reverse(submit_viewname_repost,
                                                                kwargs={'id': parent.id}),
                                            prefix=CommentForm.FORM_NAME,
                                            category_queryset=parent.comment_object().category_queryset())

        proposal_attachment_form = AttachmentForm(request.POST, request.FILES,
                                                  form_action=reverse(submit_viewname_repost,
                                                                      kwargs={'id': parent.id}),
                                                  category_queryset=parent.attachment_object().category_queryset(),
                                                  prefix=AttachmentForm.FORM_NAME)

        if proposal_attachment_form.is_valid():
            if proposal_attachment_form.save(parent, request.user):
                messages.success(request, 'Attachment saved')
                return redirect(reverse(submit_viewname, kwargs={'id': parent.id}))
            else:
                messages.error(request, 'Error saving attachment. Try again please.')

    else:
        assert False

    context[AttachmentForm.FORM_NAME] = proposal_attachment_form
    context[CommentForm.FORM_NAME] = proposal_comment_form

    return render(request, form_with_errors_template, context)