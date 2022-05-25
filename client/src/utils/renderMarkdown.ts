import MarkdownIt from 'markdown-it'
import markdownItPrism from 'markdown-it-prism'

import 'prismjs/components/prism-c.min.js'
import 'prismjs/components/prism-cpp.min.js'
import 'prismjs/components/prism-csharp.min.js'
import 'prismjs/components/prism-haskell.min.js'
import 'prismjs/components/prism-javascript.min.js'
import 'prismjs/components/prism-python.min.js'
import 'prismjs/components/prism-rust.min.js'
import 'prismjs/components/prism-solidity.min.js'

function renderMarkdown(markdown: string) {
  const md = MarkdownIt()
  md.use(markdownItPrism, {
    defaultLanguage: 'javascript',
  })
  return md.render(markdown)
}
export default renderMarkdown
