(comment) @comment

;(snippet body: (_) @injection.language) @injection.content

(section caller: (_) @type)
(section task: (_) @function)
(section reciever: (_) @variable.parameter)

(section code_remark: (_) @string.special)
(section set: (_) @constant)

[
  ">"
  "."
  "["
  "]"
  "{"
  "}"
  "("
  ")"
] @punctuation.delimiter
