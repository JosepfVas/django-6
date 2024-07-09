from django import forms

from blog.models import Blog


class StyleMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class BlogForm(StyleMixin):
    class Meta:
        model = Blog
        exclude = ('view_count',)
