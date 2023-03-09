## mq-attr
Remove attribute ```@measure_quantity``` from ```<term/>``` elements.

### Example
Before transformation:
```xml
<teiHeader>
  <profileDesc>
    <textClass>
      <classCode/>
      <keywords>
        <term measure_quantity='1'>Term1</term>        
        <term measure_quantity='2'>Term2</term>
        <term measure_quantity='4'>Term3</term>
      </keywords>
    </textClass>
  </profileDesc>
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <profileDesc>
    <textClass>
      <classCode/>
      <keywords>
        <term>Term1</term>        
        <term>Term2</term>
        <term>Term3</term>
      </keywords>
    </textClass>
  </profileDesc>
</teiHeader>
```
