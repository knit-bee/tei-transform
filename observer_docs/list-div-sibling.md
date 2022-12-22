## list-div-sibling
Find ```<list/>``` elements that are following sibling of  ```<div/>``` elements and add a new ```<div/>``` wrapping the ```<list/>``` element.

### Example
Before transformation:
```xml
<div>
  <div>
    <p>text</p>
  </div>
  <list>
    <item>text</item>
  </list>
</div>
```

After transformation:
```xml
<div>
  <div>
    <p>text</p>
  </div>
  <div> <!-- insert new <div> here -->
    <list>
      <item>text</item>
    </list>
  </div>
</div>
```
