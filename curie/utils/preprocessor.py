from pathlib import Path

from django.template.loader import get_template
from django_user_agents.utils import get_user_agent


def is_mobile_browser(request):
    user_agent = get_user_agent(request)
    return user_agent.is_mobile


def get_template_name(request, template_name) -> str:
    """ Returns the mobile version of a template if it's available.
    """
    template_dir = str(get_template(template_name).origin)
    template_dir = template_dir.replace("\\", "/")
    template_dir = "/".join(template_dir.split("/")[:-1])
    mobile_version = "m_" + template_name.split("/")[-1]
    mobile_file = f"{template_dir}/{mobile_version}"

    mobile_template = f"{'/'.join(template_name.split('/')[:-1])}/{mobile_version}" if len(
        template_name.split('/')) > 1 else mobile_version
    
    if Path(mobile_file).is_file():
        if is_mobile_browser(request):
            return mobile_template
    else:
        return template_name
    return template_name