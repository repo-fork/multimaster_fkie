# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Fraunhofer FKIE/US, Alexander Tiderko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Fraunhofer nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import roslib

from common import get_ros_home, masteruri_from_ros

class Settings(object):

  USER_DEFAULT = 'robot'
  # set the cwd to the package of the node_manager_fkie to support the images
  # in HTML descriptions of the robots and capabilities
  PKG_NAME = 'node_manager_fkie'
  PACKAGE_DIR = ''.join([roslib.packages.get_pkg_dir(PKG_NAME), os.path.sep])
  ROBOTS_DIR = ''.join([PACKAGE_DIR, os.path.sep, 'images', os.path.sep])
  CFG_PATH = ''.join(['.node_manager', os.sep])
  '''@ivar: configuration path to store the history.'''
  HELP_FILE = ''.join([PACKAGE_DIR, os.path.sep, 'README.rst'])
  CURRENT_DIALOG_PATH = os.path.expanduser('~')
  LOG_PATH = ''.join([os.environ.get('ROS_LOG_DIR'), os.path.sep]) if os.environ.get('ROS_LOG_DIR') else os.path.join(os.path.expanduser('~'), '.ros/log/')

  LOG_VIEWER = "/usr/bin/less -fKLnQrSU"
  STARTER_SCRIPT = 'rosrun node_manager_fkie remote_nm.py'
  RESPAWN_SCRIPT = 'rosrun node_manager_fkie respawn'
  '''
  the script used on remote hosts to start new ROS nodes
  '''

  LAUNCH_HISTORY_FILE = 'launch.history'
  LAUNCH_HISTORY_LENGTH = 5

  PARAM_HISTORY_FILE = 'param.history'
  PARAM_HISTORY_LENGTH = 12

  CFG_REDIRECT_FILE = 'redirect'
  CFG_FILE = 'settings.ini'
  CFG_GUI_FILE = 'settings.ini'

  TIMEOUT_CONTROL = 5
  TIMEOUT_UPDATES = 20

  FOLLOW_INCLUDED_EXT = ['.launch', '.yaml', '.conf', '.cfg', '.iface', '.sync', '.test', '.xml']
  LAUNCH_VIEW_EXT = ['.launch', '.yaml', '.conf', '.cfg', '.iface', '.sync', '.test']

  STORE_GEOMETRY = True

  def __init__(self):
    self._terminal_emulator = None
    self._masteruri = masteruri_from_ros()
    self.CFG_PATH = ''.join([get_ros_home(), os.sep, 'node_manager', os.sep])
    self._cfg_path = self.CFG_PATH
    if not os.path.isdir(self.cfg_path):
      os.makedirs(self.cfg_path)
    elif os.path.exists(os.path.join(self.cfg_path, self.CFG_REDIRECT_FILE)):
      settings = self.qsettings(self.CFG_REDIRECT_FILE)
      self._cfg_path = settings.value('cfg_path', self.CFG_PATH)
    self._robots_path = self.ROBOTS_DIR
    settings = self.qsettings(self.CFG_FILE)
    self._default_user = settings.value('default_user', self.USER_DEFAULT)
    self._launch_history_length = int(settings.value('launch_history_length', self.LAUNCH_HISTORY_LENGTH))
    self._param_history_length = int(settings.value('param_history_length', self.PARAM_HISTORY_LENGTH))
    self._current_dialog_path = self.CURRENT_DIALOG_PATH
    self._log_viewer = self.LOG_VIEWER
    self._start_remote_script = self.STARTER_SCRIPT
    self._respawn_script = self.RESPAWN_SCRIPT
    self._launch_view_file_ext = self.str2list(settings.value('launch_view_file_ext', ', '.join(self.LAUNCH_VIEW_EXT)))
    self._follow_include_file_ext = self.str2list(settings.value('launch_view_file_ext', ', '.join(self.FOLLOW_INCLUDED_EXT)))
    self._store_geometry = self.str2bool(settings.value('store_geometry', self.STORE_GEOMETRY))

  def masteruri(self):
    return self._masteruri

  @property
  def cfg_path(self):
    return self._cfg_path

  @cfg_path.setter
  def cfg_path(self, path):
    if not os.path.isdir(path):
      os.makedirs(path)
    self._cfg_path = path
    if self._cfg_path != self.CFG_PATH:
      settings = self.qsettings(self.CFG_REDIRECT_FILE)
      settings.setValue('cfg_path', self._cfg_path)
    else:
      # remove the redirection
      try:
        os.remove(os.path.join(self._cfg_path, self.CFG_REDIRECT_FILE))
      except:
        pass

  @property
  def robots_path(self):
    return self._robots_path

  @robots_path.setter
  def robots_path(self, path):
    if not os.path.isdir(path):
      os.makedirs(path)
    self._robots_path = path
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('robots_path', self._robots_path)

  @property
  def default_user(self):
    return self._default_user

  @default_user.setter
  def default_user(self, user):
    if user:
      self._default_user = user
      settings = self.qsettings(self.CFG_FILE)
      settings.setValue('default_user', self._default_user)

  @property
  def launch_history_length(self):
    return self._launch_history_length

  @launch_history_length.setter
  def launch_history_length(self, len):
    self._launch_history_length = len
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('launch_history_length', self._launch_history_length)

  @property
  def param_history_length(self):
    return self._param_history_length

  @param_history_length.setter
  def param_history_length(self, len):
    self._param_history_length = len
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('param_history_length', self._param_history_length)

  @property
  def current_dialog_path(self):
    return self._current_dialog_path

  @current_dialog_path.setter
  def current_dialog_path(self, path):
    self._current_dialog_path = path

  def robot_image_file(self, robot_name):
    return os.path.join(self.ROBOTS_DIR, '%s.png'%robot_name)

  @property
  def log_viewer(self):
    return self._log_viewer

  @log_viewer.setter
  def log_viewer(self, viewer):
    self._log_viewer = viewer

  @property
  def start_remote_script(self):
    return self._start_remote_script

  @start_remote_script.setter
  def start_remote_script(self, script):
    self._start_remote_script = script

  @property
  def respawn_script(self):
    return self._respawn_script

  @respawn_script.setter
  def respawn_script(self, script):
    self._respawn_script = script

  @property
  def launch_view_file_ext(self):
    return self._launch_view_file_ext

  @launch_view_file_ext.setter
  def launch_view_file_ext(self, exts):
    self._launch_view_file_ext = self.str2list('%s'%exts)
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('launch_view_file_ext', self._launch_view_file_ext)

  @property
  def follow_include_file_ext(self):
    return self._follow_include_file_ext

  @follow_include_file_ext.setter
  def follow_include_file_ext(self, exts):
    self._follow_include_file_ext = self.str2list('%s'%exts)
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('follow_include_file_ext', self._follow_include_file_ext)

  @property
  def store_geometry(self):
    return self._store_geometry

  @store_geometry.setter
  def store_geometry(self, value):
    self._store_geometry = self.str2bool(value)
    settings = self.qsettings(self.CFG_FILE)
    settings.setValue('store_geometry', self._store_geometry)

  def str2bool(self, v):
    if isinstance(v, bool):
      return v
    return v.lower() in ("yes", "true", "t", "1")

  def str2list(self, l):
    if isinstance(l, list):
      return l
    l = l.strip('[]')
    l = l.replace('u"', '')
    l = l.replace('"', '')
    l = l.replace("'", '')
    l = l.replace(",", ' ')
    return [str(i).strip() for i in l.split(' ') if i]

  def terminal_cmd(self, cmd, title):
    '''
    Creates a command string to run with a terminal prefix
    @param cmd: the list with a command and args
    @type cmd: [str,..]
    @param title: the title of the terminal
    @type title: str
    @return: command with a terminal prefix
    @rtype:  str
    '''
    if self._terminal_emulator is None:
      self._terminal_emulator = ""
      for t in ['/usr/bin/x-terminal-emulator', '/usr/bin/xterm']:
        if os.path.isfile(t) and os.access(t, os.X_OK):
          self._terminal_emulator = t
          break
    if self._terminal_emulator == "": return ""
    return "%s -T %s -e %s"%(self._terminal_emulator, title, ' '.join(cmd))

  def qsettings(self, file):
    from python_qt_binding import QtCore
    return QtCore.QSettings(os.path.join(self.cfg_path, file),
                            QtCore.QSettings.IniFormat)