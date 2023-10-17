## empty-attrib
Remove attributes with empty string as value from all elements.
List the attributes that should be removed in the config file.

The config file should contain the following section:
```
[empty-attrib]
target = atr1, atr2
```
### Example
Config section:
```
[empty-attrib]
target=level

```
Before transformation:
```xml
<TEI>
  <!- ... ->
  <title level=''/>
  <!- ... ->
  <div>
    <head level=''>text</head>
    <p/>
  </div>
</TEI>
```

After transformation:
```xml
<TEI>
  <!- ... ->
  <title/>
  <!- ... ->
  <div>
    <head>text</head>
    <p/>
  </div>
</TEI>
```
