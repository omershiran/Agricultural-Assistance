import React, { useState, useRef } from 'react';
 
function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [recordings, setRecordings] = useState([]);
  const mediaRecorderRef = useRef(null);

  

  function startRecording() {
    return new Promise((resolve, reject) => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
      const mediaRecorder = new MediaRecorder(stream);
      const audioContext = new AudioContext();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      microphone.connect(analyser);
      analyser.fftSize = 2048;
      let dataArray = new Uint8Array(analyser.frequencyBinCount);
      let silenceCounter = 0;
      let animationFrameId;
  
      mediaRecorder.start();
  
      
      const checkSilence = () => {
        analyser.getByteFrequencyData(dataArray);
        let sum = dataArray.reduce((a, b) => a + b, 0);
        let average = sum / dataArray.length;
      console.log('average:  ',average);
        // זיהוי שתיקה בהתבסס על עוצמה ממוצעת נמוכה
        if (average < 5) { // SILENCE_THRESHOLD יש להתאים
          silenceCounter++;
          if (silenceCounter > 100) { 
            console.log('in if');
            mediaRecorder.stop();
            audioContext.close();
            cancelAnimationFrame(animationFrameId);
            return;
          }
        } else {
          silenceCounter = 0;
        }
      
        animationFrameId = requestAnimationFrame(checkSilence);
      };
      
        
  
      // התחלת בדיקת השתיקה
      animationFrameId = requestAnimationFrame(checkSilence);
  
      // התחלת הקלטת האודיו
      mediaRecorder.ondataavailable = async (e) => {
        const audioBlob = new Blob([e.data], { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audioFile', audioBlob, Date.now()+'.wav');
      
        try {
          const response = await fetch('http://192.168.1.195:8000/audio_manager/uploade', {
            method: 'POST',
            body: formData,
          });
          if (response.ok) {
            console.log('Recording uploaded');
          } else {
            console.error('Upload failed');
          }
        } catch (error) {
          console.error('Error in upload: ', error);
        }
      };
      
  
      // כאשר ההקלטה מסתיימת
      mediaRecorder.onstop = () => {
        stream.getTracks().forEach(track => track.stop());
        resolve();
        // טיפול בסיום ההקלטה, לדוגמה הצגת הקלטה למשתמש
      };
      mediaRecorder.onerror = (e) => reject(e);
    }).catch(err => {
      console.error('Error in starting recording: ', err);
    });
  }
    )}
  

  function playAudioFile(filePath) {
    return new Promise((resolve, reject) => {
      const audio = new Audio(filePath);
      audio.onended = resolve; // כאשר הנגינה תסתיים, הבטחה תתממש
      audio.onerror = reject; // במקרה של שגיאה בנגינה
      audio.play();
    });
  }
  const  voiceChat=async()=>{
  let voiceFiles=['voice_files/1703533449.8110383.wav', 'voice_files/1703533462.9922378.wav', 'voice_files/1703533465.917387.wav', 'voice_files/1703530981.7942042.wav', 'voice_files/1703530985.1124084.wav', 'voice_files/1703530990.303712.wav', 'voice_files/1703530993.1538754.wav', 'voice_files/1703531000.7579093.wav', 'voice_files/1703531004.640988.wav', 'voice_files/1703531009.1521485.wav', 'voice_files/1703531012.083384.wav', 'voice_files/1703531015.6642942.wav', 'voice_files/1703531018.9017708.wav', 'voice_files/1703531024.6664872.wav', 'voice_files/1703531028.385587.wav', 'voice_files/1703531037.1895192.wav', 'voice_files/1703531040.257128.wav', 'voice_files/1703531044.783376.wav', 'voice_files/1703531048.0661132.wav']
  await playAudioFile(voiceFiles[0])

    for (let i=1;i<voiceFiles.length;i=i+2){
      let dt1=Date.now()
      await startRecording()
      let dt2=Date.now()
      if (dt2-dt1<3000){
      await playAudioFile('voice_files/1703535158.978147.wav')
      await startRecording()

      }

      await playAudioFile(voiceFiles[i])
      await playAudioFile(voiceFiles[i+1])
    }


  }
  return (
    <div>
      
      <div>
        {recordings.map((recording, index) => (
          <div key={index}>
            <audio src={recording} controls />
          </div>
        ))}
      </div>
      <button onClick={voiceChat}>Play Audio File</button>
        
    
    
    </div>
  );
}

export default AudioRecorder;
