from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.serializers.json import DjangoJSONEncoder


def currency_display(amount, currency="$"):
    _amount = round(float(amount), 2)
    frac_part, int_part = math.modf(_amount)
    return "{currency}{int_part}{float_part}".format(
        **{
            "currency": currency,
            "int_part": intcomma(math.trunc(int_part)),
            "float_part": "{:0.2f}".format(abs(frac_part)).lstrip("0"),
        }
    )


def admin_json_field_prettifier(instance_data):
    """ Useful to represent json and dicts """
    try:
        from pygments import highlight
        from pygments.lexers import JsonLexer
        from pygments.formatters import HtmlFormatter

        import json

        # Convert the data to sorted, indented JSON
        response = json.dumps(
            instance_data, sort_keys=True, indent=4, cls=DjangoJSONEncoder
        )
        # response = json.dumps(instance_data, sort_keys=True, indent=4)
        # Get the Pygments formatter
        formatter = HtmlFormatter(style="colorful", nowrap=True, lineseparator="</br>")
        # Highlight the data
        response = highlight(response, JsonLexer(), formatter).replace("  ", " &nbsp;")
        # Get the stylesheet
        style = formatter.get_style_defs().replace("\n", " ")
        # Safe the output
        return format_html(
            "<style>{}</style><pre>{}</pre>", mark_safe(style), mark_safe(response)
        )
    except ImportError:
        import pprint

        return format_html("<pre>{}</pre>", pprint.pformat(instance_data, indent=2))

