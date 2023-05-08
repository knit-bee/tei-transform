## head-child
Remove `<p/>` and `<ab/>` elements that are children of `<head/>` by stripping the target tag. Children of the target are added as children of `<head/>` and text and tail of the target are added at the appropriate position.
If both the `<head/>` parent and the target contain text, a new `<lb/>` is added to mark the boundary between the text parts.

### Example
Before transformation:
```xml
<div>
  <head>text1
    <p>text2</p>
  </head>
  <head>
    <p>text3</p>
  </head>
  <head>text4
    <ab>
      <hi>text5</hi>
    </ab>
  </head>
</div>
```

After transformation:
```xml
<div>
  <head>text1<lb/>text2</head>
  <head>text3</head>
  <head>text4
    <hi>text5</hi>
  </head>
</div>

```
