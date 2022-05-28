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
import 'prismjs/components/prism-yaml.min.js'
import 'prismjs/components/prism-nginx.min.js'
import 'prismjs/components/prism-vim.min.js'
import 'prismjs/components/prism-typescript.min.js'
import 'prismjs/components/prism-toml.min.js'
import 'prismjs/components/prism-systemd.min.js'
import 'prismjs/components/prism-scss.min.js'
import 'prismjs/components/prism-regex.min.js'
import 'prismjs/components/prism-graphql.min.js'
import 'prismjs/components/prism-go.min.js'
import 'prismjs/components/prism-java.min.js'
import 'prismjs/components/prism-lua.min.js'
import 'prismjs/components/prism-docker.min.js'

function renderMarkdown(markdown: string) {
  const md = MarkdownIt()
  md.use(markdownItPrism, {
    defaultLanguageForUnknown: 'javascript',
    defaultLanguageForUnspecified: 'javascript',
  })
  return md.render(markdown)
}
export default renderMarkdown
