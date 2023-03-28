## lang-ident
Set `@ident` attribute and value for `<language/>` elements if this attribtue is missing. The value that is set should be passed via configuration. If no configuration is passed, the empty string is used as value.
To configure the plugin, add the following section to  the config file:
```
[lang-ident]
ident=de
```
If there are multiple `<language/>` elements in the source file, pass  the language codes separated by comma. The `<language/>` elements are matched with the language codes based on index.
``[lang-ident]
ident=de, tr, fr`

```


### Example
Before transformation:
```xml
<langUsage>
  <language>deutsch</language>
  <language>türkçe</language>
  <p>some other element</p>
  <language usage="80">français</language>
</langUsage>
```

After transformation:
```xml
<langUsage>
  <language ident="de">deutsch</language>
  <language ident="tr">türkçe</language>
  <p>some other element</p>
  <language usage="80" ident="fr">français</language>
</langUsage>
```
