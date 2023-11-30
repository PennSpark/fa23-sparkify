import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';


function App() {

  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      const body = {
        imgPath: "homeress.png"
      }
      axios.post("http://localhost:3001/getS3Image", body)
      .then(resp => {
        const imgUrl = resp.data.imgUrl;
        setImageUrl(imgUrl);
      })
      .catch(error => {
        console.error(error);
      });

    };

    fetchImage();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={imageUrl} className="App-logo" alt="logo"/>

        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
