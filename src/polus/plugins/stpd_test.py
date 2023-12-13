import streamlit as st
from polus.plugins._plugins.classes.plugin_classes import Plugin
import streamlit_pydantic as stpd
from polus.plugins._plugins.classes.plugin_classes import load_plugin

# function takes a Plugin object as an argument
def generate_input_form(plugin: Plugin):
    input_schema = plugin.inputs

    # defining pydantic model using decorator
    @stpd.pydantic
    class InputModel:
        # define model fields based on the input schema
        # add more fields based on plugin
        field1: str
        field2: str

    # create an instance of the Pydantic model
    input_data = InputModel()

    # generate the input form using streamlit-pydantic
    form_result = stpd.pydantic_form(key = 'my_form', model = InputModel)
    
    return form_result

# path to the manifest
manifest_path = "/user/akshat/manifest.json"

# load the plugin using the manifest
selected_plugin = load_plugin(manifest_path)

# generate the input form for the selected plugin
form_result = generate_input_form(selected_plugin)

# use the form_result to get the user's input
st.write("User Input:", form_result)