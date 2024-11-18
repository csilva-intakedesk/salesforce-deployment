import os
import subprocess
import sys


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
        f"--wait {timeout}",
        f"--test-level {test_level}",
    ]

    if dry_run:
        deploy_flags.append("--dry-run")
        deploy_flags.append("--verbose")

    if sf_auth_username:
        deploy_flags.append(f"-o {sf_auth_username}")

    if delta_source_directory and os.path.isfile(delta_source_directory):
        print(f"Deploying changes from {delta_from_source} to {delta_to_source}")
        deploy_flags.append(f"--manifest {delta_source_directory}")
    else:
        print("No changes to deploy")

    destructive_changes_file = "destructiveChanges/destructiveChanges.xml"
    if os.path.isfile(destructive_changes_file):
        print(
            f"Deploying destructive changes from {delta_from_source} to {delta_to_source}"
        )
        deploy_flags.append(f"--post-destructive-changes {destructive_changes_file}")
    else:
        print("No destructive changes to deploy")

    # Build and execute the command
    deploy_command = ["sf", "project", "deploy", "start"] + deploy_flags
    print(f"Executing command: {' '.join(deploy_command)}")

    # Execute the deploy command
    subprocess.run(deploy_command, check=True)


if __name__ == "__main__":
    salesforce_deployment()
