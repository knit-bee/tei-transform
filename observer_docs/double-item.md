## double-item
Convert ```<item/>``` elements that are direct children of  ```<item/>``` to ```<ab/>```. If the inner ```<item/>``` has children, the element will not be renamed but wrapped by an additional ```<list/>```.

### Example
Before transformation:
```xml
<list>
  <item>
    <item>
      text1
    </item>
  </item>
  <item>
    <item>
      <p>text2</p>
    </item>
  </item>
</list>
```

After transformation:
```xml
<list>
  <item>
    <ab>
      text1
    </ab>
  </item>
  <item>
    <list>
      <item>
        <p>text2</p>
      </item>
    </list>
  </item>
</list>
```
