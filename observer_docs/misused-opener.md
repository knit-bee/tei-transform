## misused-opener
Change tag of `<opener/>` elements to `<ab/>` if they don't appear at the top of a section because they have previous siblings that are not part of [model.divWrapper](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.divWrapper.html) (i.e. tags other than "argument", "byline", "dateline", "docAuthor", "docDate", "epigraph", "signed", "meeting", "salute", "head", "opener").
Elements with children are not transformed, since it is assumed that they are really intended to be `<opener/>`. However, the position would still be invalid and should be handled.

### Example
Before transformation:
```xml
<!-- ... -->
  </teiHeader>
  <text>
     <body>
       <div>
         <p>text</p>
         <opener/>
         <p>text</p>
       </div>
       <div>
         <p/>
         <opener>
           <dateline/>
         </opener>
         <p/>
       </div>
     <!-- ... -->
   </body>
  </text>
```

After transformation:
```xml
<!-- ... -->
  </teiHeader>
  <text>
     <body>
       <div>
         <p>text</p>
         <ab/>
         <p>text</p>
       </div>
       <div>
         <p/>
         <!-- not changed but <p/> before invalid-->
         <opener>
           <dateline/>
         </opener>
         <p/>
       </div>
     <!-- ... -->
   </body>
  </text>
```
