import React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

const PhotoForm = ({ file, handleFileChange, handleUploadClick, error}) => (
  <div className="field field--wide">
    <input name="photo" type="file" onChange={handleFileChange} />

    <div>{file && `${file.name} - ${file.type}`}</div>

    <button onClick={handleUploadClick}>Upload</button>
  </div>
);

export const Photo = () => {
  const [file, setFile] = React.useState("");
  const [error, setError] = React.useState();
  
  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUploadClick = () => {
    if (!file) {
      console.error("file missing")
      return;
    }

    // 👇 Uploading the file using the fetch API to the server
    fetch('http://localhost:5000/api/photo/upload', {
      method: 'POST',
      body: file,
    })
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));
  };

  return (
    <PhotoForm
        file={file}
        error={error}
        handleFileChange={handleFileChange}
        handleUploadClick={handleUploadClick}
      />
  );
};

Photo.title = "Photo";
Photo.path = "/";
