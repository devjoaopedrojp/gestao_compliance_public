from django.db import models


class Documentacao(models.Model):
    nome = models.CharField(
        max_length=255, null=True, blank=True) 
    link = models.URLField()
    palavra_chave = models.JSONField()  # Armazenando as palavras-chave como uma lista
    # Para armazenar os embeddings das palavras-chave
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Todo(models.Model):
    pergunta = models.TextField()
    resposta = models.TextField()
    cliente = models.CharField(
        max_length=255, null=True, blank=True) 
    data_criacao = models.DateTimeField(auto_now_add=True)
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.pergunta
