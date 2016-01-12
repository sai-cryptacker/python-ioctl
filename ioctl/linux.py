import ctypes
import platform

class _IoctlGeneric(object):
    _IOC_NRBITS = 8
    _IOC_TYPEBITS = 8
    _IOC_SIZEBITS = 14
    _IOC_DIRBITS = 2
    _IOC_NONE = 0
    _IOC_WRITE = 1
    _IOC_READ = 2

    @classmethod
    def ioc(cls, direction, request_type, request_nr, size):
        _IOC_NRSHIFT = 0
        _IOC_TYPESHIFT = _IOC_NRSHIFT + cls._IOC_NRBITS
        _IOC_SIZESHIFT = _IOC_TYPESHIFT + cls._IOC_TYPEBITS
        _IOC_DIRSHIFT = _IOC_SIZESHIFT + cls._IOC_SIZEBITS
        return (
            (direction << _IOC_DIRSHIFT) |
            (request_type << _IOC_TYPESHIFT) |
            (request_nr << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT)
            )

class _IoctlAlpha(_IoctlGeneric):
    _IOC_NRBITS = 8
    _IOC_TYPEBITS = 8
    _IOC_SIZEBITS = 13
    _IOC_DIRBITS = 3
    _IOC_NONE = 1
    _IOC_READ = 2
    _IOC_WRITE = 4

class _IoctlMips(_IoctlGeneric):
    _IOC_SIZEBITS = 13
    _IOC_DIRBITS = 3
    _IOC_NONE = 1
    _IOC_READ = 2
    _IOC_WRITE = 4

class _IoctlParisc(_IoctlGeneric):
    _IOC_NONE = 0
    _IOC_WRITE = 2
    _IOC_READ = 1

class _IoctlPowerPC(_IoctlGeneric):
    _IOC_SIZEBITS = 13
    _IOC_DIRBITS = 3
    _IOC_NONE = 1
    _IOC_READ = 2
    _IOC_WRITE = 4

class _IoctlSparc(_IoctlGeneric):
    _IOC_NRBITS = 8
    _IOC_TYPEBITS = 8
    _IOC_SIZEBITS = 13
    _IOC_DIRBITS = 3
    _IOC_NONE = 1
    _IOC_READ = 2
    _IOC_WRITE = 4

_machine_ioctl_map = {
    'alpha': _IoctlAlpha,
    'mips': _IoctlMips,
    'mips64': _IoctlMips,
    'parisc': _IoctlParisc,
    'parisc64': _IoctlParisc,
    'ppc': _IoctlPowerPC,
    'ppcle': _IoctlPowerPC,
    'ppc64': _IoctlPowerPC,
    'ppc64le': _IoctlPowerPC,
    'sparc': _IoctlSparc,
    'sparc64': _IoctlSparc,
}

def _machine_ioctl_calculator():
    machine = platform.machine()
    return _machine_ioctl_map.get(machine, _IoctlGeneric)

def _ioc_type_size(size):
    if issubclass(size, ctypes._SimpleCData):
        return ctypes.sizeof(size)
    elif isinstance(int, size):
        return size
    else:
        raise TypeError('Invalid type for size: {size_type}'.format(size_type=type.__class__.__name__))

def IOC(direction, request_type, request_nr, size):
    calc = _machine_ioctl_calculator()

    if direction is None:
        direction = calc._IOC_NONE
    elif direction == 'r':
        direction = calc._IOC_READ
    elif direction == 'w':
        direction = calc._IOC_WRITE
    elif direction == 'rw':
        direction = calc._IOC_READ | calc._IOC_WRITE
    else:
        raise ValueError('direction must be None, \'r\', \'w\' or \'rw\'.')

    request_type = ord(request_type)
    return calc.ioc(direction, request_type, request_nr, size)

def IO(request_type, request_nr):
    calc = _machine_ioctl_calculator()
    request_type = ord(request_type)
    return calc.ioc(calc._IOC_NONE, request_type, request_nr, 0)

def IOR(request_type, request_nr, size):
    calc = _machine_ioctl_calculator()
    request_type = ord(request_type)
    size = _ioc_type_size(size)
    return calc.ioc(calc._IOC_READ, request_type, request_nr, size)

def IOW(request_type, request_nr, size):
    calc = _machine_ioctl_calculator()
    request_type = ord(request_type)
    size = _ioc_type_size(size)
    return calc.ioc(calc._IOC_WRITE, request_type, request_nr, size)

def IOWR(request_type, request_nr, size):
    calc = _machine_ioctl_calculator()
    request_type = ord(request_type)
    size = _ioc_type_size(size)
    return calc.ioc(calc._IOC_READ|calc._IOC_WRITE, request_type, request_nr, size)
