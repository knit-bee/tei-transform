## invalid-attr
Remove unwanted attributes from all elements unless the element is marked as an exception.
List the attributes that should be removed and their exceptions in the config file.

The config file should contain the following section:
```
[invalid-attr]
some-attribute = elem1
other-attribute =
third-attribute = elem1, elem2
```
List the (localnames of) elements where an attribute should not be removed after the equals sign. To exclude multiple elements, separate them by comma.
If an attribute should be removed from all elements, leave the space after the equals sign empty.

### Example
Config section:
```
[invalid-attr]
class=msItem
datetime=

```
Before transformation:
```xml
<TEI>
  <!- ... ->
  <msItem class='sth'/>
  <!- ... ->
  <div datetime='dd-mm-yyyy'>
    <list class='ul'>
      <item datetime='dd-mm-yyyy'/>
    </list>
  </div>
</TEI>
```

After transformation:
```xml
<TEI>
  <!- ... ->
  <msItem class='sth'/>
  <!- ... ->
  <div>
    <list>
      <item/>
    </list>
  </div>
</TEI>
```
