from django.core.management.base import BaseCommand
from todos.models import Todo
from todos.utils import gerar_embedding


class Command(BaseCommand):
    help = 'Atualiza os embeddings das perguntas já cadastradas no banco de dados'

    def handle(self, *args, **kwargs):
        # Busca perguntas sem embedding
        todos = Todo.objects.filter(embedding__isnull=True)

        for todo in todos:
            # Gera o embedding somente com a pergunta
            embedding = gerar_embedding(todo.pergunta)
            todo.embedding = embedding  # Atribui o embedding ao objeto
            todo.save()  # Salva as alterações no banco de dados
            self.stdout.write(self.style.SUCCESS(
                f'Embedding atualizado para: {todo.pergunta}'))

        self.stdout.write(self.style.SUCCESS(
            'Todos os embeddings foram atualizados com sucesso!'))
