## lb-text
Remove text content from `<lb/>` elements and merge the text with the tail.

### Example
Before transformation:
```xml
<p>text
  <lb>text1</lb>tail
  <lb>text2</lb>
</p>
```

After transformation:
```xml
<p>text
  <lb/>text1 tail
  <lb/>text2
</p>
```
