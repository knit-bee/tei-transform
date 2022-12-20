## tail-text
Remove tail of elements with tag ```<p/>, <ab/>, or <fw/>``` if the tail is outside of a ```<p/>``` element (and counting thus, for example, as text in ```<div/>```). A new ```<p/>``` element is added containing the former tail as next sibling and the tail is removed from the original element. Only elements that are descendants of ```<text/>``` are considered (i.e. elements in the ```<teiHeader>``` are ignored.)

### Example
Before transformation:
```xml
<div>
  <p>text</p>tail
</div>
```

After transformation:
```xml
<div>
  <p>text</p>
  <p>tail</p>
</div>
```
