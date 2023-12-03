"use client"

import Image from 'next/image'
import styles from './page.module.css'
import React, { useState, useEffect } from 'react'


export default function Home() {
  const [askWeacherInput, setAskWeacherInput] = useState('')
  const [response, setReseponse] = useState<any>()
  const [conversation, setConversation] = useState('')
  const [question, setQuestion] = useState('')
  const [location, setLocation] = useState('')
  const [latitude, setLatitude] = useState('')
  const [longitude, setLongitude] = useState('')
  const [weatherType, setWeatherType] = useState('')
  const [date, setDate] = useState('')
  const [responseType, setResposneType] = useState('')


  let temp_response, weather_desc, cur_temp, max_temp, min_temp, cur_humidity, temp_date, icon, pop, responseJSX

  const getTimestamp = () => new Date().toDateString()

  const getResponse = async (input: string, conversation: string, question: string, location: string, latitude: string, longitude: string, weatherType: string, date: string) => {
    const apiResponse = fetch((`http://127.0.0.1:5000/askWeacher?input=${input}&conversation=${conversation}&question=${question}&location=${location}&latitude=${latitude}&longitude=${longitude}&weatherType=${weatherType}&date=${date}`), { method: 'POST' })
      .then(resp => resp.json())

    return apiResponse

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

    if (test) {
      setConversation(test.conversation)
      setQuestion(test.question)
      setLocation(test.location)
      setLatitude(test.latitude)
      setLongitude(test.longitude)
      setWeatherType(test.weather_type)
      setDate(test.date)
      setResposneType(test.response_type)


      if (test.response_type == 'string') {
        setReseponse(test.response)


      } else if (test.response_type == 'weather') {
        temp_response = test.response
        weather_desc = temp_response.cur_weather
        cur_temp = temp_response.cur_temp
        max_temp = temp_response.cur_max_temp
        min_temp = temp_response.cur_min_temp
        cur_humidity = temp_response.cur_humidity
        temp_date = temp_response.cur_date
        icon = 'https://openweathermap.org/img/wn/' + temp_response.icon + '.png'

        responseJSX = (
          <>
            <p>Weather in {location ? location : ''} on {temp_date}</p>
            <img src={icon} />
            <p>Description: {weather_desc}</p>
            <p>Current temprature: {cur_temp}</p>
            <p>Max temperature: {max_temp}</p>
            <p>Min temperature: {min_temp}</p>
            <p>Humidity: {cur_humidity}</p>
          </>

        )

        setReseponse(responseJSX)


      } else if (test.response_type == 'weather specific date') {
        temp_response = test.response
        weather_desc = temp_response.cur_weather
        max_temp = temp_response.cur_max_temp
        min_temp = temp_response.cur_min_temp
        cur_humidity = temp_response.cur_humidity
        temp_date = temp_response.cur_date
        pop = temp_response.pop
        icon = 'https://openweathermap.org/img/wn/' + temp_response.icon + '.png'

        responseJSX = (
          <>
            <p>Weather in {location ? location : ''} on {temp_date}</p>
            <img src={icon} />
            <p>Description: {weather_desc}</p>
            <p>Max temperature: {max_temp}</p>
            <p>Min temperature: {min_temp}</p>
            <p>Humidity: {cur_humidity}</p>
            <p>Precipitation: {pop} %</p>
          </>

        )

        setReseponse(responseJSX)

      } else {
        temp_response = test.response
        console.log(temp_response)
        responseJSX = temp_response.map((resp: any) => {
          return (
            <>
              <p>Weather in {location ? location : ''} on {resp.date}</p>
              <img src={'https://openweathermap.org/img/wn/' + resp.icon + '.png'} />
              <p>Description: {resp.weather}</p>
              <p>Max temperature: {resp.max_temp}</p>
              <p>Min temperature: {resp.min_temp}</p>
              <p>Humidity: {resp.humidity}</p>
              <p>Precipitation: {resp.pop * 100} %</p>
            </>)
        })

        setReseponse(responseJSX)

      }
    }

    setAskWeacherInput('')

  }

  useEffect(() => {
    if (response) {
      const output = {
        speaker: 'Weacher',
        dialog: response,
        timestamp: getTimestamp()
      }

      setDialogs([...dialogs, output])
    }
  }, [response])

  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <h1>Talk to Weacher</h1>
        <section className="chat">
          <div className="weacher" >
            {dialogs.map((d: { speaker: string; dialog: string; timestamp: string }) => {
              return (
                <div className={d.speaker.toLowerCase()}>
                  <span className="speaker">{d.speaker}:</span>
                  <span className="timestamp">{d.timestamp}</span>
                  <p>{d.dialog}</p>
                </div>)
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
