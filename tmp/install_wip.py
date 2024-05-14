import subprocess
import os


def check_python_version(required_version="3.8"):
    """
    Checks if the installed Python version meets the requirement.

    Args:
            required_version (str, optional): The required Python version. Defaults to "3.8".

    Returns:
            bool: True if the version meets the requirement, False otherwise.
    """
    try:
        output = subprocess.run(["python3", "-c", "import platform; print(platform.python_version())"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return output.stdout.strip() >= required_version


def install_python(version="3.8"):
    """
    Installs the required Python version using the system package manager.

    Args:
            version (str, optional): The version of Python to install. Defaults to "3.8".
    """
    package_manager = get_package_manager()
    if package_manager:
        command = [package_manager, "install", f"python{version}"]
        subprocess.run(command, check=True)
    else:
        print(f"Warning: System package manager not detected. Manual Python installation might be required.")


def check_package_installed(package_name):
    """
    Checks if a specific package is installed using pip.

    Args:
            package_name (str): The name of the package to check.

    Returns:
            bool: True if the package is installed, False otherwise.
    """
    try:
        subprocess.run(["pip", "show", package_name], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name):
    """
    Installs a package using pip.

    Args:
            package_name (str): The name of the package to install.
    """
    subprocess.run(["pip", "install", package_name], check=True)


def get_current_user():
    """
    Gets the current user name.

    Returns:
            str: The current user name.
    """
    return os.getlogin()


def check_directory_exists(path):
    """
    Checks if a directory exists.

    Args:
            path (str): The path to the directory.

    Returns:
            bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(path)


def create_directory(path):
    """
    Creates a directory with appropriate permissions.

    Args:
            path (str): The path to the directory.
    """
    os.makedirs(path, exist_ok=True)    # Create directory with intermediate directories if needed


def main():
    """
    The main entry point for the script.
    """

    # Define installation steps with check and install functions
    a_dir = "/Users/stewartbr/foo"
    steps = [
        (check_python_version, install_python, []),
        (check_package_installed, install_package, ["requests"]),
        (check_directory_exists, create_directory, [a_dir]),
    ]

    # Check and perform each installation step
    for check_func, install_func, args in steps:
        if not check_func(*args):
            doc = check_func.__doc__.split('\n\n')[0].strip()
            print(f"Requirement not met: {doc}")
            install_func(*args)
            print("Requirement installed.")


if __name__ == "__main__":
    main()

