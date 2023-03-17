## misused-byline
Change tag of `<byline/>` elements to `<ab/>` if they have previous AND  following siblings with `<p/>`, `<ab/>`, `<head/>`, `<div/>`, or `<opener/>` tags (`<head/>`, `<div/>`, and `<opener/>` only for following siblings).  

### Example
Before transformation:
```xml
<div>
  <head>text1</head>
  <byline>text2</byline>
  <p>text3</p>
  <byline>text4</byline>
  <p>text5</p>
</div>
```

After transformation:
```xml
<div>
  <head>text1</head>
  <byline>text2</byline>
  <p>text3</p>
  <ab>text4</ab>
  <p>text5</p>
</div>
```
