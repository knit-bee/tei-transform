## empty-elem
Remove empty `<list/>`, `<table/>`, and `<row/>` elements. Elements are considered empty if they don't contain text or have any descendant elements.

If the empty target elements has a (non-whitespace character) tail, for `<list/>` and `<table/>` the tail content is concatenated with the text of the parent element or, if the parent shouldn't contain text (e.g. if its tag is `<div/>`), a new `<p/>` element containing the text is added at the index of the empty target element.
For `<row/>` elements, the tail is added to a new `<cell/>` element that is added as child of the formerly empty `<row/>` (the element is then not removed, since it is not empty anymore).

N.B.: Elements with tags `<list/>`, `<table/>`, or `<row/>` shouldn't contain text characters and should be handled accordingly but they are not considered empty and thus not handled by this plugin.

### Example
Before transformation:
```xml
<div>
  <div>
    <list>
      <item>
        <list/>
        tail1
      </item>
    </list>
  </div>
  <div>
    <table>
      <row/>
      <row/>tail2
    </table>
    <table/>
  </div>
  <div>
    <p/>
    <list/>tail3
  </div>
</div>
```

After transformation:
```xml
<div>
  <div>
    <list>
      <item>
        <!-- tail of empty <list/> added to parent-->
        tail1
      </item>
    </list>
  </div>
  <div>
    <table>
      <!-- first empty <row/> removed  -->
      <row>
        <!-- tail of second added under <cell/> -->
        <cell>tail2</cell>
      </row>
    </table>
    <!-- empty <table/> removed -->
  </div>
  <div>
    <p/>
      <!-- tail of empty <list/> added to new <p/> -->
    <p>tail3</p>
  </div>
</div>
```
