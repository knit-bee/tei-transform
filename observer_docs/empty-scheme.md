## empty-scheme
Find `<classCode/>` elements that have attribute ```@scheme``` where the value of the attribute is the empty string. Configuration of this plugin is mandatory.

In the config file that is used for the transformation, add the following section to set a new value for the `@scheme` attribute:
```
[empty-scheme]
scheme=path/to/scheme
```
To remove the `<classCode/>` element instead, use the following configuration:
```
[empty-scheme]
action=remove
```
N.B.: If both configurations are set, setting the new value will override the removal action.

### Example
Before transformation:
```xml
<profileDesc>
  <textClass>
    <classCode scheme="" xml:id="sc">Code</classCode>
    <keywords/>
  </textClass>
</profileDesc>
```

After transformation:
```xml
<profileDesc>
  <textClass>
    <classCode scheme="path/to/scheme" xml:id="sc">Code</classCode>
    <keywords/>
  </textClass>
</profileDesc>
```
