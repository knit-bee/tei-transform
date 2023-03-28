## empty-kw
Add empty `<term/>` element to `<keywords/>` elements that don't contain any children.

### Example
Before transformation:
```xml
<profileDesc>
  <textClass>
    <keywords/>
  </textClass>
</profileDesc>
```

After transformation:
```xml
<profileDesc>
  <textClass>
    <keywords>
      <term/>
    </keywords>
  </textClass>
</profileDesc>
```
