from __future__ import print_function


class LibCfg(object):
  CREATE_MODE_OFF = 'off'
  CREATE_MODE_AUTO = 'auto'
  CREATE_MODE_VAMOS = 'vamos'
  CREATE_MODE_AMIGA = 'amiga'
  CREATE_MODE_FAKE = 'fake'

  EXPUNGE_MODE_LAST_CLOSE = 'last_close'
  EXPUNGE_MODE_NO_MEM = 'no_mem'
  EXPUNGE_MODE_SHUTDOWN = 'shutdown'

  valid_create_modes = (
      CREATE_MODE_OFF,
      CREATE_MODE_AUTO,
      CREATE_MODE_VAMOS,
      CREATE_MODE_AMIGA,
      CREATE_MODE_FAKE
  )

  valid_expunge_modes = (
      EXPUNGE_MODE_LAST_CLOSE,
      EXPUNGE_MODE_NO_MEM,
      EXPUNGE_MODE_SHUTDOWN
  )

  def __init__(self, create_mode=None,
               force_version=None, expunge_mode=None):
    # set defaults
    if create_mode is None:
      create_mode = self.CREATE_MODE_AUTO
    if expunge_mode is None:
      expunge_mode = self.EXPUNGE_MODE_LAST_CLOSE
    if create_mode not in self.valid_create_modes:
      raise ValueError("invalid create_mode: " + create_mode)
    if expunge_mode not in self.valid_expunge_modes:
      raise ValueError("invalid expunge mode: " + expunge_mode)
    # store values
    self.create_mode = create_mode
    self.force_version = force_version
    self.expunge_mode = expunge_mode

  @classmethod
  def from_dict(cls, cfg):
    create_mode = cfg.mode
    force_version = cfg.version
    expunge_mode = cfg.expunge
    return cls(create_mode, force_version, expunge_mode)

  def get_create_mode(self):
    return self.create_mode

  def get_force_version(self):
    return self.force_version

  def get_expunge_mode(self):
    return self.expunge_mode

  def __eq__(self, other):
    return self.create_mode == other.create_mode and \
        self.force_version == other.force_version and \
        self.expunge_mode == other.expunge_mode

  def __ne__(self, other):
    return self.create_mode != other.create_mode or \
        self.force_version != other.force_version or \
        self.expunge_mode != other.expunge_mode

  def __repr__(self):
    return "LibCfg(create_mode=%s," \
        " force_version=%s, expunge_mode=%s)" % \
        (self.create_mode,
         self.force_version, self.expunge_mode)


class LibMgrCfg(object):
  """hold config options of the lib manager"""

  def __init__(self, lib_default=None, dev_default=None):
    if lib_default is None:
      lib_default = LibCfg()
    if dev_default is None:
      dev_default = LibCfg()
    self.lib_default = lib_default
    self.dev_default = dev_default
    self.libs = {}
    self.devs = {}

  @classmethod
  def from_dict(cls, cfg_dict):
    mgr = cls()
    # add libs
    lib_cfg = cfg_dict.libs
    for lib in lib_cfg:
      cfg = LibCfg.from_dict(lib_cfg[lib])
      if lib == '*.library':
        mgr.set_lib_default(cfg)
      else:
        mgr.add_lib_cfg(lib, cfg)
    # add devs
    dev_cfg = cfg_dict.devs
    for dev in dev_cfg:
      cfg = LibCfg.from_dict(dev_cfg[dev])
      if dev == '*.device':
        mgr.set_dev_default(cfg)
      else:
        mgr.add_dev_cfg(dev, cfg)
    return mgr

  def set_lib_default(self, lib_cfg):
    self.lib_default = lib_cfg

  def set_dev_default(self, lib_cfg):
    self.dev_default = lib_cfg

  def get_lib_default(self):
    return self.lib_default

  def get_dev_default(self):
    return self.dev_default

  def add_lib_cfg(self, name, lib_cfg):
    self.libs[name] = lib_cfg

  def add_dev_cfg(self, name, lib_cfg):
    self.devs[name] = lib_cfg

  def get_lib_cfg(self, name, allow_default=True):
    if name in self.libs:
      return self.libs[name]
    if allow_default:
      return self.lib_default

  def get_dev_cfg(self, name, allow_default=True):
    if name in self.devs:
      return self.devs[name]
    if allow_default:
      return self.dev_default
