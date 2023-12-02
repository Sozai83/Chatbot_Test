"use client"

import Image from 'next/image'
import styles from './page.module.css'
import React, { useState } from 'react'

export default function Home() {
  const [askWeacherInput, setAskWeacherInput] = useState('')

  const getTimestamp = () => new Date().toUTCString()

  const dialogArr = [
    {
      speaker: 'Weacher',
      dialog: 'Hello. My name is Weacher. How can I help?',
      timestamp: getTimestamp()
    },
  ]
  const [dialogs, setDialogs] = useState<any>(dialogArr)

  const askWeacher = (e: any) => {
    e.preventDefault()

    const input = {
      speaker: 'You',
      dialog: askWeacherInput,
      timestamp: getTimestamp()
    }

    setDialogs([...dialogs, input])
    setAskWeacherInput('')

  }




  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <h1>Talk to Weacher</h1>
        <section className="chat">
          <section className="weacher" >
            {dialogs.map(d => {
              return (<><p>{d.speaker}:</p><p>{d.dialog}</p><p>{d.timestamp}</p></>)
            })}
          </section>
        </section>
        <section className="form" onSubmit={askWeacher}>
          <form action="/askWeacher" method="post" id="messageArea">
            <input type="text" name="ask_weacher" value={askWeacherInput} onChange={e => setAskWeacherInput(e.target.value)} aria-label="Question for weacher" />
            <input type="submit" className="submit" value="Check weather" aria-label="submit" />
          </form>
        </section>
      </div>
    </main >
  )
}
