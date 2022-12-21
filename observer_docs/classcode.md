## classcode
Replace ```<classcode/>``` elements with ```<classCode/>```. The whole tree is checked but usually `<classCode/` should only appear in the *teiHeader*.

### Example
Before transformation:
```xml
<!-- ... -->
<teiHeader>
   <!-- ... -->
   <profileDesc>
     <textClass>
       <classcode>
         some code
       </classcode>
     </textClass>
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
