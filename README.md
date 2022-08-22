# tei-transform
Fix errors in xml document that make it invalid according to TEI P5


## Installation
Install from github repository:

```sh
$ pip install git+ssh://github.com/knit-bee/tei-transform.git
```

### Requirements
* Python >= 3.8
* lxml >= 4.0

To run tests, you also need:

* pytest >= 7.0

## Usage
tei-transform allows command-line usage:
```sh
 $ tei-transform --help
usage: tei-transform [-h]
                     [--transformation TRANSFORMATION [TRANSFORMATION ...]]
                     [--revision_config REVISION_CONFIG] [--output OUTPUT]
                     file

Parse an xml-file that has some errors (that make it invalid according to TEI
P5) and apply transformations the file content.

positional arguments:
  file                  File to process

optional arguments:
  -h, --help            show this help message and exit
  --transformation TRANSFORMATION [TRANSFORMATION ...], -t TRANSFORMATION [TRANSFORMATION ...]
                        Observer plugins that should be used to transform the
                        file content. If no plugin is passed, the default
                        setting will be used ('schemalocation, id-attribute,
                        teiheader, notesstmt, filename-element')
  --revision_config REVISION_CONFIG, -c REVISION_CONFIG
                        Name of config file where information for change entry
                        for revisionDesc element in the teiHeader is stored.
                        If no file is passed, no new change entry will be
                        added to revisionDesc. The file should contain a
                        section [revision] with the entries 'person =
                        Firstname Lastname', 'reason = reason why the file was
                        changed' and an optional 'date = YYYY-MM-DD'. If the
                        person entry should contain multiple names, separate
                        them by comma. If no date parameter is passed, the
                        current date will be inserted
  --output OUTPUT, -o OUTPUT
                        Name of output directory to store transformed file
                        in. If the directory doesn't exist, it will be
                        created. No output file will be created, if this
                        option is disabled.
```

The **file** argument takes the path to the file you want to change.

If you want to add an entry in the <revisionDesc/> section of the transformed
document, you can use the keyword argument **revision_config** and pass the name of
the config file. This file should contain the following section:

```
[revision]
person = Name of the responsible person
reason = Reason why the file changed
date = YYYY-MM-DD
```
(The date entry is optional.)


For all available transformation plugins, see [Available Plugins](Available_plugins.md) .

### Example

```sh
$ tei-transform file.xml  --transformation schemalocation, id-attribute
```
This will apply the transformations defined for the **schemalocation** and **id-attribute**
plugins.

## Add Plugins
To customize the transformations, you can add your own plugin that specifies a
transformation. To do so, you should add an observer that implements the interace
of the AbstractNodeObserver, i.e. it should define how to recognise the nodes it
 is going to act on and the change it will apply to these nodes.

Then, you need to register the plugin in the **setup.cfg** as an entry point under
the **node_observer** section, e.g.

```
[options.entry_points]

node_observer =
  id-attribute = tei_transform.id_attribute_observer:IdAttributeObserver
```

After that, run
```
$ python setup.py develop
```
in order to make the registration effective.

## License
Copyright © 2022 Berlin-Brandenburgische Akademie der Wissenschaften.

This project is licensed under the GNU General Public License v3.0.
