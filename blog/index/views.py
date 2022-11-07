from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


class PostListView(ListView):
    tag = None
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'index/post/list.html'

    def get_queryset(self):
        try:
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.filter(tags__in=[tag])
        except KeyError:
            return Post.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            slug = self.kwargs['tag_slug']
        except KeyError:
            return context
        context['tag'] = Tag.objects.get(slug=slug)
        return context


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status='published', publish__year=year, publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'index/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


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
