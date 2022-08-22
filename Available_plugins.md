## Available Plugins
### classcode
Replace ```<classcode/>``` elements with ```<classCode/>```.

### div-text
Remove text from ```<div/>``` elements and add under new ```<p/>```.

### double-cell
Rename ```<cell/>``` elements that are direct children of ```<cell/>``` to ```<p/>```. If the inner ```<cell/>``` element has children, it will not be renamed but added as a sibling before the outer ```<cell/>```.

### double-item
Rename ```<item/>``` elements that are direct children of  ```<item/>``` to ```<ab/>```. If the inner ```<item/>``` has children, the element will not be renamed but a additional ```<list/>``` will be inserted, wrapping the inner ```<item/>```.

### filename-element
Rename ```<filename/>``` nodes.

### head-type
Remove ```type``` attribute from ```<head/>``` elements.

### hi-parent
Wrap ```<hi/>``` elements in ```<p/>```. If siblings contain any ```<div/>```, additionally wrap with the according ```<div#/>```.

### id-attribute
Replace attribute ```id``` with ```xml:id```.

### list-div-sibling
Add a new ```<div/>``` as parent for ```<list/>``` if the  ```<list/>``` element is a sibling of a ```<div/>``` element.

### notesstmt
Remove ```type``` from ```<notesStmt/>```.

### p-div-sibling
Add a new ```<div/>``` as parent for ```<p/>``` if the  ```<p/>``` element is a sibling of a ```<div/>``` element.

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
