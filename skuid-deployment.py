import os
import subprocess
import sys


def skuid_deployment():
    # Get environment variables
    all_changed_files = os.environ.get("ALL_CHANGED_FILES", "")
    target_username_alias = os.environ.get("TARGET_USERNAME_ALIAS", "")

    # Ensure there's something to work with
    if not all_changed_files:
        print("No changed files detected.")
        sys.exit(0)

    # Split the changed files into a list
    changed_files = all_changed_files.split()

    # Check if there are any files in the "skuidpages" directory
    pages_to_deploy = []
    deploy = False

    for file in changed_files:
        if "skuidpages/" in file:
            filename = file.split("/")[-1]  # Get the file name from the path
            pages_to_deploy.append(filename)
            deploy = True

    # If there are changes in "skuidpages", deploy the files
    if not deploy:
        print("No specific changes to deploy.")
        print(
            "A full deploy is not possible because it will pass the max limit of 6 million characters imposed by Salesforce."
        )
        print("Nothing to deploy.")
        sys.exit(0)

    print("Deploying pages:", pages_to_deploy)
    if target_username_alias:
        print(f"Using target username alias: {target_username_alias}")
    else:
        print("No target username alias provided.")

    deploy_flags = []
    deploy_flags.append(f"--targetusername {target_username_alias}")

    # Assuming `sf` is available and can be called via subprocess
    for page in pages_to_deploy:
        print(f"Deploying page: {page}")
        # Run the deployment command for each page (uncomment the line below to run it)
        # os.system(f"sf skuid page push --targetusername={target_username_alias} ./skuidpages/{page}")
        deploy_flags.append(f"./skuidpages/{page}")
        deploy_command = ["sf", "skuid", "page", "push"] + deploy_flags
        print(f"Executing command: {' '.join(deploy_command)}")
        subprocess.run(deploy_command, check=True)


if __name__ == "__main__":
    skuid_deployment()
