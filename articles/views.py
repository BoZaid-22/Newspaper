#LoginRequiredMixin module used to restrict access to urls only login users
#UserPasses module used to restrict access to edit or delete anly own articles not other users articles
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic import ListView, DetailView
#this module to create, update and delelete articles
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article
#this module to redirect user to article list after delete any article
from django.urls import reverse_lazy

# Create your views here.

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'article_edit.html'
    fields = (
        'title',
        'body',
    )
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = (
        'title',
        'body',
    )
   #this method to set the author of article as the current user who is login outomaicly
    def form_valid(self,form):  
       form.instance.author = self.request.user
       return super().form_valid(form)