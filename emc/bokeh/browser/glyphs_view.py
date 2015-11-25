#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import field
from plone.directives import dexterity
from plone.memoize.instance import memoize
from emc.bokeh.content.glyphs import IFearture

from emc.bokeh import _

grok.templatedir('templates') 

class FeartureView(grok.View):
    "emc fearture view"
    grok.context(IFearture)
    grok.template('fearture_view')
    grok.name('fview')
    grok.require('zope2.View')    
    
#    def update(self):
#        # Hide the editable-object border
#        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context) 

 

        
 # fetch data
    def getData(self):
        # this is a list,and every item of the list must be dic
        datadic = self.context.coordination
        return datadic

    @memoize         
    def getPlot(self):
        """using bokeh output glyph
        """
        from bokeh.plotting import figure
        from bokeh.embed import components
        data = self.getData()
        if data ==None:
            x = [1, 2, 3, 4, 5]
            y = [6, 7, 2, 4, 5]
        else:
            x = []
            y = []
            for d in data:
                m = d['x']
                n = d['y']
                if m ==None:
                    x.append(0)
                else:
                    x.append(m)
                if n == None:
                    y.append(0)
                else:
                    y.append(n)
        # create a new plot with a title and axis labels
        p = figure(title=self.context.title, x_axis_label='x', y_axis_label='y')      
        # add a line renderer with legend and line thickness
        p.line(x, y, legend=self.context.legend, line_width=2)
        script, div = components(p)
#        import pdb
#        pdb.set_trace()
        out = {}
        out['js'] = script
        out['div'] = div
        return out    
        
