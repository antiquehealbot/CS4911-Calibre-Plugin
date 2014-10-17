#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2014, CATS'
__docformat__ = 'restructuredtext en'

if False:
    # This is here to keep my python error checker from complaining about
    # the builtin functions that will be defined by the plugin loading system
    # You do not need this code in your plugins
    get_icons = get_resources = None

# The class that all interface action plugins must inherit from
from calibre.gui2.actions import InterfaceAction

import re,json,urllib2

class InterfacePlugin(InterfaceAction):

    name = 'Sign Dict Plugin'

    # Declare the main action associated with this plugin
    # The keyboard shortcut can be None if you dont want to use a keyboard
    # shortcut. Remember that currently calibre has no central management for
    # keyboard shortcuts, so try to use an unusual/unused shortcut.
    action_spec = ('Sign Dict Plugin', None,
            'Run the Sign Dict Plugin', 'Ctrl+Shift+F1')

    def genesis(self):
        # This method is called once per plugin, do initial setup here

        # Set the icon for this interface action
        # The get_icons function is a builtin function defined for all your
        # plugin code. It loads icons from the plugin zip file. It returns
        # QIcon objects, if you want the actual data, use the analogous
        # get_resources builtin function.
        #
        # Note that if you are loading more than one icon, for performance, you
        # should pass a list of names to get_icons. In this case, get_icons
        # will return a dictionary mapping names to QIcons. Names that
        # are not found in the zip file will result in null QIcons.
        icon = get_icons('images/icon.png')
        

        # The qaction is automatically created from the action_spec defined
        # above
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.getPlayersForKeyword)

    def getPlayersForKeyword(self):
        #clean up keyword
        keyword = "hello"
        keyword = re.sub("(\'s|\'d|\.|,|\?|!|;|,)","",keyword)
        keyword = re.sub("(~ |~|_)"," ",keyword)
        keyword = keyword.strip()
        #grab info from REST API
        url = "http://smartsign.imtc.gatech.edu/videos?keywords=" + keyword
        response = urllib2.urlopen(url)
        #convert JSON to Python object
        info = json.load(response)
        #pull ids from converted JSON
        ids = []
        for item in info:
            ids.append(item["id"])
        #use ids to build a list of embedded players
        players = []
        for i in ids:
            players.append('<iframe width="640" height="360" align:right src="http://www.youtube.com/embed/' + i + '?rel=0"> </iframe>')
        print("keyword is: "+keyword)
        print("list of players: "+str(players))
        return players
