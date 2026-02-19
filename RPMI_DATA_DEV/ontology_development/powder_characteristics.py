#%%
#--Powder Characteristics-- 

'''
things like powder characteristics might make sense to separate as its own material table,
since in theory you can use the same batch of powder for multiple builds/parts etc.
So then when you are doing a build you just need to link the build to the material record
Information like external factors will be heavily manual to link. "here is a spreadsheet operators add records to"

'''
powder_characteristics = pd.DataFrame({
    "parameter_name": []

})