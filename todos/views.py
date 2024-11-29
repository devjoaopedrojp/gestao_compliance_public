from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q 
from .models import Todo
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import torch
from sentence_transformers import util
from .utils import gerar_embedding


class TodoListView(ListView):
    model = Todo
    template_name = "todos/todo_list.html"
    context_object_name = 'todo_list'

    def get_queryset(self):
        query = self.request.GET.get("search")
        cliente_selecionado = self.request.GET.get("cliente")

        # Carrega o queryset inicial
        todos = Todo.objects.all()

        # Filtrar por cliente
        if cliente_selecionado:
            todos = todos.filter(cliente=cliente_selecionado)

        # Filtro de busca por pergunta
        if query:
            query_embedding = gerar_embedding(query)
            todos = todos.exclude(embedding=None)
            resultados = []

            for todo in todos:
                embedding = torch.tensor(todo.embedding)
                similaridade = util.cos_sim(query_embedding, embedding).item()
                if todo.pergunta.strip().lower() == query.strip().lower():
                    similaridade += 0.3
                resultados.append((todo, similaridade))

            resultados = sorted(resultados, key=lambda x: x[1], reverse=True)
            todos = [item[0] for item in resultados[:20]]

        return todos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get("search", "")
        context['clientes_unicos'] = Todo.objects.values_list(
            "cliente", flat=True).distinct()
        context['cliente_selecionado'] = self.request.GET.get("cliente", "")
        return context


class TodoCreateView(CreateView):
    model = Todo
    fields = ["pergunta", "resposta", "cliente"]
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        # Gerar embedding somente com a pergunta
        form.instance.embedding = gerar_embedding(
            form.instance.pergunta)  
        messages.success(self.request, "Pergunta criada com sucesso!")
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["pergunta", "resposta", "cliente"]
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        # Gerar embedding atualizado somente com a pergunta
        form.instance.embedding = gerar_embedding(
            form.instance.pergunta)  
        messages.success(self.request, "Pergunta atualizada com sucesso!")
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy("todo_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})  # Retorna um JSON de sucesso


class TodoLoginView(LoginView):
    template_name = "todos/login.html"
    redirect_authenticated_user = False  # Não redireciona automaticamente

    def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Altere para a URL desejada após o login
                return redirect('todos:lista')
            else:
                return render(request, 'todos/login.html', {'error': 'Usuário ou senha inválidos.'})
        return render(request, 'todos/login.html')