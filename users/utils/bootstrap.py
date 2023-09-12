from django import forms


class BootstrapModelForm(forms.ModelForm):
    """重写init方法"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加样式
        for field_name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = f"请输入{field.label}"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": f"请输入{field.label}"
                }
