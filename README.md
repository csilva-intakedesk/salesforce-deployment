# Salesforce Deployment Script for GitHub Actions

This process involves the creation of a package.xml and subsequent deployment to a designated Salesforce environment. The generation of the delta is facilitated through [sf sgd source delta](https://github.com/scolladon/sfdx-git-delta) as a reference. It's important to note that while this plugin, though not officially supported by Salesforce, is widely adopted within the community for its effective usage.



#### Note
A ***delta*** is the difference between the files or 2 set of files. In the context of Salesforce the delta will be the difference of components, classes, etc that are in the local/sandbox version against the production one. The issue is that Salesforce, unless correctly specified, will deploy everything like a compiled application which can be time consuming. The delta generated here will be all new entities that are in one environemnt and another and all entities that are now removed. If using  `sg sgd source delta` is not something you want to use, then you can manually create the `package/package.xml`, `destructiveChanges/destructiveChanges.xml` and `destructiveChanges/package.xml` files to perform the delta.

## Inputs

|INPUT         |Optional|Type     |Default Value|Options|Description|
|--------------|:------:|:-------:|:-----------:|:-----:|:---------:|
|SF_AUTH_URL|N|string|-|-|The Salesforce Auth URL.|
|SF_AUTH_USERNAME|N|string|-|-|The Salesforce username for login. Salesforce project deploy `-o` flag.|
|DELTA_FROM_SOURCE|N|string|-|-|The from source that will be used on the sgd delta.|
|DELTA_TO_SOURCE|N|string|-|-|The to source that will be used on the sgd delta.|
|TEST_LEVEL|Y|option|RunLocalTests|NoTestRun, RunSpecifiedTests, RunLocalTests, RunAllTestsInOrg|Salesforce project deploy `--test-level` parameter. Defaults to RunLocalTests.|
|TIMEOUT|Y|number|30|-|Salesforce project deploy `--wait` flag value. Timeout in minutes for the command to complete and display results|
|MANIFEST_SOURCE_DIRECTORY|Y|string|force-app|-|Source files path for project manifest generation `--source-dir` flag.|
|MANIFEST_OUTPUT_DIRECTORY|Y|string|manifest|-|Output directoryfor project manifest generation `--output-dir` flag.|
|PACKAGE_SOURCE_DIRECTORY|Y|string|manifest/package.xml|-|Salesforce project deploy `--manifest` file path flag.|


## Usage

To get the required SF_AUTH_URL, use the following command in your terminal.

```bash
sf org display --verbose --json -o <TARGET_ORG_ALIAS_OR_USERNAME>
```

On your GitHub action add as part of a step. Example:

```yml
jobs:
  pre-check-merge:  
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v4

    - name: Debug Base Branch
      run: |
        #!/bin/bash
        echo "Triggered by merge to branch: ${{ github.ref_name }}"

    - name: Salesforce Production Pre-deployment Job
      uses: jvega-intakedesk/salesforce-deployment@v2.0.5
      with:
        SF_AUTH_URL: ${{ secrets.SFDX_UAT_AUTH_URL }}
        DELTA_FROM_SOURCE: ${{ vars.DELTA_FROM_SOURCE }}
        DELTA_TO_SOURCE: ${{ vars.DELTA_TO_SOURCE }}
        TEST_LEVEL: ${{ vars.TEST_LEVEL }}
        SF_AUTH_USERNAME: ${{ vars.SF_UAT_AUTH_USERNAME }}
```

