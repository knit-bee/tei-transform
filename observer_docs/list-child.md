## list-child
Wrap `<p/>`, `<hi/>`, `<ab/>`, `<list/>`, `<del/>`, `<quote/>`, and `<table/>` elements that are direct descendants of `<list/>` in a new `<item/>` element.


### Example
Before transformation:
```xml
<list>
  <head>list head</head>
  <item>text</item>
  <p>text2</p>tail
  <hi>text3</hi>
</list>
```

After transformation:
```xml
<list>
  <head>list head</head>
  <item>text</item>
  <item>
    <p>text2</p>tail
  </item>
  <item>
    <hi>text3</hi>
  </item>
</list>
```
