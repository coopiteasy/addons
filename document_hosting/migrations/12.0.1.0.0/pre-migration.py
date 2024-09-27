from openupgradelib import openupgrade

model_renames_document = [
    ('easy_my_coop.document', 'document_hosting.document'),
]

model_renames_category = [
    ('easy_my_coop.document.category', 'document_hosting.category'),
]

table_renames_document = [
    ('easy_my_coop_document', 'document_hosting_document'),
]

table_renames_category = [
    ('easy_my_coop_document_category', 'document_hosting_category'),
]

xmlid_renames = [
    # easy_my_coop_website_document
    ('easy_my_coop_website_document.menu_website_document',
     'document_hosting.menu_website_document'),
    ('easy_my_coop_website_document.website_document_side_bar',
     'document_hosting.website_document_side_bar'),
    ('easy_my_coop_website_document.website_document_display_document_list',
     'document_hosting.website_document_display_document_list'),
    ('easy_my_coop_website_document.display_categories_and_documents',
     'document_hosting.display_categories_and_documents'),
    ('easy_my_coop_website_document.template_website_document',
     'document_hosting.template_website_document'),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if openupgrade.table_exists(cr, 'easy_my_coop_document'):
        openupgrade.rename_models(cr, model_renames_document)
        openupgrade.rename_tables(cr, table_renames_document)
    if openupgrade.table_exists(cr, 'easy_my_coop_document_category'):
        openupgrade.rename_models(cr, model_renames_category)
        openupgrade.rename_tables(cr, table_renames_category)
    openupgrade.rename_xmlids(cr, xmlid_renames)
