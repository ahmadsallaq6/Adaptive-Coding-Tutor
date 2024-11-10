// Monaco Editor setup for code input
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs' } });

require(['vs/editor/editor.main'], function () {
    // Ensure Monaco editor is initialized before it's used
    const editor = monaco.editor.create(document.getElementById('code-editor'), {
        value: '',
        language: 'javascript',
        theme: 'vs-dark',
    });

    // Store editor instance globally
    window.editor = editor;  // This will make editor accessible globally
});