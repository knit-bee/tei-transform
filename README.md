# tei-transform
Fix errors in xml document that make it invalid according to TEI P5


## Installation
Install from github repository:

```sh
$ pip install git+https://github.com/knit-bee/tei-transform.git
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
 ```
```
usage: tei-transform [-h] [--transformation TRANSFORMATION [TRANSFORMATION ...]]
                     [--revision-config REVISION_CONFIG] [--output OUTPUT]
                     [--no-validation | --copy-valid | --ignore-valid]
                     file_or_dir

Parse xml-files that have some errors (that make them invalid according to TEI P5) and apply
transformations to the file content and save to new file. The old file is not changed. There
are options to validate files before processing to e.g. ignore valid files. Files are validated
against the Relax NG scheme of the current version of the TEI guidelines (tei_all.rng).

positional arguments:
  file_or_dir           File or directory to process

options:
  -h, --help            show this help message and exit
  --transformation TRANSFORMATION [TRANSFORMATION ...], -t TRANSFORMATION [TRANSFORMATION ...]
                        Observer plugins that should be used to transform the file content. If
                        no plugin is passed, the default setting will be used ('schemalocation,
                        id-attribute, teiheader, notesstmt, filename-element')
  --revision-config REVISION_CONFIG, -c REVISION_CONFIG
                        Name of config file where information for change entry for revisionDesc
                        element in the teiHeader is stored. If no file is passed, no new change
                        entry will be added to revisionDesc. The file should contain a section
                        [revision] with the entries 'person = Firstname Lastname', 'reason =
                        reason why the file was changed' and an optional 'date = YYYY-MM-DD'.
                        If the person entry should contain multiple names, separate them by
                        comma. If no date parameter is passed, the current date will be
                        inserted.
  --output OUTPUT, -o OUTPUT
                        Name of output directory to store transformed file in. If the directory
                        doesn't exist, it will be created. Default is 'output'.
  --no-validation       Do not validate files before processing. This is the default setting.
                        Valid files will be written to output directory with new timestamp but
                        without changes to the xml tree. An xml-declaration is added as default
                        and the formatting of the document may change.
  --copy-valid          Validate files before processing and copy valid files from input
                        directory to output directory, trying to preserve metadata (i.e.
                        timestamps are preserved, permissions if possible).
  --ignore-valid        Validate files before processing and ignore valid file during
                        processing. Only transformed files are written to the output directory.
```

The **file_or_dir** argument takes the path to the file you want to change.

If you want to add an entry in the <revisionDesc/> section of the transformed
document, you can use the keyword argument **revision-config** and pass the name of
the config file. This file should contain the following section:

```
[revision]
person = Name of the responsible person
reason = Reason how the file changed
date = YYYY-MM-DD
```
(The date entry is optional.)
This will be rendered as a `<change/>` element and added as last child to `<revisionDesc/>`. If
 a `<revisionDesc/>` element was not part of the teiHeader before, it is added as last child
 of the `<teiHeader/>` element. The `<change/>` element will appear as follows in the document:

```
<change when="YYYY-MM-DD">
  <name>Name of the responsible person</name>Reason how the file changed
</change>
```
N.B.: Make sure that the `<revisionDesc/>` of the document(s) that are processed
 contains only `<change/>` or `<listChange/>` elements as direct children. If the
 original format uses `<list/>`, the resulting document might not be valid.


For all available transformation plugins, see [Available Plugins](Available_plugins.md) .

### Example

```sh
$ tei-transform file.xml  --transformation schemalocation, id-attribute
```
This will apply the transformations defined for the **schemalocation** and **id-attribute**
plugins.

## Add Plugins
To customize the transformations, you can add your own plugin that specifies a
transformation. To do so, you should add an observer that implements the interface
of the AbstractNodeObserver, i.e. it should define how to recognise the nodes it
 is going to act on and the change it will apply to these nodes.

Then, you need to register the plugin in the **pyproject.toml** as an entry point under
the **node_observer** section, e.g.

```
[project.entry-points."node_observer"]
id-attribute = tei_transform.id_attribute_observer:IdAttributeObserver
```

After that, install the plugin, e.g. with
```sh
$ pip install plugin
```


## License
Copyright © 2022 Berlin-Brandenburgische Akademie der Wissenschaften.

This project is licensed under the GNU General Public License v3.0.
