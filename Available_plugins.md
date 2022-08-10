## Available Plugins
### classcode
Replace ```<classcode/>``` elements with ```<classCode/>```.

### filename-element
Rename ```<filename/>``` nodes.

### head-type
Remove ```type``` attribute from ```<head/>``` elements.

### id-attribute
Replace attribute ```id``` with ```xml:id```.

### notesstmt
Remove ```type``` from ```<notesStmt/>```.

### p-head
Replace tag ```<head/>``` elements that appear after ```<p/>``` with ```<ab/>``` and add ```type='head'``` attribute.

### schemalocation
Remove ```schemaLocation``` attribute from ```<TEI/>``` elements.

### tail-text
Remove text in tail of ```<p/>```, ```<ab/>``` and ```<fw/>``` if tail would be outside of a ```<p/>``` element. Add a new sibling ```<p/>``` that contains the former tail.

### teiheader
Remove ```type``` attribute from ```<teiHeader/>```.

### tei-ns
Add TEI namespace declaration to ```<TEI/>``` element.

### textclass
Replace ```<textclass/>``` elements with ```<textClass/>```.
