## byline-sibling
Find elements that are siblings after  ```<byline/>``` where the  ```<byline/>```elements has siblings on both sides that are not part of [model.divWrapper](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.divWrapper.html) (i.e. tags other than "argument", "byline", "dateline", "docAuthor", "docDate", "epigraph", "signed", "meeting", "salute", "head", "opener" (the last two only at the beginning of a textual division)).
A new ```<div/>```element is added to encompass all sibling elements (up to any ```<div/>``` if present) before the violating element.
N.B.: The following siblings are not handled, i.e. a ```<p/>``` element might now appear as a sibling of ```<div/>```. To avoid this invalid tree structure, use in combination with [div-sibling](observer_docs/div-sibling-md).

### Example
Before transformation:
```xml
<!-- ... -->
</teiHeader>
<text>
   <!-- ... -->
   <div>
     <p>text</p>
     <byline/>
     <p>text</p>
   </div>
   <div>
     <div/>
     <ab/>
     <p/>
     <byline/>
     <p/>
   </div>
   <!-- ... -->
</text>
</TEI>
```

After transformation:
```xml
<!-- ... -->
</teiHeader>
<text>
   <!-- ... -->
   <div>
     <div>
       <p>text</p>
       <byline/>
       <p>text</p>
     </div>
   </div>
   <div>
     <div/>
     <div>
       <ab/>
       <p/>
       <byline/>
     </div>
     <p/> <!-- use div-sibling to correct this -->
   </div>
   <!-- ... -->
</text>
</TEI>
```
