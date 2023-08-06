# Jenkins Auto Updater

Using the magic of automation from Selenium and Python, this script will automatically update your Jenkins plugins[1].

[1]At least most of them...

## Requirements

    - Python >= 3.7
    - Firefox >= 91.5

## Usage
Just run the script with the following arguments.

`python jenkinsautoupdater.py <jenkins URL> <username> <password> [auto restart jenkins]`

**Example**:

`python jenkinsautoupdater.py https://example.org admin AS3cur3P@$$w0rd! true`

**Note**: If you execute the command with true at the end, Jenkins will auto-restart after downloading the updates.
Default behaviour is to not restart Jenkins.

## Caveats
Sometimes the script will not select some checkboxes, but at least will click most of them.
It's up to you if you want to click the last ones or retry. If you want to fix this behaviour, you're welcome to do so.
