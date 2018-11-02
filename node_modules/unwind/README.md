unwind
======

Generate objects based on a (possibly nested) path and a value.

## unwind(path, value)

Generates a simple object based on a (possibly nested) path, and the value
associated with it.

### Params:

* **String** *path* A path, or nested path - a representation of nested keys
* **Mixed** *value* The value to set to this path

### Return:

* **Object** The generated object

## Example:
```javascript
unwind('something.nested', 10)
// => { something: { nested: 10 } }
unwind('something', 'else')
// => { something: 'else' }
```
