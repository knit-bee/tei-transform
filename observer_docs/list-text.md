## list-text
Remove text from ```<list/>``` elements and add under new ```<item/>```.

Find ```<list/>``` elements that contain text or any `<item/>` elements with tail and wrap the text in a ```<item/>``` element.

### Example
Before transformation:
```xml
<div>
  <list>
    text
  </list>
  <list>
    <item>text</item>tail
  </list>
</div>
```

After transformation:
```xml
<div>
  <list>
    <item>text</item>
  </list>
  <list>
    <item>text</item>
    <item>tail</item>
  </list>
</div>
```
