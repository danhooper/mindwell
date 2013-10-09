from django import template

register = template.Library()


@register.inclusion_tag('custom_modal_template.html')
def render_custom_modal(choices,
                        current_val,
                        title):
    try:
        curr_choices_list = current_val.split(', ')
    except AttributeError:
        curr_choices_list = []
    curr_choices_list = [choice.strip() for choice in curr_choices_list]
    for choice in choices:
        if choice.choice in curr_choices_list:
            choice.selected = True
    other_choices_list = []
    choices_str_list = [choice.choice for choice in choices]
    for choice in curr_choices_list:
        if choice not in choices_str_list:
            other_choices_list.append(choice)
    other_choice = ', '.join(other_choices_list)
    return {'choices': choices,
            'other_choice': other_choice,
            'title': title,
            'form_prefix': '_'.join(title.split(' ')).lower()
            }
