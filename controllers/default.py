# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """   
        
    if request.vars.the_view:
		current_view = request.vars.the_view
		session.the_view = request.vars.the_view
    elif session.the_view:
        current_view = session.the_view    
    else:
        current_view = "kitchen"
    
    current_row = db(db.tags.tag == current_view).select()    
    current_tag = current_row[0].id
            
    links = db(db.links.tags.contains(current_tag)).select()
    
    return dict(links = links)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

@auth.requires_membership('administrators')
def edit():
    edit_form = crud.update(db.links, request.args[0])
    closer = A('close', _href=URL('#'), _class='close_link')
    the_title = H3('Edit this Place')
    
    return dict(form = edit_form, closer=closer, the_title=the_title)
	
@auth.requires_membership('administrators')
def create():
	form = crud.create(db.links)
	closer = A('close', _href=URL('#'), _class='close_link')
	the_title = H3('Link to a New Place')
		
	return dict(form = form, closer=closer, the_title=the_title)
