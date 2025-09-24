from .tools import (
    get_initiatives,
    get_initiative_by_id,
    create_initiative,
    update_initiative,
    delete_initiative,
    get_status_list,
)

ALL_TOOLS = {
    get_initiatives,
    get_initiative_by_id,
    create_initiative,
    update_initiative,
    delete_initiative,
    get_status_list,
}

def get_role_tools(role):
    """
    Returns a list of tool callables allowed for this role (admin or user).
    """
    if role and role.lower() == "admin":
        tools_allowed = ALL_TOOLS
    else:
        # Read only for regular users
        tools_allowed = [get_initiatives, get_initiative_by_id, get_status_list]

    return tools_allowed