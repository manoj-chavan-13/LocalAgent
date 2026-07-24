import React from 'react'
import { Chat } from './components/Chat'

function App() {
  return (
    <div className="flex flex-col h-screen w-full items-center bg-gray-900 text-white pt-10">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-blue-500 mb-2">Local AI DevOps Agent</h1>
        <p className="text-gray-400">Connected to local Ollama & ChromaDB</p>
      </div>
      
      <Chat />
    </div>
  )
}

export default App
