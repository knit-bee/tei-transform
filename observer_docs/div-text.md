## div-text
Remove text from ```<div/>``` elements and add under new ```<p/>```.

Find ```<div/>``` elements that contain text and wrap the text in a ```<p/>``` element. If the length of the text is one (i.e. it is only one non-whitespace character), it is added to the first child of the ```<div/>``` element if this is a ```<p/>```.

### Example
Before transformation:
```xml
<div>
  <div>
    text
  </div>
  <div>T
    <p>ext</p>
  </div>
</div>
```

After transformation:
```xml
<div>
  <div>
    <p>text</p>
  </div>
  <div>
    <p>Text</p>
  </div>
</div>
```
