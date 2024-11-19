import os
import subprocess
import sys
import tempfile


def salesforce_deployment():
    # Gather environment variables from GitHub inputs
    dry_run = os.getenv("DRY_RUN") == "true"
    test_level = os.getenv("TEST_LEVEL")
    timeout = os.getenv("TIMEOUT")
    delta_from_source = os.getenv("DELTA_FROM_SOURCE")
    delta_to_source = os.getenv("DELTA_TO_SOURCE")
    sf_auth_username = os.getenv("SF_AUTH_USERNAME")
    delta_source_directory = os.getenv("DELTA_SOURCE_DIRECTORY")
    all_changed_files = os.environ.get("ALL_CHANGED_FILES", "")


    # Assuming inputs.SF_AUTH_URL contains the URL string
    sf_auth_url = os.getenv("SF_AUTH_URL")

    # Create a temporary file to store the SFDX URL
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sf_auth_url.encode())  # Write the URL to the temp file
        temp_file_path = temp_file.name  # Get the file path

    login_command = ["sf", "org", "login", "sfdx-url", "--set-default", "--sfdx-url-file", temp_file_path]

    print(f"Executing command: {' '.join(login_command)}")

    # Execute the login command
    subprocess.run(login_command, check=True)

    if not all_changed_files:
        print("No changed files detected.")
        sys.exit(0)

    # Split the changed files into a list
    changed_files = all_changed_files.split()
    deploy = False
    for file in changed_files:
        if "force-app/" in file:
            deploy = True

    if not deploy:
        print("No specific changes to deploy.")
        print(
            "A full deploy is not possible because it will pass the max limit of 6 million characters imposed by Salesforce."
        )
        print("Nothing to deploy.")
        sys.exit(0)

    deploy_flags = [
        "--wait",
        timeout,
        "--test-level",
        test_level
    ]

    if dry_run:
        deploy_flags.append("--dry-run")
        deploy_flags.append("--verbose")

    if delta_source_directory and os.path.isfile(delta_source_directory):
        print(f"Deploying changes from {delta_from_source} to {delta_to_source}")
        deploy_flags.append("--manifest")
        deploy_flags.append(delta_source_directory)
    else:
        print("No changes to deploy")

    destructive_changes_file = "destructiveChanges/destructiveChanges.xml"
    if os.path.isfile(destructive_changes_file):
        print(
            f"Deploying destructive changes from {delta_from_source} to {delta_to_source}"
        )
        deploy_flags.append("--post-destructive-changes")
        deploy_flags.append(destructive_changes_file)
    else:
        print("No destructive changes to deploy")

    # Build and execute the command
    deploy_command = ["sf", "project", "deploy", "start"] + deploy_flags
    print(f"Executing command: {' '.join(deploy_command)}")

    # Execute the deploy command
    subprocess.run(deploy_command, check=True)


if __name__ == "__main__":
    salesforce_deployment()