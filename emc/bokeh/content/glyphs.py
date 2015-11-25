#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
import datetime

from z3c.form.form import extends
from z3c.form import field

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from collective import dexteritytextindexer

#from collective.dexteritytextindexer.behavior import IDexterityTextIndexer
#from emc.bokeh.registrysource import DynamicVocabulary
from emc.bokeh import _



#图像数据schema,包括x坐标，y坐标
class IPlotDataSchema(Interface):
    x = schema.Float(title=_(u"X Coordinate"))
    y = schema.Float(title=_(u"Y Coordinate"))


class IFearture(form.Schema,IBasic):
    """
    emc project features content type
    """
#标准名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"standard name"),
                             default=u"",
                            required=True,) 
#标准描述        
    description = schema.TextLine(title=_(u"standard description"),
                             default=u"",
                             required=False,)
#图例       
    lengend = schema.TextLine(title=_(u"a legend of the  figure"),
                             default=u"",
                             required=True,)    
# 图像数据字段
    form.widget(coordination=DataGridFieldFactory)
    coordination = schema.List(title=u"coordination data",
        value_type=DictRow(title=u"coordination data row", schema=IPlotDataSchema))


##数据来源 
#    source = schema.Choice(
#        title=_(u"Where the source data that will composing the plot come from ?"),     
#        source=possibleOrganization,     
#        required=True
#    )
#
##包含图像数据的csv文件   
#    report = NamedBlobFile(title=_(u"report"),
#        description=_(u"Attach your photo data report file(csv format)."),
#        required=True
#    )
    
class EditForm(form.EditForm):
    extends(form.EditForm)

    grok.context(IFearture)
    grok.require('zope2.View')
    fields = field.Fields(IFearture)
    label=_(u"modify standard parameters for Plotting the figure")

    fields['coordination'].widgetFactory = DataGridFieldFactory


         