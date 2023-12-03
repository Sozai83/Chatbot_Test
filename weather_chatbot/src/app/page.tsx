"use client"

import Image from 'next/image'
import styles from './page.module.css'
import React, { useState } from 'react'


export default function Home() {
  const [askWeacherInput, setAskWeacherInput] = useState('')
  const [response, setReseponse] = useState()
  const [conversation, setConversation] = useState('')
  const [question, setQuestion] = useState('')
  const [location, setLocation] = useState('')
  const [latitude, setLatitude] = useState('')
  const [longitude, setLongitude] = useState('')
  const [weatherType, setWeatherType] = useState('')
  const [date, setDate] = useState('')
  const [responseType, setResposneType] = useState('')

  const getTimestamp = () => new Date().toString()

  const getResponse = async (input: string, conversation: string, question: string, location: string, latitude: string, longitude: string, weatherType: string, date: string) => {
    const response = fetch((`http://127.0.0.1:5000/askWeacher?input=${input}&conversation=${conversation}&question=${question}&location=${location}&latitude=${latitude}&longitude=${longitude}&weatherType=${weatherType}&date=${date}`), { method: 'POST' })
      .then(resp => resp.json())

    return response

  }

  const dialogArr = [
    {
      speaker: 'Weacher',
      dialog: 'Hello. My name is Weacher. How can I help?',
      timestamp: getTimestamp()
    },
  ]
  const [dialogs, setDialogs] = useState<any>(dialogArr)

  const askWeacher = async (e: any) => {
    e.preventDefault()

    const input = {
      speaker: 'You',
      dialog: askWeacherInput,
      timestamp: getTimestamp()
    }

    setDialogs([...dialogs, input])

    const test = await getResponse(askWeacherInput, conversation, question, location, latitude, longitude, weatherType, date)

    setConversation(test.conversation)
    setQuestion(test.question)
    setLocation(test.location)
    setLatitude(test.latitude)
    setLongitude(test.longitude)
    setWeatherType(test.weather_type)
    setDate(test.date)

    setReseponse(test.response)

    const output = {
      speaker: 'Weacher',
      dialog: test.response,
      timestamp: getTimestamp()
    }

    setDialogs([...dialogs, input, output])

    setAskWeacherInput('')

  }

  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <h1>Talk to Weacher</h1>
        <section className="chat">
          <div className="weacher" >
            {dialogs.map((d: { speaker: string | number | boolean | React.ReactElement<string, string | React.JSXElementConstructor<string>> | Iterable<React.ReactNode> | React.ReactPortal | React.PromiseLikeOfReactNode | null | undefined; dialog: string | number | boolean | React.ReactElement<string, string | React.JSXElementConstructor<string>> | Iterable<React.ReactNode> | React.ReactPortal | React.PromiseLikeOfReactNode | null | undefined; timestamp: string | number | boolean | React.ReactElement<string, string | React.JSXElementConstructor<string>> | Iterable<React.ReactNode> | React.ReactPortal | React.PromiseLikeOfReactNode | null | undefined }) => {
              return (<><p>{d.speaker}:</p><p>{d.dialog}</p><p>{d.timestamp}</p></>)
            })}
          </div>
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
