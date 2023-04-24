## list-text
Remove text from ```<list/>``` elements and add under new ```<item/>```.

Find ```<list/>``` elements that contain text or any elements with tail. The text content of `<list/>` is added under a new ```<item/>``` element. Any text content in tails on `<item/>` or other children of the `<list/>` are concatenated with the text content of the `<item/>` (resp. added to the tail of the last child if `<item/>`, if present). If the child has `<lb/>` tag, it is appended to its previous sibling.

### Example
Before transformation:
```xml
<div>
  <list>
    text
  </list>
  <list>
    text
    <lb/>text2
  </list>
  <list>
    <item>text</item>tail
    <item>
      <p>text</p>tail2
    </item>tail3
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
    <item>text<lb/>text2</item>
  </list>
  <list>
    <item>text tail</item>
    <item>
      <p>text</p>tail2 tail3
    </item>
  </list>
</div>
```
