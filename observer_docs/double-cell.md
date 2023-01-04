## (plugin name)
Covert ```<cell/>``` elements that are direct children of ```<cell/>``` to ```<p/>``` if the ```<cell/>``` only contains text. If the inner ```<cell/>``` also has children, it will be added as a sibling **before** the outer ```<cell/>``` .

### Example
Before transformation:
```xml
<table>
  <row>
    <cell>
      <cell>
        text1
      </cell>
    </cell>
  </row>
  <row>
    <cell>
      <cell>
        <p>text2</p>
      </cell>
      <p>text3</p>
    <cell>
  </row>
</table>
```

After transformation:
```xml
<table>
  <row>
    <cell>
      <p>
        text1
      </p>
    </cell>
  </row>
  <row>
    <cell>
      <p>text2</p>
    </cell>
    <cell>
      <p>text3</p>
    <cell>
  </row>
</table>
```
