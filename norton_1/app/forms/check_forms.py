from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput   

class MultiCheckBoxField(SelectMultipleField):
    """
        Renders a list check box instead of a <select multiple>
    """

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()