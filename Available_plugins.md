## Available Plugins
For more details, click on the plugin name.

### [byline-sibling](observer_docs/byline-sibling.md)
Find elements that are siblings of ```<byline/>``` but invalid after ```<byline/>``` (i.e. ```<p/>``` after ```<byline/>``` if there are already other ```<p/>``` elements before ```<byline/>```). All elements surrounding the ```<byline/>``` until the invalid element and upto any ```<div/>``` are wrapped by a new ```<div/>``` element.
N.B.: The invalid element that was the former direct sibling of ```<byline/>``` is not handled. If this element is a  ```<p/>``` element for example,  use in combination with [p-div-sibling](#p-div-sibling) plugin to remove the invalid ```<p/>``` after  ```<div/>```.

### [classcode](observer_docs/classcode.md)
Replace ```<classcode/>``` elements with ```<classCode/>```.

### [div-text](observer_docs/div-text.md)
Remove text from ```<div/>``` elements and add under new ```<p/>```.

### [double-cell](observer_docs/double-cell.md)
Rename ```<cell/>``` elements that are direct children of ```<cell/>``` to ```<p/>```. If the inner ```<cell/>``` element has children, it will not be renamed but added as a sibling before the outer ```<cell/>```.

### [double-item](observer_docs/double-cell.md)
Rename ```<item/>``` elements that are direct children of  ```<item/>``` to ```<ab/>```. If the inner ```<item/>``` has children, the element will not be renamed but an additional ```<list/>``` will be inserted, wrapping the inner ```<item/>```.

### [filename-element](observer_docs/double-cell.md)
Remove ```<filename/>``` elements.

### [head-type](observer_docs/double-cell.md)
Remove ```type``` attribute from ```<head/>``` elements.

### [hi-parent](observer_docs/double-cell.md)
Wrap ```<hi/>``` elements in ```<p/>```. If siblings contain any ```<div/>```, additionally wrap with the according ```<div#/>```.

### [id-attribute](observer_docs/double-cell.md)
Replace attribute ```id``` with ```xml:id```.

### [list-div-sibling](observer_docs/double-cell.md)
Add a new ```<div/>``` as parent for ```<list/>``` if the  ```<list/>``` element is a sibling of a ```<div/>``` element.

### [missing-publisher](observer_docs/missing-publisher.md)
Add an empty ```<publisher/>``` as first child to ```<publicationStmt/>``` if it does not contain any element from the *publicationStmtPart.agency* group (i.e. ```<publisher/>, <distributor/>, <authority/>```). N.B.: This plugin will only add an empty element, it does not guarantee that the order of the elements is valid if an element of the *publicationStmtPart.agency* group was already present.

### [notesstmt](observer_docs/double-cell.md)
Remove ```type``` from ```<notesStmt/>```.

### [p-div-sibling](observer_docs/double-cell.md)
Add a new ```<div/>``` as parent for ```<p/>``` if the  ```<p/>``` element is a sibling of a ```<div/>``` element.

### [p-head](observer_docs/double-cell.md)
Replace tag ```<head/>``` elements that appear after ```<p/>``` with ```<ab/>``` and add ```type='head'``` attribute.

### [rel-item](observer_docs/rel-item.md)
Remove ```<relatedItem/>``` elements that do not have children or do not have ```@target``` attribute. If the parent element would be empty after removal, it will also be removed.

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
