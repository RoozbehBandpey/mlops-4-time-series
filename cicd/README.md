# Continuous Integration and Continuous Delivery
Developers practicing continuous integration merge their changes back to the main branch as often as possible. The developer's changes are validated by creating a build and running automated tests against the build. By doing so, you avoid the integration hell that usually happens when people wait for release day to merge their changes into the release branch.

Continuous delivery is an extension of continuous integration to make sure that you can release new changes to your customers quickly in a sustainable way. This means that on top of having automated your testing, you also have automated your release process and you can deploy your application at any point of time by clicking on a button.
## Barebones Databricks CI/CD with Azure DevOps
This contains the most basic instructions for connecting a Databricks workspace to Azure DevOps for CI/CD.

In an ideal CI/CD scenario we would have multiple Databricks workspaces for DEV, INT and PROD. But for sake of demonstration we would eliminate those segregation and keep everything in one workspace.

### End Goal Scenario:
1. Develop a notebook in repository attached to workspace
1. Commit this to Azure DevOps (Master branch of the repo)
1. Once the commit is successful, this notebook will automatically be deployed into PROD workspace

> Note: Ideally, a developers should create a feature branch first and work there. Once it's reviewed by peers using 'pull request', this feature branch can be committed to master branch. Then, it'll be automatically deployed into higher environment like Staging for production testing or PROD directly.