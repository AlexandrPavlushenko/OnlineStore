from django import forms
from .models import Product, Category

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта",
    "биржа", "дешево", "бесплатно",
    "обман", "полиция", "радар",
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available']


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Название не должно содержать запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание не должно содержать запрещенные слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5 МБ
                raise forms.ValidationError("Файл не должен превышать 5 MB.")
            if not (image.name.endswith('.jpg') or image.name.endswith('.jpeg') or image.name.endswith('.png')):
                raise forms.ValidationError("Допустимые форматы: JPEG, PNG.")
        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check'})