## resp-note
Add a new `<resp/>` element as parent for `<note/>` elements with `<respStmt/>` parent that have no `<resp/>` element as previous sibling.

### Example
Before transformation:
```xml
<teiHeader>
  <titleStmt>
    <title>Titel</title>
    <author>Author</author>
    <respStmt>
      <note>some note</note>
      <name>Person1</name>
    </respStmt>
    <respStmt>
      <orgName>Organisation</orgName>
      <note>note2</note>
    </respStmt>
  </titleStmt>
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <titleStmt>
    <title>Titel</title>
    <author>Author</author>
    <respStmt>
      <resp>
        <note>some note</note>
      </resp>
      <name>Person1</name>
    </respStmt>
    <respStmt>
      <orgName>Organisation</orgName>
      <resp>
        <note>note2</note>
      </resp>
    </respStmt>
  </titleStmt>
</teiHeader>

```
