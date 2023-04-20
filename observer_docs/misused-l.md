## misused-l
Change tags of `<l/>` elements that are direct children of `<s/>` to `<w/>`.

### Example
Before transformation:
```xml
<p>
  <s>
    <l>First</l>
    <l>Word</l>
    <l>,</l>
    <l>Second</l>
    <l>word</l>
  </s>
</p>
```

After transformation:
```xml
<p>
  <s>
    <w>First</w>
    <w>Word</w>
    <w>,</w>
    <w>Second</w>
    <w>word</w>
  </s>
</p>
```
