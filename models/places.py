# coding: utf8
db.define_table('tags',
    Field('tag'),
    format='%(tag)s')

db.define_table('links',
    Field('link_name'),
    Field('link_url'),
    Field('tags', 'list:reference db.tags'),
    Field('link_image', 'upload'),
    Field('link_colour'),
    format='%(link_name)s')
    
db.links.tags.requires = IS_IN_DB(db, 'tags.id', db.tags._format, multiple = True)
