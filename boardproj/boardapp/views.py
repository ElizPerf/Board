from datetime import datetime

from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest, request
from django.shortcuts import redirect, render, get_object_or_404

from boardproj.settings import DEFAULT_FROM_EMAIL
from .models import Notice, Response
from .forms import NoticeForm


class NoticesList(ListView):
    model = Notice
    ordering = '-dateCreation'
    template_name = 'notices/notices.html'
    context_object_name = 'notices'
    paginate_by = 2


class NoticesListProfile(ListView):
    model = Notice
    template_name = 'profile/notices_profile.html'
    context_object_name = 'notices_profile'
    ordering = '-dateCreation'
    paginate_by = 2

    def get_queryset(self):
        return Notice.objects.filter(author=self.request.user)


class NoticeDetail(DetailView):
    model = Notice
    template_name = 'notices/notice.html'
    context_object_name = 'notice'
    pk_url_kwarg = 'notice_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice = self.get_object()
        responses = Response.objects.filter(notice=notice)
        context['responses'] = responses
        return context


@login_required
def profile(request):
    notices = Notice.objects.filter(author=request.user)
    responses = Response.objects.filter(notice__in=notices)
    selected_notice_id = request.GET.get('notice_id')
    if selected_notice_id:
        responses = responses.filter(notice_id=selected_notice_id)

    return render(request, 'profile/responses_profile.html', {'notices': notices, 'responses': responses})


def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice_item = form.save(commit=False)
            notice_item.request = request
            notice_item.save()
            return redirect('notices_profile')
    else:
        form = NoticeForm()
    return render(request, 'notices/notice_form.html', {'form': form})


def notice_edit(request, notice_id=None):
    item = get_object_or_404(Notice, id=notice_id)
    form = NoticeForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('notices_profile')
    return render(request, 'notices/notice_form.html', {'form': form})


def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        notice.delete()
        return redirect('notices_profile')

    return render(request, 'notices/notice_delete.html', {'notice': notice})


@login_required
def response_create(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        response = Response(author=request.user, notice=notice, text=text)
        response.save()

        subject = 'New response on notice'
        message = f'New response on notice: {notice.title}'
        from_email = DEFAULT_FROM_EMAIL
        to_email = notice.author.email
        send_mail(subject, message, from_email, [to_email])

        return HttpResponseRedirect('/notices/{}'.format(notice_id))

    return render(request, 'response_create.html', {'notice': notice})


@login_required
def response_status(request, response_id, action):
    response = get_object_or_404(Response, id=response_id)
    if action == 'accept':
        response.status = 'accepted'
        subject = 'Your response was accepted'
        message = f'Your response on notice was "{response.notice.title}" accepted'
    elif action == 'reject':
        response.status = 'rejected'
        subject = 'Your response was rejected'
        message = f'Your response on notice was "{response.notice.title}" rejected'
    else:
        return HttpResponseBadRequest('Wrong action')

    response.save()

    from_email = DEFAULT_FROM_EMAIL
    to_email = response.author.email
    send_mail(subject, message, from_email, [to_email])

    return redirect('post', post_id=response.post.id)