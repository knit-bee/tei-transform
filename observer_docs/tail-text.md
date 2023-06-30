## tail-text
Remove tail of elements with tag `<p/>`, `<ab/>`, `<fw/>`, `<table/>`, `<list/>`, `<head/>` or `<quote/>` if the parent of the element is  ```<div/>```, `<body/>`, or `<floatingText/>`. A new ```<p/>``` element is added containing the former tail as next sibling of the original element and the tail is removed from the original element.
If the element has tag `fw/` and is a direct child of `<floatingText/>`, `fw`  will be used as the tag of the newly added element instead of `p` (as `<p/>` cannot appear as child of `<floatingText/>`)

### Example
Before transformation:
```xml
<div>
  <p>text</p>tail
  <div>
    <table/>tail
  </div>
</div>
```

After transformation:
```xml
<div>
  <p>text</p>
  <p>tail</p>
  <div>
    <table/>
    <p>tail</p>
</div>
```
