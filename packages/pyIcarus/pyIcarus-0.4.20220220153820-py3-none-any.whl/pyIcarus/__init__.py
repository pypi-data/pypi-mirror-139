import os

import pkg_resources
from monty.dev import install_excepthook

install_excepthook()

from . import cool_decorators, parsers, replay_pcap, zoomzoom, cool_utils

dependencies_present = pkg_resources.resource_filename('pyIcarus', 'dependencies_present')
__all__ = ['cool_decorators', 'parsers', 'replay_pcap', 'zoomzoom', 'cool_utils']


def check_base_dependency():
    if os.path.exists(dependencies_present):
        del dependencies_present
    else:
        try:
            import conda.cli.python_api as Conda
            import sys
            return True
        except ImportError as mf:
            print("Conda not installed, please install conda")
            return False


def install(*package):
    (stdout_str, stderr_str, return_code_int) = Conda.run_command(
        Conda.Commands.INSTALL, *package,
        use_exception_handler=True, stdout=sys.stdout, stderr=sys.stderr
    )


def install_dependencies():
    try:
        print("Confirming cusignal installed")
        import cusignal
    except ImportError as mf:
        install(['-c', 'rapidsai', 'cusignal'])
    try:
        print("Confirming cupy installed")
        import cupy
    except ImportError as mf:
        install(['-c', 'rapidsai', 'cupy-cuda115'])
    try:
        print("Confirming digital_rf installed")
        import digital_rf
    except ImportError as mf:
        install(['digital_rf'])
    with open(dependencies_present, 'w') as f:
        ...


try:
    if check_base_dependency():
        print("Installing dependencies...")
        install_dependencies()
        print("Finished installing dependencies")
except Exception as e:
    print(f"Unable to install dependencies due to {e}")
