## p-parent
Add a `<p/>` element as parent to elements with incorrect `<div/>` parent. Configuration of this plugin is obligatory.

In the config file, add the following section:
```
[p-parent]
target = element
```
Set the localnames of the elements that should be handled as values of the *target* key.
To set multiple tags, separate them by comma, e.g.:
```
[p-parent]
target = code, del, hi
```

### Example
Before transformation:
```xml
<div>
  <p>text1</p>
  <code>text2</code>tail
  <p>text3</p>
  <del>text4</del>
  <hi>text5</hi>
</div>
```

After transformation:
```xml
<div>
  <p>text1</p>
  <p>
    <code>text2</code>tail
  </p>
  <p>text3</p>
  <p>
    <del>text4</del>
  </p>
  <p>
    <hi>text5</hi>
  </p>
</div>
```
