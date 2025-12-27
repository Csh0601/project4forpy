from django import forms
from .models import BlogPost, Comment, Tag


class BlogPostForm(forms.ModelForm):
    """博客文章表单"""
    # 标签输入框（逗号分隔）
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '输入标签，用逗号分隔（如：Python, Django, Web）'
        }),
        label='标签'
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入文章标题'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '输入文章内容...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            # 处理标签
            tags_str = self.cleaned_data.get('tags_input', '')
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                instance.tags.clear()
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    instance.tags.add(tag)
        return instance


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '写下你的评论...'
            }),
        }
        labels = {'content': ''}
