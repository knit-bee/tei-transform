## Available Plugins
For more details, click on the plugin name.

### [author-type](observer_docs/author-type.md)
Remove ```@type``` attribute from ```<author/>``` elements.

### [body-text](observer_docs/body-text.md)
Remove text content from `<body/>` elements and add to first child if it can contain text. Else, add a new `<p/>` that is inserted as first child of `<body/>`.

### [byline-sibling](observer_docs/byline-sibling.md)
Find elements that are siblings of ```<byline/>``` but invalid after ```<byline/>``` (i.e. ```<p/>``` after ```<byline/>``` if there are already other ```<p/>``` elements before ```<byline/>```). All elements surrounding the ```<byline/>``` until the invalid element and upto any ```<div/>``` are wrapped by a new ```<div/>``` element.
N.B.: The invalid element that was the former direct sibling of ```<byline/>``` is not handled. If this element is a  ```<p/>``` element for example,  use in combination with [p-div-sibling](#p-div-sibling) plugin to remove the invalid ```<p/>``` after  ```<div/>```.

### [classcode](observer_docs/classcode.md)
Replace ```<classcode/>``` elements with ```<classCode/>```.

### [code-elem](observer_docs/code-elem.md)
Replace `<code/>` elements with `<ab/>` if the element has descendants or is a descendant of `<div/>`. N.B.: Use in combination with *double-plike* plugin to avoid nesting of `<ab/>`
 and `<p/>` elements.

### [div-parent](observer_docs/div-parent.md)
Strip `<div/>` elements with invalid parents. If the parent of `<div/>` is `<p/>` or `<ab/>`, the `<div/>` element is added as a sibling of its parent.

### [div-sibling](observer_docs/div-sibling.md)
Add a new ```<div/>``` as parent for ```<table/>```,  `<quote/>`, and `<list/>` elements  if they are a following sibling of a ```<div/>``` element.

### [div-tail](observer_docs/div-tail.md)
Remove tail from `<div/>` elements and add under new `<p/>` that is appended as last child of the `<div/>`.

### [div-text](observer_docs/div-text.md)
Remove text from ```<div/>``` elements and add under new ```<p/>```.

### [double-cell](observer_docs/double-cell.md)
Rename ```<cell/>``` elements that are direct children of ```<cell/>``` to ```<p/>```. If the inner ```<cell/>``` element has children, it will not be renamed but added as a sibling before the outer ```<cell/>```.

### [double-item](observer_docs/double-item.md)
Rename ```<item/>``` elements that are direct children of  ```<item/>``` to ```<ab/>```. If the inner ```<item/>``` has children, the element will not be renamed but an additional ```<list/>``` will be inserted, wrapping the inner ```<item/>```.

### [double-plike](observer_docs/double-plike.md)
Remove nested paragraph-like elements (`<p/>`, `<ab/>`) by stripping the inner tag.

### [empty-body](observer_docs/empty-body.md)
Add empty `<p/>` to `<body/>` element without (required) children.

### [empty-elem](observer_docs/empty-elem.md)
Remove empty `<list/>`, `<table/>`, and `<row/>` elements.

### [empty-kw](observer_docs/empty-kw.md)
Add empty `<term/>` to empty `<keywords/>` elements.

### [empty-scheme](observer_docs/empty-scheme.md)
Find `<classCode/>` elements  with `@scheme` attribute with empty value and set new value or remove element. This requires configuration, see [empty-scheme](observer_docs/empty-scheme.md) for more details.

### [filename-element](observer_docs/filename-element.md)
Remove ```<filename/>``` elements.

### [fw-child](observer_docs/fw-child.md)
Find `<p/>`, `<list/>`, and `<table/>` elements with `<fw/>` parent. Merge `<p/>` element into parent. Rename parent to `<ab/>` if target has tag `<list/>` or `<table/>`.

### [head-type](observer_docs/head-type.md)
Remove ```@type``` attribute from ```<head/>``` elements.

### [hi-child](observer_docs/hi-child.md)
Remove `<p/>` elements with `<hi/>` parent by stripping the `<p/>` tag.

### [hi-parent](observer_docs/hi-parent.md)
Wrap ```<hi/>``` elements in ```<p/>```. If siblings contain any ```<div/>```, additionally wrap with the according ```<div#/>```.

### [id-attribute](observer_docs/id-attribute.md)
Replace attribute ```@id``` with ```@xml:id```.

### [lang-ident](observer_docs/lang-ident.md)
Set `@ident` attribute for `<language/>` elements where this attribute is missing. Values to be set should be passed via configuration files, see [lang-ident](observer_docs/lang-ident.md) for more details.

### [lb-div](observer_docs/lb-div.md)
Wrap `<lb/>` elements with tail that have `<div/>` parent with a new `<p/>` element.

### [list-child](observer_docs/list-child.md)
Add an `<item/>` element as parent of `<p/>`, `<ab/>`, and `<hi/>` elements that are direct descendants of `<list/>`.

### [list-text](observer_docs/list-text.md)
Remove text from `<list/>` elements that is not contained by any `<item/>` and add under a new `<item/>` element.

### [lonely-cell](observer_docs/lonely-cell.md)
Find `<cell/>` elements that are outside of `<row/>` and wrap them in `<row/>` and `<table/>`, if necessary.

### [lonely-item](observer_docs/lonely-item.md)
Find `<item/>` elements that are outside of `<list/>` and wrap them in `<list/>`. Empty elements are removed.

### [lonely-row](observer_docs/lonely-row.md)
Wrap `<row/>` elements that are outside a `<table/>` element with `<table/>`.

### [missing-publisher](observer_docs/missing-publisher.md)
Add an empty ```<publisher/>``` as first child to ```<publicationStmt/>``` if it does not contain any element from the *publicationStmtPart.agency* group (i.e. ```<publisher/>, <distributor/>, <authority/>```). N.B.: This plugin will only add an empty element, it does not guarantee that the order of the elements is valid if an element of the *publicationStmtPart.agency* group was already present.

### [misused-byline](observer_docs/misused-byline.md)
Convert `<byline/>` elements with `<p/>`-like siblings before and after to  `<ab/>`.

### [misused-opener](observer_docs/misused-opener.md)
Change tag of `<opener/>` elements that have invalid older sibling and no children (except `<lb/>`) to `<ab/>`.

### [mq-attr](observer_docs/mq-attr.md)
Remove attribute `@measure_quantity` from `<term/>` elements.

### [nested-fw](observer_docs/nested-fw.md)
Find `<fw/>` elements with `<fw/>` parent and `<list/>` or `<table/>` as descendant (and the `<list/>`/`<table/>` has `<fw/>` or `<p/>` as parent) and add as sibling of the parent. Any following siblings are added under a new `<fw/>` after the target.

### [notesstmt](observer_docs/notesstmt.md)
Remove ```@type``` from ```<notesStmt/>```.

### [p-div-sibling](observer_docs/p-div-sibling.md)
Add a new ```<div/>``` as parent for ```<p/>``` if the  ```<p/>``` element is a sibling of a ```<div/>``` element.

### [p-head](observer_docs/p-head.md)
Replace tag ```<head/>``` elements that appear after  invalid elements (e.g ```<p/>```) with ```<ab/>``` and add ```type='head'``` attribute.

### [p-parent](observer_docs/p-parent.md)
Add `<p/>` as parent to elements that incorrectly have `<div/>` as parent. This requires configuration to set the target elements, see [p-parent](observer_docs/p-parent.md) for more details.

### [rel-item](observer_docs/rel-item.md)
Remove ```<relatedItem/>``` elements that do not have children or do not have ```@target``` attribute. If the parent element would be empty after removal, it will also be removed.

### [resp-note](observer_docs/resp-note.md)
Wrap `<note/>` elements with parent `<respStmt/>` with a new `<resp/>` element if the `<note/>` element has no previous `<resp/>` sibling.

### [schemalocation](observer_docs/schemalocation.md)
Remove ```@schemaLocation``` attribute from ```<TEI/>``` elements.

### [table-text](observer_docs/table-text.md)
Remove text content of `<table/>` and tail of children of `<table/>`. Any `<p/>` child of table is converted to `<fw/>`.

### [tail-text](observer_docs/tail-text.md)
Remove text in tail of ```<p/>```, ```<ab/>``` and ```<fw/>``` if parent is a ```<div/>```, `<body/>`, or `<floatingText/>`  element. Add a new sibling ```<p/>``` that contains the former tail.

### [teiheader](observer_docs/teiheader.md)
Remove ```@type``` attribute from ```<teiHeader/>```.

### [tei-ns](observer_docs/tei-ns.md)
Add TEI namespace declaration to ```<TEI/>``` element.

### [textclass](observer_docs/textclass.md)
Replace ```<textclass/>``` elements with ```<textClass/>```.

### [ul-elem](observer_docs/ul-elem.md)
Replace `<ul/>` elements with `<list/>`.

### [unfinished-elem](observer_docs/unfinished-elem.md)
Find `<table/>` and `<list/>` elements without the required children and add an empty child with the required tag.
