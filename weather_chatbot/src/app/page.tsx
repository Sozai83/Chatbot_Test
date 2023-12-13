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
  const [multilocation, setMultilocation] = useState('')
  const [responseType, setResposneType] = useState('')


  let temp_response, weather_desc, cur_temp, temp_location, max_temp, min_temp, cur_humidity, temp_date, icon, pop, responseJSX

  const getTimestamp = () => new Date().toDateString()

  const getResponse = async (input: string, conversation: string, question: string, location: string, latitude: string, longitude: string, weatherType: string, date: string) => {
    const apiResponse = fetch((`http://127.0.0.1:5000/askWeacher?input=${input}&conversation=${conversation}&question=${question}&location=${location}&latitude=${latitude}&longitude=${longitude}&weatherType=${weatherType}&date=${date}&multilocation=${multilocation}`), { method: 'POST' })
      .then(resp => resp.json())

    return apiResponse

  }

  const firstConvo = (
    <>Weacher can tell you weathers in locations.<br />
      If you want to know the weather in a location, you can ask "What's the weather in XXX?"<br />
      If you want Weacher to recommend a location in your itenerary to go today or tomorrow, you can ask "Where do you recommend to go today?"</>
  )

  const dialogArr = [
    {
      speaker: 'Weacher',
      dialog: firstConvo,
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
      setMultilocation(test.multilocation)


      if (test.response_type == 'string') {
        temp_response = test.response.split('<br>')
        responseJSX = (
          <>
            {temp_response.map((resp: any) => {
              return (
                <>
                  {resp}<br />
                </>)
            })}
          </>
        )

        setReseponse(responseJSX)


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
            <h2>{temp_date}<img src={icon} /></h2>
            <h3>{location ? location : ''}</h3>
            <p>It is currently {weather_desc} and {cur_temp} ℃.<br />
              The maximum temprature will be {max_temp} ℃, and the loweset will be {min_temp} ℃.<br />
              It is {cur_humidity >= 60 ? 'humid' : cur_humidity >= 30 ? 'normal' : 'dry'}</p >
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
            <h2>{temp_date}<img src={icon} /></h2>
            <h3>{location ? location : ''}</h3>
            <p>Weather in {location ? location : ''} on {temp_date} is {weather_desc}<br />
              The maximum temprature will be {max_temp} ℃, and the loweset will be {min_temp} ℃.<br />
              It is {cur_humidity >= 60 ? 'humid' : cur_humidity >= 30 ? 'normal' : 'dry'} and the chance of rain is {pop * 100} %.</p>
          </>
        )

        setReseponse(responseJSX)

      } else if (test.response_type == 'multiWeatherTomorrow') {
        temp_response = test.response
        responseJSX = (
          <>
            {temp_response.map((weatherData: { cur_weather: any; cur_max_temp: any; cur_min_temp: any; cur_humidity: any; cur_date: any; pop: any; location: any }) => {
              weather_desc = weatherData.cur_weather
              max_temp = weatherData.cur_max_temp
              min_temp = weatherData.cur_min_temp
              cur_humidity = weatherData.cur_humidity
              temp_date = weatherData.cur_date
              pop = weatherData.pop
              temp_location = weatherData.location
              return (
                <p>Weather in {temp_location} is {weather_desc} tomorrow.<br />
                  The maximum temprature will be {max_temp} ℃, and the loweset will be {min_temp} ℃.<br />
                  It is {cur_humidity >= 60 ? 'humid' : cur_humidity >= 30 ? 'normal' : 'dry'} and the chance of rain is {pop * 100} %.</p>
              )
            })}
          </>
        )

        setReseponse(responseJSX)

      } else if (test.response_type == 'multiWeatherToday') {
        temp_response = test.response
        responseJSX = (
          <>
            {temp_response.map((weatherData: { cur_weather: any; cur_temp: any; cur_max_temp: any; cur_min_temp: any; cur_humidity: any; cur_date: any; location: any }) => {
              weather_desc = weatherData.cur_weather
              cur_temp = weatherData.cur_temp
              max_temp = weatherData.cur_max_temp
              min_temp = weatherData.cur_min_temp
              cur_humidity = weatherData.cur_humidity
              temp_date = weatherData.cur_date
              temp_location = weatherData.location

              return (
                <p>It is currently {weather_desc} and {cur_temp} ℃ in {temp_location}.<br />
                  The maximum temprature will be {max_temp} ℃, and the loweset will be {min_temp} ℃ and it is {cur_humidity >= 60 ? 'humid' : cur_humidity >= 30 ? 'normal' : 'dry'}.</p >
              )
            })}
          </>
        )

        setReseponse(responseJSX)

      } else if (test.response_type == 'multiForecast') {
        temp_response = test.response
        responseJSX = (
          <>
            {temp_response.map((forecastData: any[]) => {
              temp_location = forecastData[0].location
              return (
                <>
                  <h3>Forecast for {temp_location}</h3>
                  <table className="forecast-table">
                    <tbody className="forecast">
                      <tr className="forecast-separator">
                        {forecastData.map((weatherData: { weather: any; max_temp: any; min_temp: any; date: string; icon: string }) => {
                          weather_desc = weatherData.weather
                          max_temp = weatherData.max_temp
                          min_temp = weatherData.min_temp
                          const temp_date_list = weatherData.date.split("-")
                          temp_date = temp_date_list[1] + '-' + temp_date_list[2]
                          icon = 'https://openweathermap.org/img/wn/' + weatherData.icon + '.png'
                          return (
                            <td>
                              <table>
                                <thead>
                                  <tr className="date">
                                    <th>{temp_date}</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr className="weather">
                                    <td><img src={icon} alt="Rain" /></td>
                                    <td>{weather_desc}</td>
                                  </tr>
                                  <tr className="temp">
                                    <td className="min"><span className="small">Min: </span>{min_temp} ℃</td>
                                    <td className="max"><span className="small">Max: </span>{max_temp} ℃</td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          )
                        }
                        )}
                      </tr>
                    </tbody >
                  </table >
                </>
              )
            })
            }
          </>
        )

        setReseponse(responseJSX)

      } else {
        temp_response = test.response
        console.log(temp_response)
        responseJSX = (<>
          <h2>Weekly forecast</h2>
          <h3>{location ? location : ''}</h3>
          {temp_response.map((resp: any) => {
          return (
            <>
              <p><b>{resp.date}</b>
                <img src={'https://openweathermap.org/img/wn/' + resp.icon + '.png'} /><br />
                The maximum temprature will be {resp.max_temp} ℃, and the loweset will be {resp.min_temp} ℃.<br />
                It will be {resp.cur_humidity >= 60 ? 'humid' : resp.cur_humidity >= 30 ? 'normal' : 'dry'} and the chance of rain is {resp.pop * 100} %.</p >
            </>)
          })
          }
        </>)

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
            {dialogs.map((d: { speaker: string; dialog: string; timestamp: string }) => {
              return (
                <div className={'chat_dialog ' + d.speaker.toLowerCase()}>
                  <div className="speaker">
                    <span className="speaker">{d.speaker}:</span>
                    <span className="timestamp">{d.timestamp}</span>
                  </div>
                  <p>{d.dialog}</p>
                </div>)
            })}
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
