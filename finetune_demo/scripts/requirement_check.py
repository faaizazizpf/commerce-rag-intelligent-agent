# File paths
expected_requirements_file = './expected_requirements.txt'
project_requirements_file = './project_requirements.txt'
unmatched_requirements_file = './unmatched_requirements.txt'
to_uninstall_requirements_file = './to_uninstall_requirements.txt'

def parse_requirements(file_path):
    """Reads a requirements file and returns a dictionary of packages with their versions."""
    requirements = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '==' in line:
                package, version = line.strip().split('==')
                requirements[package] = version
    return requirements

# Parse the requirements files
expected_requirements = parse_requirements(expected_requirements_file)
project_requirements = parse_requirements(project_requirements_file)

# Find mismatched packages
mismatched_packages = {
    package: expected_version
    for package, expected_version in expected_requirements.items()
    if package not in project_requirements or project_requirements[package] != expected_version
}

# Write mismatched packages with versions to unmatched_requirements.txt
with open(unmatched_requirements_file, 'w') as file:
    for package, version in mismatched_packages.items():
        file.write(f"{package}=={version}\n")

# Write package names only to to_uninstall_requirements.txt
with open(to_uninstall_requirements_file, 'w') as file:
    for package in mismatched_packages.keys():
        file.write(f"{package}\n")

print(f"Mismatched packages with versions have been written to {unmatched_requirements_file}")
print(f"Package names only have been written to {to_uninstall_requirements_file}")
