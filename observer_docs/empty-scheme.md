## empty-scheme
Remove attribute ```@scheme``` from elements if the value is the empty string.

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
    <classCode >Code</classCode>
    <keywords/>
  </textClass>
</profileDesc>
```
