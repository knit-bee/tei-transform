## empty-scheme
Find `<classCode/>` elements that have attribute ```@scheme``` where the value of the attribute is the empty string. Configuration of this plugin is mandatory.

In the config file that is used for the transformation, add the following section:
```
[empty-scheme]
scheme=path/to/scheme
```

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
