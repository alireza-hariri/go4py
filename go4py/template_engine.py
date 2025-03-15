import re


def render_template(template_string, data):
    """
    A very basic template engine that replaces placeholders with values from a dictionary.

    Args:
      template_string: The string containing placeholders like {{ variable_name }}.
      data: A dictionary where keys are variable names and values are their corresponding values.

    Returns:
      The template string with placeholders replaced by their values.
      Returns the original template if a placeholder is not found in the data.
    """

    def replace_placeholder(match):
        variable_name = match.group(1).strip()
        try:
            return str(data[variable_name])
        except KeyError:
            return match.group(0)  # Return the original placeholder if not found

    return re.sub(r"{{(.*?)}}", replace_placeholder, template_string)
