from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'index/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'index/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read post "{}" on page {}\n\n Comment added by {}: {}'.format(post.title, post_url, cd['name'],
                                                                                     cd['comments'])
            send_mail(subject, message, 'jacek@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'index/post/share.html', {'post': post, 'form': form, 'sent': sent})