## h-level
Change tag of elements with 'h#' tag (e.g. `<h3/>`) to `<ab/>` and add `@type='head'` attribute and `@rend` with the old tag name as value. Invalid attributes, such as `@class` and `@title` are removed from the element.

### Example
Before transformation:
```xml
<div>
  <head/>
  <p/>
  <h3 class='sth'>
    <lb/>text
  </h3>
  <p/>
</div>
```

After transformation:
```xml
<div>
  <head/>
  <p/>
  <ab type="head" rend="h3">
    <lb/>text
  </ab>
  <p/>
</div>
```
