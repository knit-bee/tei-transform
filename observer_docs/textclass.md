## texclass
Replace element tag ```<textclass/>``` with ```<textClass/>```.

### Example
Before transformation:
```xml
<!-- ... -->
<teiHeader>
   <!-- ... -->
   <profileDesc>
     <textclass>
       <classCode>
         some code
       </classCode>
     </textclass>
   </profileDesc>
   <!-- ... -->
</teiHeader>
<!-- ... -->
```

After transformation:
```xml
<!-- ... -->
<teiHeader>
   <!-- ... -->
   <profileDesc>
     <textClass>
       <classCode>
         some code
       </classCode>
     </textClass>
   </profileDesc>
   <!-- ... -->
</teiHeader>
<!-- ... -->
```
