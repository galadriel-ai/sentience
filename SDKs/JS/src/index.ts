const isBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';
const isNode = typeof process !== 'undefined' && process.versions != null && process.versions.node != null;

if (isBrowser) {
  console.log('Running in the browser');
}

if (isNode) {
  console.log('Running in Node.js');
}

if (isNode && !global.fetch) {
  global.fetch = require('node-fetch');
}

fetch("https://api.galadriel.com/")
  .then(response => {
    console.log("Success")
    console.log(response)
  }).catch(err => {
    console.log(err)
})
console.log("SDK Initialized")