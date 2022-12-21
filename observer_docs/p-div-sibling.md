## p-div-sibling
Find ```<p/>``` elements that are sibling of  ```<div/>``` elements and add a new ```<div/>``` wrapping the ```<p/>``` element. Multiple consecutive ```<p/>``` elements following the same ```<div/>``` element will be grouped under the same new ```<div/>``` (instead of adding a ```<div/>``` for each ```<p/>```).
Empty ```<p/>``` elements (i.e. not containing text, tail, or children) will be removed.

### Example
Before transformation:
```xml
<body>
  <div>
    <p>text1</p>
  </div>
  <p>text2</p>
  <p>text3</p>
  <p/>
</body>
```

After transformation:
```xml
<body>
  <div>
    <p>text1</p>
  </div>
  <div>
    <p>text2</p>
    <p>text3</p>
  </div>
</body>
```
