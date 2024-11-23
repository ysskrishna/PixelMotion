import React, { useState, useEffect } from 'react';
import config from './config';
import axios from 'axios';
import useWebSocket from 'react-use-websocket';
import Table from './components/Table';
import Upload from './components/Upload';
import Logo from './assets/logo.png';


const App = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [tasks, setTasks] = useState([]);
  
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get(`${config?.baseUrl}/user/tasks`);
        setTasks(response.data);
      } catch (error) {
        console.error('Error fetching tasks: ', error);
      }
    };
    fetchTasks();
  }, []);

  const { sendMessage, lastMessage, readyState } = useWebSocket(config?.websocketBaseUrl, {
    onOpen: () => console.log('WebSocket connection opened!'),
    onClose: () => console.log('WebSocket connection closed!'),
    onError: (event) => console.error('WebSocket error:', event),
    onMessage: (event) => {
      const updatedTask = JSON.parse(event.data);
      setTasks((prevTasks) => {
        const taskIndex = prevTasks.findIndex(task => task.task_id === updatedTask.task_id);
        if (taskIndex !== -1) {
          const updatedTasks = [...prevTasks];
          updatedTasks[taskIndex] = updatedTask;
          return updatedTasks;
        }
        return [...prevTasks, updatedTask];
      });
    },
  });

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append('file', file);
      const title = file.name.split('.').slice(0, -1).join('.') || "title";
      formData.append('title', title);

      const response = await axios.post(`${config?.baseUrl}/user/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const task_id = response.data.task_id;
      console.log(`Upload successful, Task ID: ${task_id}`);

    } catch (error) {
      console.error('Error uploading file: ', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 my-2">
      <section className="bg-white dark:bg-gray-900">
        <div className="px-4 mx-auto max-w-screen-xl text-center justify-center items-center">
          <img src={Logo} alt="PixelMotion" className="h-10 md:h-12  mx-auto" />  
          <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-16">Transform your images into stunning  videos in just a few clicks.</p>
        </div>
      </section>

      <div className="flex flex-col items-center justify-center w-full">
        <Upload file={file} handleFileChange={handleFileChange} />
        <button 
          onClick={handleUpload} 
          disabled={!file || uploading} 
          className="w-[100%] disabled:opacity-50 disabled:cursor-not-allowed my-2 cursor-pointer relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-cyan-500 to-blue-500 group-hover:from-cyan-500 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-cyan-200 dark:focus:ring-cyan-800"
        >
          <span className="w-[100%] relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
            Generate Video
          </span>
        </button>
      </div> 
      
      <Table data={tasks} />
    </div>
  );
};

export default App;