import React from 'react';

const PhotoDetectForm = ({ file, handleFileChange, handleUploadClick, image, error}) => (
  <div className="field field--wide">
    <input name="photo" type="file" onChange={handleFileChange} />

    <div>{file && `${file.name} - ${file.type}`}</div>

    <button onClick={handleUploadClick}>Upload</button>

    <div>
      <img src={image} />
    </div>
  </div>
);

export const PhotoDetect = () => {
  const [file, setFile] = React.useState("");
  const [error, setError] = React.useState();
  const [image, setImage] = React.useState("");
  
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
    fetch('http://localhost:5000/api/photo/detect', {
      method: 'POST',
      body: file,
    })
      .then((res) => {
        res.json().then(detection => {
          console.log(detection);
          setImage('http://localhost:5000/image?path=' + detection.path);
        });
      })
      .then((data) => {})
      .catch((err) => console.error(err));
  };

  return (
    <PhotoDetectForm
        file={file}
        error={error}
        handleFileChange={handleFileChange}
        handleUploadClick={handleUploadClick}
        image={image}
      />
  );
};

PhotoDetect.title = "PhotoDetect";
PhotoDetect.path = "/";
