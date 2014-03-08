# Copyright (C) 2014 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html


import mimetypes

from gi.repository import GdkPixbuf
from gi.repository import Gio
from gi.repository import Gtk

ICON_SIZE = 48
FOLDER = 'folder'
UNKNOWN = 'unknown'

class MimeProvider:
    '''用于提供IconView中显示时需要的缩略图'''

    _data = {}

    def __init__(self, app):
        self.app = app
        # First, load `unknown' icon
        self.get('/foo', False)

    def get_mime(self, path, isdir):
        '''猜测文件类型, 根据它的文件扩展名'''
        if isdir:
            file_type = FOLDER
        else:
            file_type = mimetypes.guess_type(path)[0]
            if not file_type:
                file_type = UNKNOWN
        return file_type

    def get(self, path, isdir, icon_size=ICON_SIZE):
        '''取得一个缩略图.
        
        path - 文件的路径, 可以包括绝对路径, 也可以是文件名.
        isdir - 是否为一个目录.
        icon_size - 图标的大小, 如果是显示在IconView中的, 48就可以;
                    如果是显示在TreView的话, 可以用Gtk.IconSize.MENU

        @return 会返回一个Pixbuf以象, 和这个文件的类型(MIME)
        '''
        # FIXME: using icon_size 
        file_type = self.get_mime(path, isdir)
        if file_type in self._data:
            return (self._data[file_type], file_type)

        themed_icon = Gio.content_type_get_icon(file_type)
        icon_names = themed_icon.to_string().split(' ')[2:]
        icon_info = self.app.icon_theme.choose_icon(
                icon_names, icon_size, Gtk.IconLookupFlags.NO_SVG)
        if icon_info:
            pixbuf = icon_info.load_icon()
            self._data[file_type] = pixbuf
            return (pixbuf, file_type)
        else:
            pixbuf = self._data[UNKNOWN]
            return (pixbuf, file_type)

    def get_icon_name(self, path, isdir):
        file_type = self.get_mime(path, isdir)
        if file_type in (FOLDER, UNKNOWN):
            return file_type
        icon_name = Gio.content_type_get_generic_icon_name(file_type)
        if icon_name:
            return icon_name
        else:
            return UNKNOWN

    def get_app_img(self, app_info):
        themed_icon = app_info.get_icon()
        icon_names = themed_icon.get_names()
        if icon_names:
            img = Gtk.Image.new_from_icon_name(
                    icon_names[0], Gtk.IconSize.MENU)
            return img
        else:
            return None

