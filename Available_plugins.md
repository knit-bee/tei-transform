## Available Plugins
For more details, click on the plugin name.

### [classcode](observer_docs/classcode.md)
Replace ```<classcode/>``` elements with ```<classCode/>```.

### [div-text](observer_docs/div-text.md)
Remove text from ```<div/>``` elements and add under new ```<p/>```.

### [double-cell](observer_docs/double-cell.md)
Rename ```<cell/>``` elements that are direct children of ```<cell/>``` to ```<p/>```. If the inner ```<cell/>``` element has children, it will not be renamed but added as a sibling before the outer ```<cell/>```.

### [double-item](observer_docs/double-cell.md)
Rename ```<item/>``` elements that are direct children of  ```<item/>``` to ```<ab/>```. If the inner ```<item/>``` has children, the element will not be renamed but an additional ```<list/>``` will be inserted, wrapping the inner ```<item/>```.

### [filename-element](observer_docs/double-cell.md)
Rename ```<filename/>``` nodes.

### [head-type](observer_docs/double-cell.md)
Remove ```type``` attribute from ```<head/>``` elements.

### [hi-parent](observer_docs/double-cell.md)
Wrap ```<hi/>``` elements in ```<p/>```. If siblings contain any ```<div/>```, additionally wrap with the according ```<div#/>```.

### [id-attribute](observer_docs/double-cell.md)
Replace attribute ```id``` with ```xml:id```.

### [list-div-sibling](observer_docs/double-cell.md)
Add a new ```<div/>``` as parent for ```<list/>``` if the  ```<list/>``` element is a sibling of a ```<div/>``` element.

### [notesstmt](observer_docs/double-cell.md)
Remove ```type``` from ```<notesStmt/>```.

### [p-div-sibling](observer_docs/double-cell.md)
Add a new ```<div/>``` as parent for ```<p/>``` if the  ```<p/>``` element is a sibling of a ```<div/>``` element.

### [p-head](observer_docs/double-cell.md)
Replace tag ```<head/>``` elements that appear after ```<p/>``` with ```<ab/>``` and add ```type='head'``` attribute.

### [schemalocation](observer_docs/double-cell.md)
Remove ```schemaLocation``` attribute from ```<TEI/>``` elements.

### [tail-text](observer_docs/double-cell.md)
Remove text in tail of ```<p/>```, ```<ab/>``` and ```<fw/>``` if tail would be outside of a ```<p/>``` element. Add a new sibling ```<p/>``` that contains the former tail.

### [teiheader](observer_docs/double-cell.md)
Remove ```type``` attribute from ```<teiHeader/>```.

### [tei-ns](observer_docs/double-cell.md)
Add TEI namespace declaration to ```<TEI/>``` element.

### [textclass](observer_docs/double-cell.md)
Replace ```<textclass/>``` elements with ```<textClass/>```.
