from django.forms.widgets import Input


class ColorWidget(Input):
    # HTML widget for color input
    input_type = 'color'
    template_name = 'dev_sup/forms/widgets/color.html'
