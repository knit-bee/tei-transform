## cell-tail
Remove tail of `<cell/>` elements. The content of the tail is added to the text of the `<cell/>` or, if the  `<cell/>` has children to the  tail of the last child.

### Example
Before transformation:
```xml
<table>
  <row>
    <cell>
      text1
    </cell>tail1
    <cell>text2
      <p>text3</p>
    </cell>tail2
  </row>
</table>
```

After transformation:
```xml
<table>
  <row>
    <cell>text1 tail1</cell>
    <cell>text2
      <p>text3</p>tail2
    </cell>
  </row>
</table>

```
