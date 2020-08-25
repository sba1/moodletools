The moodletools
===============

This is a client-side moodle command that can be used to gather various
information about a remote Moodle installation.

Requirements
------------

Currently the `moodle` command access a Moodle instance using the web service
designed for the mobile client. Thus, the remote Moodle instance needs to have
the possibility for the client to be activated by the Moodle instance's system
administrator.

Usage
-----

Before using the command, you need to configure remotes. This can be
accomplished by creating a file located in `~/.config/moodlecli/moodlecli.ini`.

The file is stored in the ini-format in which each section is configuing a
remote moodle instance. The pattern looks like this:
```
[url]
short =
locale_mobile_token =
moodle_mobile_app_token =
```

where `url` in the section is the URL of the Moodle instance you want to
control. Within the section `short` can be used to abreviate the URL in the
command. The remaining fields are the tokens that are generated to access your
Moodle account without the need to use the password all the time. You can view
or reset the tokens by navigating to the *Preferences > Security keys* page on
the Moodle instance.

Alternatively, you may want to use the 'moodle remote add' command to configure
the remote:

```
 $ moodle remote add [--retrieve-tokens] <name> <url>
```

If `--retrieve-tokes` is given, `moodle` will ask for the credentials and then
retrieve the necessary tokens.

Commands
--------

```
usage: moodle [-h] commmand [args [args ...]]

Commandline client for Moodle

positional arguments:
  commmand    The command to be invoked.
  args        Further command-specific arguments.

optional arguments:
  -h, --help  show this help message and exit

Available commands:
   course   Deal with Moodle courses
   member   Manage course members
   remote   Manage Moodle remotes

```

Notes
-----

The `moodle` command is in a very early stage and supports only a limited set of
commands. It will change in the future.
