from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return password_confirm



from .models import Group, Comment

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description','user_name', 'image']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']



from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "text"]

# Проверяем, есть ли в тексте слово "спасибо"
    def clean_text(self):
        data = self.cleaned_data['text'].lower()
        gratitude_words = ['спасибо', 'благодарю', 'спасибки']
        if not any(word in data for word in gratitude_words):
            raise forms.ValidationError('Пожалуйста, используйте слова благодарности в сообщении!')
        return data



