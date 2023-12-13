#%%
# fresh install
import polus.plugins as pp
import pathlib
pp.list # lists all locally available plugins
# %%
pp.submit_plugin("https://raw.githubusercontent.com/PolusAI/polus-plugins/master/formats/file-renaming-plugin/plugin.json")
pp.refresh()
pp.list

# %%
path = pathlib.Path('/Users/akshat.saini/Documents/pj/polus-plugins/features/nyxus-plugin/plugin.json')
pp.submit_plugin(path)
# %%
pp.refresh()
#%%
pp.list
# %%
filerenaming.inputs     
# %%
filerenaming.outputs         
# %%
filerenaming.inpDir
# %%