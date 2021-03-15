#%%
import pandas as pd 

edgelist = pd.read_csv("taxon_edgelist.csv", sep='\t')
nodelist = pd.read_csv("taxon_nodelist.csv", sep='\t')

#%%

# Attach children to parents

# df = (
#     nodelist
#     .merge(
#         edgelist, 
#         left_on=['content_id'], 
#         right_on=['target_content_id'],
#         how='left'
#     )
#     .merge(
#         nodelist[['title', 'content_id']], 
#         left_on=['src_content_id'], 
#         right_on=['content_id'],
#         suffixes=(None, '_child'),
#         how='left'
#     )
#     .drop(['src_content_id', 'target_content_id', 'content_id_child'], axis='columns')
#     # .groupby(['title', 'content_id', 'base_path', 'document_type', 'level'])
#     # .agg({'title_child': list})
# )

#%%
# Attach parents to children
df = (
    nodelist
    .merge(
        edgelist, 
        left_on=['content_id'], 
        right_on=['src_content_id'],
        how='left'
    )
    .merge(
        nodelist[['title', 'content_id', 'base_path']], 
        left_on=['target_content_id'], 
        right_on=['content_id'],
        suffixes=(None, '_parent'),
        how='left'
    )
    .drop(['src_content_id', 'target_content_id'], axis='columns')
    # .groupby(['title', 'content_id', 'base_path', 'document_type', 'level'])
    # .agg({'title_child': list})
)

#%%
df.to_csv("gov-uk-taxonomy.csv", index=False)

hierarchy = pd.read_csv("gov-uk-taxonomy.csv")