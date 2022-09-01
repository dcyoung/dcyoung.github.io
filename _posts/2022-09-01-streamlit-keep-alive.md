---
title: "Automated a Deployed App Keep-Alive Probe"
date: 2022-09-01T00:00:00-00:00
last_modified_at: 2022-09-01T00:00:00-00:00
categories:
  - automation
  - software notes
permalink: /post-streamlit-keep-alive/
classes: wide
excerpt: Automating a keep-alive probe for a deployed streamlit app. 
header:
  og_image: https://docs.streamlit.io/images/spin_down.png
  teaser: https://docs.streamlit.io/images/spin_down.png
---


## Problem

Streamlit cloud allows developers to easily host streamlit applications for free! However, public apps will eventually hibernate if unused for a period of time. This can result in an pesky and occasionally lengthy reboot time.  See [details](https://docs.streamlit.io/streamlit-cloud/get-started/manage-your-app#app-hibernation)

![placeholder](https://docs.streamlit.io/images/spin_down.png){:.align-center}

## Solution

To make sure the app is always primed, I automated a `keep alive` probe which opens the website and clicks on the "reset" button if visible. I leveraged [puppeteer](https://github.com/puppeteer/puppeteer) to navigate and interact with the webpage using a headless browser. Then I automated a cron-job using Github Actions.

The final repository for the streamlit app looks like this:

```bash
repo/                   # The git repo deployed to streamlit cloud
  .github/
    workflows/
      keep-alive.yml    # The cron job
  probe-action/         # The keep-alive action
    Dockerfile
    action.yml
    probe.js
  app.py                # The streamlit app
```

### Schedule a cron-job with Github Actions

Here is the workflow file `.github/workflows/keep-alive.yml`. Every 2 days it will check out the repo and run the probe action.

```yml
# .github/workflows/keep-alive.yml
name: Trigger Probe of Deployed App on a CRON Schedule
on:
  schedule:
    # Runs "at minute 0 past every 48 hour" (see https://crontab.guru)... ie: every 2 days
    - cron: '0 */48 * * *'

jobs:
  probe_deployed_app:
    runs-on: ubuntu-latest
    name: A job to probe deployed app
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Probe Deployed App Action Step
        uses: ./probe-action # Uses an action in the probe-action directory
        id: probe
```

### Creating a Probe Action

Now we'll setup the action itself. First, create the action metadata file which Github Actions will use to build and run the dockerfile

```yml
# probe-action/action.yml
name: "Probe Deployed App"
description: "Probes a deployed streamlit app."
runs:
  using: "docker"
  image: "Dockerfile"
```

Next, create a very simple dockerfile from an existing puppeteer image. Its only job is to run the probe script:

```docker
# probe-action/Dockerfile
FROM ghcr.io/puppeteer/puppeteer:17.0.0
COPY . /home/pptruser/src
ENTRYPOINT [ "/bin/bash", "-c", "node -e \"$(</home/pptruser/src/probe.js)\"" ]
```

Finally, create the probe script:

```javascript
const puppeteer = require('puppeteer');
const TARGET_URL = "https://<YOUR_STREAMLIT_APP_URL>.streamlitapp.com/";
const WAKE_UP_BUTTON_TEXT = "app back up";
const PAGE_LOAD_GRACE_PERIOD_MS = 8000;

(async () => {
    const browser = await puppeteer.launch(
        { args: ["--no-sandbox"] }
    );

    const page = await browser.newPage();
    await page.goto(TARGET_URL);
    // Wait a grace period for the application to load
    await page.waitForTimeout(PAGE_LOAD_GRACE_PERIOD_MS);

    const checkForHibernation = async (target) => {
        // Look for any buttons containing the target text of the reboot button
        const [button] = await target.$x(`//button[contains(., '${WAKE_UP_BUTTON_TEXT}')]`);
        if (button) {
            console.log("App hibernating. Attempting to wake up!");
            await button.click();
        }
    }

    checkForHibernation(page);
    const frames = (await page.frames());
    for (const frame of frames) {
        await checkForHibernation(frame);
    }

    await browser.close();
})();
```
