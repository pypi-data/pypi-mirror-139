from conans.errors import ConanException


def is_apple_os(os_):
    """returns True if OS is Apple one (Macos, iOS, watchOS or tvOS"""
    return str(os_) in ['Macos', 'iOS', 'watchOS', 'tvOS']


def to_apple_arch(arch, default=None):
    """converts conan-style architecture into Apple-style arch"""
    return {'x86': 'i386',
            'x86_64': 'x86_64',
            'armv7': 'armv7',
            'armv8': 'arm64',
            'armv8_32': 'arm64_32',
            'armv8.3': 'arm64e',
            'armv7s': 'armv7s',
            'armv7k': 'armv7k'}.get(arch, default)


def get_apple_sdk_name(conanfile):
    """
    Returns the 'os.sdk' (SDK name) field value. Every user should specify it because
    there could be several ones depending on the OS architecture.

    Note: In case of MacOS it'll be the same for all the architectures.
    """
    os_ = conanfile.settings.get_safe('os')
    os_sdk = conanfile.settings.get_safe('os.sdk')
    if os_sdk:
        return os_sdk
    elif os_ == "Macos":  # it has only a single value for all the architectures
        return "macosx"
    elif is_apple_os(os_):
        raise ConanException("Please, specify a suitable value for os.sdk.")


def apple_min_version_flag(os_version, os_sdk, subsystem):
    """compiler flag name which controls deployment target"""
    if not os_version or not os_sdk:
        return ''

    # FIXME: This guess seems wrong, nothing has to be guessed, but explicit
    flag = {'macosx': '-mmacosx-version-min',
            'iphoneos': '-mios-version-min',
            'iphonesimulator': '-mios-simulator-version-min',
            'watchos': '-mwatchos-version-min',
            'watchsimulator': '-mwatchos-simulator-version-min',
            'appletvos': '-mtvos-version-min',
            'appletvsimulator': '-mtvos-simulator-version-min'}.get(str(os_sdk))
    if subsystem == 'catalyst':
        # especial case, despite Catalyst is macOS, it requires an iOS version argument
        flag = '-mios-version-min'
    if not flag:
        return ''
    return "%s=%s" % (flag, os_version)
