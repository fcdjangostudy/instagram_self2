from django import forms

from ..models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        author = kwargs.get('author', None)
        if author is None:
            author = self.instance.author

        post = kwargs.get('post', None)

        if post is None:
            post = self.instance.post

        self.instance.author = author
        self.instance.post = post

        return super().save(commit)