import { useState } from 'react'
import API from '../api/axios'

export default function ChatBot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed) return

    const newMessages = [...messages, { from: 'user', text: trimmed }]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    try {
      const res = await API.post('/chat/', { question: trimmed })
      setMessages((msgs) => [...msgs, { from: 'bot', text: res.data.answer }])
    } catch (err) {
      setMessages((msgs) => [...msgs, { from: 'bot', text: 'Error contacting server.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Help Chat</h1>
      <div className="border rounded-lg p-4 mb-4 h-96 overflow-y-auto bg-white">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`mb-2 flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-3 py-2 rounded-lg max-w-prose whitespace-pre-wrap ${
                m.from === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-900'
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
      </div>
      <div className="flex">
        <textarea
          className="flex-1 border rounded-lg p-2 mr-2"
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask a question..."
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
