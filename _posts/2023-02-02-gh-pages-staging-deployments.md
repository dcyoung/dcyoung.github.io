---
title: "Automating Free Staging Deployments for Github Pages"
date: 2023-02-02T00:00:00-00:00
last_modified_at: 2023-02-02T00:00:00-00:00
categories:
  - automation
  - software notes
permalink: /post-gh-pages-staging-deployments/
classes: wide
excerpt: Automating free staging deployments for Github Pages using Github Actions. 
header:
  og_image: /images/gh-pages-staging-deployments/preview.webp
  teaser: /images/gh-pages-staging-deployments/preview.webp
---


## Problem

In typical software projects a CI/CD pipeline manages not only a "Production" deployment but also multiple other deployments for testing new features or running nightly regression tests etc. Using a "Staging" deployment to review proposed changes before you commit to production will prevent users from seeing bugs.

I use [Github Pages](https://pages.github.com/) to host sites for many of my personal projects (including this blog). I also use Github Actions for CI/CD, to automatically build and deploy a site whenever I commit changes. However, **Github Pages only supports a single deployment of any given repository**. Therefore, testing changes in a hypothetical deployment is NOT easily possible.

For professional projects I would use a more dedicated and feature rich CI/CD pipeline, but for side projects using Github Pages I wanted a simple solution:

- free
- low maintenance
- close to code... all in Github if possible
- basic staging deployment --> allow me to view a deployed version of the app BEFORE I commit to prod

## Idea

To accomplish this, I used Github Actions. The lifecycle of a Pull Request (PR) controls the lifecycle of a staging deployment - ie: 1 deployment for each PR, created when the PR is opened and removed when the PR is closed.

- Developer opens PR in the app repository
  - Github Action creates a repository for a staging deployment
  - Github Action builds the app and deploys it to the staging repository
  - Github Action writes a comment to the PR with a link to the live staging deployment
- Developer inspects the staging deployment
- Developer merges or closes the open PR
  - Github Action deletes the staging repository (and staging deployment)
- If the PR was merged, Github Action builds and deploys the app to production

The final result looks something like this:
![pr](/images/gh-pages-staging-deployments/example-pr.webp){:.align-center}

## Creating Github Actions

This process requires 2 new Github Action **actions**:

- `create-git-repo`: creates a new github repository
- `delete-git-repo`: deletes an existing github repository

I used simple JS scripts to hit the Github API, and made dedicated actions for each. I'd recommend tightly controlling any actions that leverage secrets or personal access tokens, rather than using third party actions. See the action repositories for more details: [ga-create-git-repo](https://github.com/dcyoung/ga-create-git-repo), [ga-delete-git-repo](https://github.com/dcyoung/ga-delete-git-repo).

## Creating Workflows

Next, the overall staging process requires 2 new Github Action **workflows**:

- `pr_staging_deploy`: creates and manages the staging deployment for open PRs
  - When a PR is opened
    - Creates the a new temporary repository to host the staging deployment
  - When a PR is opened or when a commit is added to an opened PR 
    - Builds the app
    - Deploys the app to the temporary staging repository
    - Posts or updates a link in the PR comments, providing a URL to the staging deployment
- `pr_staging_teardown`: removes staging deployments on PR merge/close
  - When a PR is closed (or merged), delete the staging repository & deployment

Again, the workflow centers around the lifecycle of a PR by using the **pull request node id** to create temporary repo names w/ deterministic behavior. See the [code](https://github.com/dcyoung/r3f-audio-visualizer/tree/dev/.github/workflows) for more details.

```yml
name: Staging PR Deploy
# Run when pull requests are opened
on:
  pull_request:
    branches: [dev]
env:
  PR_REPO_NAME: staging-pr-${{ github.event.pull_request.node_id }}
jobs:
  create-page-host:
    runs-on: ubuntu-latest
    steps:
      - name: Create new repository for temporary deployment
        uses: dcyoung/ga-create-git-repo@v1.0.0
        with:
          name: ${{ env.PR_REPO_NAME }}
          # org: dcyoung
          access-token: ${{ secrets.PAT }}
  pr-build-deploy:
    needs: create-page-host
    runs-on: ubuntu-latest
    environment:
      name: pr-staging
      url: https://dcyoung.github.io/${{ env.PR_REPO_NAME }}/
    steps:
      - name: Setup Node.js
        uses: actions/setup-node@v2
      - name: Set GitHub Actions as Commit Author
        run: |
          git config --global user.name github-actions
          git config --global user.email github-actions@github.com
      - name: Checkout Repo
        uses: actions/checkout@v2
        with:
          path: "pr-build"
      - name: Install and Build
        run: |
          cd pr-build
          npm install
          npm run build -- --base=/${{ env.PR_REPO_NAME }}/
        env:
          CI: ""
      - name: Checkout temporary deployment target repo
        uses: actions/checkout@v2
        with:
          repository: dcyoung/${{ env.PR_REPO_NAME }}
          fetch-depth: 0
          path: "pr-deploy"
          token: ${{ secrets.PAT }}
      - name: Push files to target
        run: |
          cp -r pr-build/dist/* pr-deploy
          cd pr-deploy
          git add .
          git commit -m $GITHUB_SHA
          git branch -M gh-pages
          git push -f -u origin gh-pages
      - name: Create link in PR
        uses: mshick/add-pr-comment@v2
        with:
          message: |
            **Staging Preview:**
            https://dcyoung.github.io/${{ env.PR_REPO_NAME }}/
```

```yml
name: Staging PR Teardown
# Run when pull requests are closed (includes merged)
on:
  pull_request:
    branches: [dev]
    types: [closed]
env:
  # The name of the staging repo created for this
  PR_REPO_NAME: staging-pr-${{ github.event.pull_request.node_id }}
jobs:
  delete-page-host:
    runs-on: ubuntu-latest
    steps:
      - name: Delete repository for temporary deployment
        uses: dcyoung/ga-delete-git-repo@v1.0.0
        with:
          name: dcyoung/${{ env.PR_REPO_NAME }}
          access-token: ${{ secrets.PAT }}
```
