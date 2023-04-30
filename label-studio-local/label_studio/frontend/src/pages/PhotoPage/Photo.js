import React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { LsPlus } from "../../assets/icons";
import { Button } from "../../components";
import { cn } from '../../utils/bem';

const PhotoForm = ({ file, handleFileChange, handleUploadClick, error}) => (
  <div className="field field--wide">
    <input type="file" onChange={handleFileChange} />

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
    fetch('https://httpbin.org/post', {
      method: 'POST',
      body: file,
      // 👇 Set headers manually for single file upload
      headers: {
        'content-type': file.type,
        'content-length': `${file.size}`, // 👈 Headers need to be a string
      },
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
