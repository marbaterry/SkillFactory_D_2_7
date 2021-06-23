from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from .models import Post, Category, CategorySubscriber
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, SubsForm
from django.core.mail import send_mail
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class PostList(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-date')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'detailpost.html'
    context_object_name = 'post'


class SearchNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-date')
    paginate_by = 10

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


# @login_required
class SubscriberCreateView(CreateView, ListView):
    model = CategorySubscriber
    template_name = 'result_subscriber.html'
    context_object_name = 'subs'
    form_class = SubsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        user = self.request.user.id
        context['category'] = CategorySubscriber.objects.filter(userTrough=user)
        return context

    def post(self, request):
        form = SubsForm(request.POST)
        if form.is_valid():
            new_sub = CategorySubscriber.objects.create(
                userTrough=User.objects.get(pk=request.user.id),
                classTrough=form.cleaned_data["classTrough"],
            )
            new_sub.save()
            html_content = render_to_string(
                'subsribe_email.html',
                {
                    'new_sub': new_sub,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'test_final',
                body='Test body',  # это то же, что и message
                from_email='marbaterry@yandex.ru',
                to=['marbaterry.crb@gmail.com'],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()
            return redirect('/subscribe')

@login_required
def user_filter(request):
    user = request.user.id
    category = CategorySubscriber.objects.filter(userTrough=user)
    context = {
        "category": category,
    }
    return render(request, "result_subscriber.html", context)



# @login_required
# def SubscriberCreateView(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#
#             form = SubsForm(request.POST)
#
#             for field in form:
#                 print(field.value())
#
#             if form.is_valid():
#                 new_sub = CategorySubscriber.objects.create(
#                     userTrough=User.objects.get(pk=request.user.id),
#                     classTrough=form.cleaned_data["classTrough"],
#                 )
#                 new_sub.save()
#                 send_mail(
#                     subject='New SUBSCRIBE',
#                     # имя клиента и дата записи будут в теме для удобства
#                     message=f'You have new sub - {new_sub.classTrough.name}',  # сообщение с кратким описанием проблемы
#                     from_email='marbaterry@yandex.ru',
#                     # здесь указываете почту, с которой будете отправлять (об этом попозже)
#                     recipient_list=['marbaterry.crb@gmail.com', ]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#                 )
#             else:
#                 print("ERROR : Form is invalid")
#                 print(form.errors)
#     return render(request, 'add_subscriber.html', {
#         'form': SubsForm
#     })
