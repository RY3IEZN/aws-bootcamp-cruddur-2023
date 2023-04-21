import './MessageGroupPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation  from '../components/DesktopNavigation';
import MessageGroupFeed from '../components/MessageGroupFeed';
import MessagesFeed from '../components/MessageFeed';
import MessagesForm from '../components/MessageForm';

// [TODO] Authenication
import Cookies from 'js-cookie'

export default function MessageGroupPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadMessageGroupsData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${"eyJraWQiOiI4ZzNMWlVPY0xIXC9XWVhiYjltVTdZcGx2SVlNcFNDb0pxa21nWU1MWEtkdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjZTFmMmJmNS1lMDc4LTRjOTItOGQwMy01YTgxYmRlNzZjNWIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0yLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMl9Ja212MjNZZVEiLCJjbGllbnRfaWQiOiIzdXVmZzZkYmppcGs2b2ZpMTNkcmxvdTUycyIsIm9yaWdpbl9qdGkiOiIwYzY3ZWYwNS0wNjlmLTQyMjgtOTlhMy0wYTc4NGY3ODc2ZmEiLCJldmVudF9pZCI6ImEwNTM3YTc5LWQ1YjYtNDZkMC05YTU1LTgwZTU0ZDJjMmVhNCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2ODE5OTU0OTksImV4cCI6MTY4MTk5OTA5OSwiaWF0IjoxNjgxOTk1NDk5LCJqdGkiOiIxNWFjYWNmYS03MzZiLTQ3ZjctODQ2Yi04MDk4YjZhZGQ2YzEiLCJ1c2VybmFtZSI6ImNlMWYyYmY1LWUwNzgtNGM5Mi04ZDAzLTVhODFiZGU3NmM1YiJ9.fFAyGS6_F9MnQTIvcsaS3n6neiJ8pukZQRYP-fDu__WNYH4p6Rjdzh_29xnwP4OMHMQqFKFTNU2fDXiBCk3bRg8P1UXu7BWNw7Omv2kJhbLteYHcO4Znd-_cDXGlOj5J0FAHNOKiakvNOarnDueHONbRFvgLbpNNcuBGrb_Eq6Tne7C6EdhIhdJHHWYHYJhzjJrC5kKWLQXXjtf-b4SMvDeZcu01TooCIIzWryDcN4gTffVRRQcU2iJj8d4FQjWXO4cl9HhI2hxO2a9cTrTa0xkEPvWXok0fQSrNSdhpP3bMKVH3wCaFLb8zXhxU4wZ-4S4hK_OaZD4p3T-dwEsLSg"}`
        },
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessageGroups(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };  

  const loadMessageGroupData = async () => {
    try {
      const handle = `@${params.handle}`;
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${handle}`
      const res = await fetch(backend_url, {
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessages(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };  

  const checkAuth = async () => {
    console.log('checkAuth')
    // [TODO] Authenication
    if (Cookies.get('user.logged_in')) {
      setUser({
        display_name: Cookies.get('user.name'),
        handle: Cookies.get('user.username')
      })
    }
  };

  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadMessageGroupsData();
    loadMessageGroupData();
    checkAuth();
  }, [])
  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content messages'>
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}