# # modules\Persona\ProfileManager\Toolbox\maps.py

from modules.Personas.ProfileManager.Toolbox import ProfileManager

# A dictionary to map function names to actual function objects
function_map = {
    "update_field": ProfileManager.update_field,
    "append_to_field": ProfileManager.append_to_field
}