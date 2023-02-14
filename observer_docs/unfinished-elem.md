## unfinished-elem
Find `<list/>` and `<table/>` elements that lack required children (`<item/>` resp. `<row/>`) and add a new, empty child from the required category.

For `<table/>` elements, a new `<row/>` with an empty `<cell/>` is added.
For `<list/>` elements, an empty `<item/>` is added.

Some elements that can appear in `<list/>` or `<table/>` should only occur at the beginning. Thus, for `<list/>` the new `<item/>` is inserted after the last of any `<head/>` or `<desc/>` element.
For `<table/>` elements, the new `<row/>` is inserted after any occurring `<head/>` element.
Otherwise, the new element is added as first child of the `<list/>` or `<table/>` element.

### Example
Before transformation:
```xml
<div>
  <table>
    <head>text1</head>
    <fw>text2</fw>
  </table>
  <list>
    <head>text3</head>
    <desc>text4</head>
    <byline>text5</byline>
  </list>
</div>
```

After transformation:
```xml
<div>
  <table>
    <head>text1</head>
    <row>
      <cell/>
    </row>
    <fw>text2</fw>
  </table>
  <list>
    <head>text3</head>
    <desc>text4</head>
    <item/>
    <byline>text5</byline>
  </list>
</div>
```
